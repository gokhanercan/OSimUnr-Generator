import threading
from pathlib import Path
from typing import List, Set, Tuple, Optional
import os

from src.Core.Dataset.DiscreteScale import DiscreteScale
from src.Core.IWordSource import IWordSource
from src.Core.Languages.LinguisticContext import LinguisticContext
from src.Core.Morphology.MorphoLex.MorphoLexSegmentedDataset import MorphoLexSegmentedDataset
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.IRootDetector import IRootDetector
from src.Core.Morphology.RootDetection.SharingRootDetector import SharingRootDetector
from src.Core.Morphology.RootDetection.IRootDetectorStack import IRootDetectorStack
from src.Core.Morphology.RootDetection.RootDetectorCacher import RootDetectorCacher
from src.Core.Morphology.RootDetection.RootDetectorStackCacher import RootDetectorStackCacher
from src.Core.OSimUnrPipeline.EnglishPipeline import EnglishPipeline
from src.Core.OSimUnrPipeline.PipelineProviderBase import PipelineProviderBase

from src.Core.Orthographic.NormalizedStringSimilarity.EditDistance import EditDistance
from src.Core.Orthographic.OverlappingMeasures import OverlapCoefficient
from src.Core.Preprocessing.WordsFilterer import WordsFilterer
from src.Core.Segmentation.Tokenizers.ITokenizer import ITokenizer
from src.Core.Segmentation.Tokenizers.NLTKWhitespaceTokenizer import NLTKWhitespaceTokenizer
from src.Core.Segmentation.Tokenizers.TokenizerCacher import TokenizerCacher
from src.Core.Task.IWordRelatednessBinaryClassifier import IWordRelatednessBinaryClassifier
from src.Core.WordNet.Classifiers.BlacklistedConceptsWordNetRelatednessFilterer import \
    BlacklistedConceptsWordNetRelatednessFilterer
from src.Core.WordNet.Classifiers.ConceptWiseWordNetRelatednessFilterer import ConceptWiseWordNetRelatednessFilterer
from src.Core.WordNet.Classifiers.DefinitionBasedRelatednessClassifier import DefinitionBasedRelatednessClassifier
from src.Core.WordNet.Classifiers.WordNetDerivationallyRelatedBinaryClassifier import \
    WordNetDerivationallyRelatedBinaryClassifier
from src.Core.WordNet.IWordNet import IWordNet, WordNetSimilarityAlgorithms, Lemma2SynsetMatching
from src.Core.WordNet.NLTKWordNetWrapper import NLTKWordNetWrapper
from src.Core.WordNet.WordPairDefinitionSourceFilter import WordPairDefinitionSourceFilter
from src.Core.WordPair import WordPair
from src.Core.WordPairSynthesizer import WordPairSynthesizer
from src.Core.WordSim.IWordSimilarity import IWordSimilarity
from src.Core.WordSim.WordSimDataset import WordSimDataset
from src.Core.WordSim.WordSimilarityNormalizerWrapper import WordSimilarityNormalizerWrapper
from src.Tools import StringHelper, Resources
from src.Tools.FormatHelper import NoDecimal
from src.Tools.Logger import logp, log, logl, logpif

#region Console Settings
import warnings  # https://stackoverflow.com/questions/15777951/how-to-suppress-pandas-future-warning/15778297

from src.Tools.Progressor import Progressor

warnings.simplefilter(action='ignore', category=FutureWarning)
#endregion

logp("Building common context for the study...", True)
Provider: PipelineProviderBase = EnglishPipeline(LinguisticContext.BuildEnglishContext(),EditDistance())
_Context: LinguisticContext = Provider.Context
_StudyName = "MyStudy"
def GetStudyPath() -> str:
    return Resources.GetStudyPath(_StudyName)
_RndName = StringHelper.GenerateRandomStr(5)
_MaxRelatedness = 0.25
logp("Common context executed!", True)

def IsIWordSimilarityInstance(model) -> bool:
    """
    Special type check is required for performance purposes because some models' bases cannot be implemented when cythonized.
    :param model:
    :return:
    """
    if isinstance(model, IWordSimilarity): return True
    name = str(model)
    if name == "nedit" or name == "edit": return True
    if name.__contains__("over_ft"): return True
    if name.__contains__("jacc"): return True
    if name.__contains__("dice"): return True
    if name.__contains__("ngram"): return True
    return False

# region: 0: Common Helper
def snapshotSave(wordpairs, subDatasetName: str, scale: DiscreteScale) -> Optional[str]:
    """
    Saves any list of word pairs.
    :param wordpairs:
    :param subDatasetName:
    :param scale:
    :return: Returns the path where it saved the file after saving.
    """
    if (not wordpairs or wordpairs.__len__() == 0): return None
    logp("Saving dataset or dataset snapshot named: " + subDatasetName + " ...", anyMode=True)
    dsName = subDatasetName + "-" + _RndName
    dsOrthographicallySimilars: WordSimDataset = WordSimDataset(dsName, scale=scale)
    dsOrthographicallySimilars.LoadWithWordPairs(wordpairs)
    fpath = str(Path(StudyPathForLanguage()).joinpath(f'{dsName}.csv'))
    dsOrthographicallySimilars.Persist(fpath)
    logp("Saved snapshot: " + fpath + "(" + str(len(wordpairs)) + ")", anyMode=True)
    return fpath

def StudyPathForLanguage():
    return Path(GetStudyPath()).joinpath(_Context.Language.Code.lower())

def SetContext(lcontext: LinguisticContext):
    """
    Aims to set the context before accessing the paper's setup.
    :param lcontext:
    :return:
    """
    global _Context
    _Context = lcontext

#endregion

def S2_GenerateOrthographicallySimilarWordPairsExhaustive(wordpool: List[str], orthographicSim: IWordSimilarity, outputName3: str = None, outputName4: str = None,
                                                   minOrthographicSimQ4: float = 0.75, minOrthographicSimQ3: float = 0.5,
                                                   limitResults: int = None, resumeStage2: str = None,
                                                   snapshotPersistenceDetectedBatch: int = None, snapshotPersistenceBatchPercentage: int = 10,
                                                   snapshotCallback=None, tryLoadStage2SessionCallback=None, snapshotFinalScale: DiscreteScale = None) -> Tuple[List[WordPair], List[WordPair], int]:
    """
    Always perform the cheaper task first.
    :param snapshotPersistenceBatchPercentage: Specifies at which percentage intervals a snapshot will be taken.
    :param wordSource:
    :param orthographicSim:
    :param snapshotPersistenceBatch: Saves a snapshot of extracted pairs after the specified number of detections. Must be between 0-100.
    :return:
    """
    # Validate
    if (minOrthographicSimQ4 == 0 or minOrthographicSimQ3 == 0): raise Exception("Orthographic similarity thresholds cannot be 0.")
    if (minOrthographicSimQ4 is None or minOrthographicSimQ3 is None): raise Exception("Orthographic similarity thresholds cannot be None.")
    if (minOrthographicSimQ3 >= minOrthographicSimQ4): raise Exception("Q3 cannot be greater than Q4.")
    if (not outputName4 or not outputName3): raise Exception("Output names are not provided.")
    oSimName: str = str(orthographicSim)
    logp("Going to use '" + oSimName + "' as the orthographic similarity algorithm!")

    wpOrthographicallySimilarsQ3: List[WordPair] = []
    wpOrthographicallySimilarsQ4: List[WordPair] = []

    # region Resume Mode
    startingChar: str = None
    reachedToLastSession: bool = None
    if (resumeStage2):
        ds4 = tryLoadStage2SessionCallback(outputName4, resumeStage2)
        ds3 = tryLoadStage2SessionCallback(outputName3, resumeStage2)
        lastWordProcessed = ds3.Wordpairs[ds3.Wordpairs.__len__() - 1].Word1  # Continue always from Q3.
        lastCharProccesed = lastWordProcessed[0]
        startingChar: str = _Context.Grammar.ToLowerCase(lastCharProccesed)
        logp("In the previous session, we stopped at the character '" + lastCharProccesed + "', and will continue from the beginning of the character '" + startingChar + "'...")
        reachedToLastSession: bool = False
        wpOrthographicallySimilarsQ3 = ds3.Wordpairs
        wpOrthographicallySimilarsQ4 = ds4.Wordpairs

        # Delete latest pairs - leftovers to avoid possible duplicates - assumes ordered list, otherwise it takes too long.
        logl(str(wpOrthographicallySimilarsQ4.__len__()), "Q4.Items", anyMode=True)
        logp("Deleting word pairs for the last remaining characters to avoid duplicates...", anyMode=True)
        for wp in wpOrthographicallySimilarsQ4:
            if (wp.Word1[0] == startingChar):  # Assumes order! Deletes automatically after finding the first character.
                index4 = wpOrthographicallySimilarsQ4.index(wp)
                wpOrthographicallySimilarsQ4 = wpOrthographicallySimilarsQ4[0:index4]
                break
        logl(str(wpOrthographicallySimilarsQ4.__len__()), "Q4.Items", anyMode=True)
        logl(str(wpOrthographicallySimilarsQ3.__len__()), "Q3.Items", anyMode=True)
        for wp in wpOrthographicallySimilarsQ3:
            if (wp.Word1[0] == startingChar):  # Same assumption of order for Q3.
                index3 = wpOrthographicallySimilarsQ3.index(wp)
                wpOrthographicallySimilarsQ3 = wpOrthographicallySimilarsQ3[0:index3]
                break
        logl(str(wpOrthographicallySimilarsQ3.__len__()), "Q3.Items", anyMode=True)
        logp("Deletion process completed.", anyMode=True)
        snapshotCallback(wpOrthographicallySimilarsQ3, outputName3, snapshotFinalScale)  # Save again with a new ID after loading.
        snapshotCallback(wpOrthographicallySimilarsQ4, outputName4, snapshotFinalScale)
    #endregion

    wpSynthesizer = WordPairSynthesizer().GeneratePossibleWordPairs(wordpool, allowSameWordsInAPair=False)

    i: int = 1
    estsize: int = int(NoDecimal((len(wordpool) * (len(wordpool) / 2))))  # Complexity: (n*n/2)
    prog = Progressor(reportRemaniningTime=True, expectedIteration=estsize)
    progBatchSize = 10 if estsize < 10000 else int(estsize / 10000)
    wpCursor = None

    def saveInSeperateThread(wps, name, scale):
        """
        #ref:http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/
        :param wps:
        :param name:
        :return:
        """
        thread = threading.Thread(target=snapshotCallback, args=(wps, name, scale))
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    firstChar: str = None
    for wp in wpSynthesizer:
        firstChar = wp.Word1[0]
        perc: float = prog.logpif(i, progressBatchSize=progBatchSize, anyMode=True, iterstr="iter-" + firstChar)

        # region resume check
        if (reachedToLastSession == False):
            if (firstChar == startingChar):  # Skipping until reaching the stopped character; skipping is 10x faster than similarity calculation.
                reachedToLastSession = True
            else:
                i = i + 1
                continue
        #endregion

        # Do the job
        try:
            sim = orthographicSim.WordSimilarity(wp.Word1, wp.Word2)  # Without this cost, generating all possibilities for EN takes only 36 minutes. 95% of time is spent on this operation!
        except Exception as e:
            print("Error in osim operation! Alg:" + str(orthographicSim) + ", wp:" + wp.ToPairDisplay())
            print(e)
            raise

        if (sim >= minOrthographicSimQ3):  # Ignore if smaller than both thresholds.
            wp.SetOtherSimilarity(oSimName, sim)
            wpCursor = wpOrthographicallySimilarsQ4 if sim >= minOrthographicSimQ4 else wpOrthographicallySimilarsQ3
            wpCursor.append(wp)
            extracted: int = len(wpCursor)
            logpif(iter=len(wpCursor), iterstr="Detected", progressBatchSize=100, anyMode=True)  # Log every 100 detections.
            if (limitResults):
                if (extracted >= limitResults):
                    return wpOrthographicallySimilarsQ3, wpOrthographicallySimilarsQ4, i - 1

            # Snapshot by detected (disabled by default)
            if (snapshotPersistenceDetectedBatch):  # Save snapshot after specified detections.
                if (extracted % snapshotPersistenceDetectedBatch == 0):
                    saveInSeperateThread(wpOrthographicallySimilarsQ3, outputName3, snapshotFinalScale)
                    saveInSeperateThread(wpOrthographicallySimilarsQ4, outputName4, snapshotFinalScale)

        # Snapshot by percentage
        if (snapshotPersistenceBatchPercentage and perc):
            if ((perc % snapshotPersistenceBatchPercentage == 0)):  # Only at whole percentage points.
                saveInSeperateThread(wpOrthographicallySimilarsQ3, outputName3, snapshotFinalScale)
                saveInSeperateThread(wpOrthographicallySimilarsQ4, outputName4, snapshotFinalScale)

        i = i + 1
    return wpOrthographicallySimilarsQ3, wpOrthographicallySimilarsQ4, i - 1


# noinspection PyUnresolvedReferences
# @with_goto
def S3_Run(orthographicallySimilarWpsPathQ4: str = None, autoPersist: bool = True, posFilters: List[POSTypes] = [POSTypes.NOUN], includeQ3: bool = True,
           orthographicallySimilarsWithRelatednessPathQ4=None, maxRelatedness: float = 0.25, skip: str = ""):
    """
    Executes the steps of Stage4-Morphological Relatedness Filtering.
    :param orthographicallySimilarWpsPathQ4:
    :param autoPersist:
    :param posFilters:
    :param includeQ3:
    :param orthographicallySimilarsWithRelatednessPathQ4: If provided, skips to 4a and starts there.
    :param maxRelatedness:
    :param skip: Indicates the subprocesses to be skipped.
    :return:
    """
    # region Commons
    dsOrthographicallySimilarsQ4 = None
    dsOrthographicallySimilarsQ3 = None
    finalScale = DiscreteScale(0, 1)
    log("S3: Starting Stage3 Relatedness Filtering...", anyMode=True)
    wnSimAlgorithm: WordNetSimilarityAlgorithms = Provider.CreateWordNetSimAlgorithm()
    wnSimName: str = "Wn_" + str(wnSimAlgorithm.name).lower()
    logl(wnSimName, "CreateWordNetSimAlgorithm")
    log("S3: Creating WordNet similarity for the language...")
    wordnetSim: IWordSimilarity = Provider.CreateWordNetForSimilarity(wnSimAlgorithm, wordSimPOSFilters=posFilters)
    logl(str(wordnetSim), "WordNetSim Type", anyMode=True)
    logp("S3: Calculating WordNet relatedness values for WordPairs...", anyMode=True)
    if skip is None: skip = ""
    # endregion

    if orthographicallySimilarsWithRelatednessPathQ4 is not None:
        raise NotImplemented("Skipping to 4a is not implemented yet!")
        # goto .Stage3a

    # region Load
    logp("S3: Loading", anyMode=True)
    if not orthographicallySimilarWpsPathQ4: raise Exception("orthographicallySimilarWpsPathQ4 is null!")
    orthographicallySimilarWpsPathQ3: str = orthographicallySimilarWpsPathQ4.replace("SimilarsQ4", "SimilarsQ3")
    dsOrthographicallySimilarsQ3: WordSimDataset = None

    # Q4
    if orthographicallySimilarWpsPathQ4:
        dsOrthographicallySimilarsQ4 = WordSimDataset(fullPath=orthographicallySimilarWpsPathQ4, linguisticContext=_Context)
        dsOrthographicallySimilarsQ4.Load()
    # Q3
    if includeQ3:
        dsOrthographicallySimilarsQ3 = WordSimDataset(fullPath=orthographicallySimilarWpsPathQ3, linguisticContext=_Context)
        dsOrthographicallySimilarsQ3.Load()
    # endregion

    def setWordNetSimilarities(wn, ds, s2ExistingPath: str, allowNoneSims: bool = False) -> Tuple[str, str]:
        """
        Adds WordNet similarity scores to the original dataset and saves it if necessary.
        :param wn:
        :param ds:
        :param allowNoneSims: In the OSimUnr usage, since the word pool is selected from WordNet, in theory, every word should have a similarity score. If True, the process continues even if None; if False, an error is raised.
        :param existingPath: Output of the S2 process without WordNet scores.
        :return: Returns the name and physical path of the new S3 dataset.
        """
        logp("Setting WordNet similarities for " + s2ExistingPath + " ...", anyMode=True)
        scoreScale = wn.SimilarityScale()
        wnEff: IWordSimilarity = None  # Can be wrapped for normalization purposes if needed.
        if not scoreScale.IsNormalized():
            wnEff = WordSimilarityNormalizerWrapper(wn, ds.Wordpairs, finalScale)
        else:
            wnEff = wn

        wpIndex: int = 0
        for wp in ds.Wordpairs:
            sim = wnEff.WordSimilarityInScale(wp.Word1, wp.Word2, finalScale)
            if sim is None and not allowNoneSims:
                raise Exception("OSim result is 'None'. Cannot proceed without enabling allowNoneSims mode. OSimUnr does not accept None TSim." + str(wp))
            ds.Wordpairs[wpIndex].SetOtherSimilarity(wnSimName, sim)
            wpIndex += 1

        if autoPersist:
            head, tail = os.path.split(s2ExistingPath)
            newSubDatasetName = tail.replace("S2", "S3").replace("OrthographicallySimilars", "OrthographicallySimilarsWithWN")
            newSubDatasetName = newSubDatasetName[0:-10]  # Replace extension and stuff
            savedPath: str = snapshotSave(ds.Wordpairs, newSubDatasetName, finalScale)
            return newSubDatasetName, savedPath

    newS3DatasetNameQ4, newS3DatasetPathQ4 = setWordNetSimilarities(wordnetSim, dsOrthographicallySimilarsQ4, orthographicallySimilarWpsPathQ4)
    if orthographicallySimilarsWithRelatednessPathQ4 is None:
        orthographicallySimilarsWithRelatednessPathQ4 = newS3DatasetPathQ4

    if includeQ3:
        newS3DatasetNameQ3, newS3DatasetPathQ3 = setWordNetSimilarities(wordnetSim, dsOrthographicallySimilarsQ3, orthographicallySimilarWpsPathQ3)

    # region 3a - Relatedness Filtering
    # label .Stage3a
    if dsOrthographicallySimilarsQ4 is None:
        dsOrthographicallySimilarsQ4 = WordSimDataset(fullPath=orthographicallySimilarsWithRelatednessPathQ4, linguisticContext=_Context)
        dsOrthographicallySimilarsQ4.Load()
    if includeQ3:
        orthographicallySimilarsWithRelatednessPathQ3: str = orthographicallySimilarsWithRelatednessPathQ4.replace("SimilarsWithWNQ4", "SimilarsWithWNQ3")
        dsOrthographicallySimilarsQ3 = WordSimDataset(fullPath=orthographicallySimilarsWithRelatednessPathQ3, linguisticContext=_Context)
        dsOrthographicallySimilarsQ3.Load()

    # Initialize Root Detection Tools
    logp("Initializing root detection dependencies...", anyMode=True)
    rootDetector: IRootDetector = Provider.CreateRootDetector()  # Will cache it because I want to use the same ML instance!
    fastRootDetector: IRootDetector = Provider.CreateFastRootDetector()  # No need to cache for the fast one; it's already dictionary-based!
    sharingRootDetector = SharingRootDetector(rootDetector, useOutOfLexiconRoots=True)
    wnDerRel: IWordRelatednessBinaryClassifier = Provider.CreateDerivationallyRelatedClassifier()
    priorPOS: POSTypes = posFilters[0] if posFilters.__len__() == 1 else None  # If it's a single POS filter experiment, conveying the POS info can increase success.

    # Initialize D-stage Definition-based classifiers
    logp("Initializing definition-based filtering dependencies...", anyMode=True)
    defClassifier: DefinitionBasedRelatednessClassifier = Provider.CreateDefinitionBasedRelatednessClassifier(priorPOS, rootDetector, fastRootDetector)
    defClassifier.SkipReferencing = skip.__contains__("3A4")
    defClassifier.SkipKeywordInTypeHierarchy = skip.__contains__("3A3")
    defClassifier.SkipMutualMeaningfulAffixes = skip.__contains__("3C3")  # Not 3A5!
    blacklistedFilterer: BlacklistedConceptsWordNetRelatednessFilterer = Provider.CreateBlacklistedConceptsFilterer(priorPOS)
    conceptFilterer: ConceptWiseWordNetRelatednessFilterer = Provider.CreateConceptPairFilterer(priorPOS)

    def detectUnrelateds(wordpairs, existingS3Path: str):
        logp("detectUnrelateds...", anyMode=True)
        if not rootDetector: logp("Gloss-based relatedness filter will not be applied as RootDetector is missing!!")

        unrelateds: List[WordPair] = []
        eliminateds: List[WordPair] = []  # Related pairs eliminated during filtering.
        if existingS3Path is not None:
            logp("S3a Relatedness Filtering is about to begin for " + existingS3Path + " ...", anyMode=True)
        else:
            logp("existingS3Path is null. Operation terminated.", anyMode=True)
            exit()

        prog = Progressor(expectedIteration=wordpairs.Wordpairs.__len__())
        batchSize: int = int(wordpairs.Wordpairs.__len__() / 100)
        i = 0
        for wp in wordpairs.Wordpairs:
            wp.Reason: str = None
            wp.SharedRoot = ""
            prog.logpif(i, "wp", progressBatchSize=batchSize, anyMode=True)
            isUnrelated: bool = True  # Default assumption is unrelated. Ask the stages until a related judgment is made.

            # Stage 3A1: WordNet Relatedness
            if isUnrelated and not skip.__contains__("3A1"):
                sim: float = wp.GetOtherSimilarity(wnSimName)
                if sim:
                    isUnrelated = sim <= maxRelatedness

            # Additional filtering stages...

            # Finalize
            if wp.Reason is not None:
                wp.Note = wp.Reason
                if wp.SharedRoot: wp.Note = wp.Note + ". Root:" + wp.SharedRoot
            if isUnrelated:
                unrelateds.append(wp)
            else:
                eliminateds.append(wp)
            i += 1

        if autoPersist:
            head, tail = os.path.split(existingS3Path)
            newSubDatasetName = tail.replace("S3", "S3a").replace("OrthographicallySimilarsWithWN", "OrthographicallySimilarButUnrelateds")
            snapshotSave(unrelateds, newSubDatasetName[0:-10], finalScale)
            newRootSubDatasetName = tail.replace("S3", "S3a").replace("OrthographicallySimilarsWithWN", "OrthographicallySimilarAndSharingRoots")
            snapshotSave(eliminateds, newRootSubDatasetName[0:-10], finalScale)
        logp("Relatedness filtering ended.", anyMode=True)

    detectUnrelateds(dsOrthographicallySimilarsQ4, orthographicallySimilarsWithRelatednessPathQ4)

    if includeQ3:
        pathQ3: str = orthographicallySimilarsWithRelatednessPathQ4.replace("SimilarsWithWNQ4", "SimilarsWithWNQ3")
        detectUnrelateds(dsOrthographicallySimilarsQ3, pathQ3)

    logp(_StudyName + " S3a process completed.", anyMode=True)


def RunStudy(wordPosFilters: List[POSTypes] = None, preExtractedWordPairsPath=None, wordpoolPath=None, wordpairLimit: int = None, autoPersist=True, limitWordCands: int = None,
             wordpairsPath: str = None, minOrthographicSimQ4: float = None, minOrthographicSimQ3: float = None, orthographicSim: IWordSimilarity = None, resumeStage2: str = None, s1Only: bool = False,
             allowAccentDuplicates: bool = True, resumeStage3and4: bool = True, maxRelatedness: float = 0.25):
    """
    :param resumeStage2: If the session ID of a previously incomplete stage2 is provided, it continues from there. If None, it calculates a new session from scratch. Default: None
    :param wordPosFilters: If None, all words found are used. If filters are provided, only those POS words are included in the pipeline at the wordpool level.
    :param preExtractedWordPairsPath:
    :param wordpoolPath:
    :param wordpairLimit:
    :param autoPersist:
    :param limitWordCands:
    :param wordpairsPath:
    :param minOrthographicSimQ4:
    :param minOrthographicSimQ3:
    :param allowAccentDuplicates: If True, allows matches like "harekât-harekat". If False, keeps the accented version and removes unaccented matches.
    :return:
    """
    finalScale = DiscreteScale(0, 1)
    _MaxRelatedness = maxRelatedness

    # General Warnings
    if (wordPosFilters is None): logp("No POS Filter defined for the entire pipeline! Are you sure? Ignore this if you are using an existing pool file!")

    def tryLoadStage2Session(subDatasetName: str, sessionId: str) -> WordSimDataset:
        logp("Loading dataset or dataset snapshot named: " + subDatasetName + " ...", anyMode=True)
        logp("For session: " + sessionId)
        dsName = subDatasetName + "-" + sessionId
        fpath = str(Path(StudyPathForLanguage().joinpath(f'{dsName}.csv')))
        dsOrthographicallySimilars: WordSimDataset = WordSimDataset(fullPath=fpath, linguisticContext=_Context)
        WordSimDataset.Load(dsOrthographicallySimilars, autoLowerCase=False)
        logp("Loaded snapshot: " + fpath + "(" + str(len(dsOrthographicallySimilars.Wordpairs)) + ")", anyMode=True)
        return dsOrthographicallySimilars

    def saveWordpool(wordpool, filePath):
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        with open(filePath, 'w', encoding="utf-8-sig") as f:
            for w in wordpool:
                f.write("%s\n" % w)
        logp("Wordpool saved. " + filePath)
    # endregion

    # region S1-S2: CANDIDATE SELECTION
    dsOrthographicallySimilars: WordSimDataset = None
    if (wordpairsPath):
        dsOrthographicallySimilars = WordSimDataset(fullPath=wordpairsPath, linguisticContext=_Context)
        dsOrthographicallySimilars.Load()
    else:
        if (preExtractedWordPairsPath):
            dsOrthographicallySimilars = WordSimDataset(preExtractedWordPairsPath)
            dsOrthographicallySimilars.Load()
        else:
            # 1.2: Load Wordpool from existing
            wordpool = []
            sortedWordpool: List = None
            if (wordpoolPath):
                with open(wordpoolPath, encoding="utf-8") as file:
                    for w in file:
                        wordpool.append(w.strip())
                log("Wordpool loaded. Size:" + str(len(wordpool)), anyMode=True)
                log(wordpoolPath)
                sortedWordpool = sorted(wordpool)
            else:
                # region S1.2: Prepare WordPool
                # InitialWordPool: Since Word definition only fetches single words, the raw state cannot be retrieved from here.
                wordsource: IWordSource = Provider.GetWordSource()

                # Single WordPool
                singleWordpool: Set[str] = wordsource.GetWords(posFilter=None)
                logp("S1-SingleWordPoolSize: " + str(len(singleWordpool)))
                saveWordpool(singleWordpool, str(Path(StudyPathForLanguage().joinpath(f'S1-SingleWordPool-{_RndName}.txt'))))

                # S1-POS Filtering
                if (wordPosFilters is None or wordPosFilters.__len__() == 0):
                    wordpoolAllPos = singleWordpool
                else:
                    wordpoolAllPos = set()
                    for pos in wordPosFilters:
                        wordpoolForPos: Set[str] = wordsource.GetWords(pos)
                        logp("S1-" + str(pos.name) + "-WordPoolSize: " + str(len(wordpoolForPos)))
                        saveWordpool(sorted(wordpoolForPos), str(Path(StudyPathForLanguage(),f'S1-{pos.name}-WordPool-{_RndName}.txt')))
                        wordpoolAllPos = wordpoolAllPos.union(wordpoolForPos)

                # Make all distinct and lowercase
                wordpoolAllPos2: Set[str] = set()
                for wordRaw in wordpoolAllPos:
                    wordpoolAllPos2.add(_Context.Grammar.ToLowerCase(wordRaw))
                logp("S1-POSFilteredWordPoolSize: " + str(len(wordpoolAllPos2)))
                saveWordpool(wordpoolAllPos2, str(Path(StudyPathForLanguage(),f'S1-POSFilteredWordPool-{_RndName}.txt')))

                # Filter
                logp("Applying WordFilter for " + str(len(wordpoolAllPos2)) + " ...")
                logp("Following word filters are hardcoded: minLength=6, allowPunctuation=False, allowNumbers=False")
                wordpoolFinal, removed = WordsFilterer().ToFiltered(wordpoolAllPos2, minLength=6, allowPunctuation=False, allowNumbers=False)
                logp(str(len(wordpoolFinal)) + " words left after filtering. Removed: " + str(removed))
                logp("S1-LengthAndPunctFilteredWordPool: " + str(len(wordpoolFinal)))
                saveWordpool(wordpoolFinal, str(Path(StudyPathForLanguage()).joinpath(f'S1-LengthAndPunctFilteredWordPool-{_RndName}.txt')))

                # region AccentedDuplicates
                # This process filters out non-accented versions of words with accents. Disabled by default.
                if (not allowAccentDuplicates):
                    wordpoolFinalAccentSafe: Set[str] = set(wordpoolFinal)  # Clone to a new set.
                    accentedCount: int = 0
                    for w in wordpoolFinal:
                        if (_Context.Grammar.HasAccent(w)):
                            wReduced: str = _Context.Grammar.ReduceAccents(w)
                            wordpoolFinalAccentSafe.discard(wReduced)
                            accentedCount = accentedCount + 1
                    logp(str(accentedCount) + " words were found with accents. Possible reduced versions have been removed.")
                    saveWordpool(wordpoolFinalAccentSafe, str(Path(StudyPathForLanguage()).joinpath(f'S1-FinalAccentSafe-{_RndName}.txt')))  # Unsorted
                    wordpoolFinal = wordpoolFinalAccentSafe
                # endregion

                # Persist
                if (limitWordCands): wordpoolFinal = wordpoolFinal[:limitWordCands]
                sortedWordpool = sorted(wordpoolFinal)
                saveWordpool(sortedWordpool, str(Path(StudyPathForLanguage()).joinpath(f'S1-FinalWordPool-{_RndName}.txt')))
                # endregion

            # 2: GENERATE WORDPAIRS
            if (s1Only):
                log("S1 completed. Exiting due to S1Only mode!", anyMode=True)
                exit()
            log("Starting Stage2...", anyMode=True)
            if (not orthographicSim): raise Exception("No OrthographicSim defined. Cannot continue to Stage2!")
            oSimName: str = str(orthographicSim).lower()
            logl(oSimName, "oSimAlg", anyMode=True)
            outputName3: str = "S2-OrthographicallySimilarsQ3-" + oSimName
            outputName4: str = "S2-OrthographicallySimilarsQ4-" + oSimName
            orthographicallySimilarQ3, orthographicallySimilarQ4, totalSpace = S2_GenerateOrthographicallySimilarWordPairsExhaustive(
                wordpool=sortedWordpool,
                orthographicSim=orthographicSim, minOrthographicSimQ3=minOrthographicSimQ3, minOrthographicSimQ4=minOrthographicSimQ4, limitResults=wordpairLimit,
                snapshotPersistenceDetectedBatch=None if autoPersist else None,
                snapshotPersistenceBatchPercentage=4 if autoPersist else None,
                snapshotCallback=snapshotSave, outputName3=outputName3, outputName4=outputName4,
                tryLoadStage2SessionCallback=tryLoadStage2Session, resumeStage2=resumeStage2, snapshotFinalScale=finalScale)
            print("totalSpace: " + str(totalSpace))

            # Save as WordSim Dataset
            if (autoPersist):
                pathQ3: Optional[str] = snapshotSave(orthographicallySimilarQ3, outputName3, finalScale)
                pathQ4: Optional[str] = snapshotSave(orthographicallySimilarQ4, outputName4, finalScale)

                # Resume Stage 3 and 4
                if (resumeStage3and4):
                    S3_Run(posFilters=wordPosFilters, orthographicallySimilarWpsPathQ4=pathQ4, autoPersist=autoPersist,
                           maxRelatedness=_MaxRelatedness)
            else:
                raise Exception("AutoPersist is disabled. Cannot continue to Stage 3 without saving the results.")
    # endregion
    logp("Process completed for " + _StudyName, anyMode=True)

def GenerateDataset(wordpoolPath: str = None, wordpairsPath: str = None,
          resume: str = None, s1Only: bool = False, limitWordCands: int = None, minOrthographicSimQ4:float=None, minOrthographicSimQ3:float=None,
          wordPosFilters:List[POSTypes]=None, resumeStage3and4=True, maxRelatedness:float = 0.25):

    if wordPosFilters is None:
        wordPosFilters = []

    oSimAlg = Provider.GetOrthographicSimilarityAlgorithm()

    RunStudy(
        wordPosFilters=wordPosFilters, limitWordCands=limitWordCands, minOrthographicSimQ3=minOrthographicSimQ3, minOrthographicSimQ4=minOrthographicSimQ4,
        orthographicSim=oSimAlg,
        wordpoolPath=wordpoolPath,
        wordpairsPath=wordpairsPath, wordpairLimit=None,
        resumeStage2=resume, s1Only=s1Only, resumeStage3and4=resumeStage3and4, maxRelatedness=maxRelatedness
    )
