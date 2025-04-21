# coding=utf-8
import pprint
import unittest
import warnings
from builtins import NotImplementedError
from statistics import mean
from typing import Optional, List, Set
from unittest import TestCase

from nltk.corpus.reader import Synset, Lemma
from pandas import DataFrame
from tabulate import tabulate

from src.Core.Dataset.DiscreteScale import DiscreteScale
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.IRootDetector import IRootDetector
from src.Core.WordNet.IWordDefinitionSource import IWordDefinitionSource
from src.Core.WordNet.IWordNet import IWordNet, IWordNetMeasures, WordNetSimilarityAlgorithms, Lemma2SynsetMatching
from src.Core.WordNet.IWordTaxonomy import RelationUsage, URelations, Directions, TaxonomyType, SenseStrategy
from src.Core.WordPair import WordPair
from src.Core.WordPairSynthesizer import WordPairSynthesizer
from src.Tools import FormatHelper
from src.Tools.Logger import logp, logv, logpif


#NLTK local data folder: %APPDATA%\nltk_data\corpora\wordnet
#Make sure to download first
    #import nltk
    #nltk.download('wordnet')


class NLTKWordNetWrapper(IWordNet,IWordNetMeasures, IRootDetector, IWordDefinitionSource):

    def __init__(self, algorithm:WordNetSimilarityAlgorithms = WordNetSimilarityAlgorithms.WUP, l2s:Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations,
                 wordSimPOSFilters:List[POSTypes] = None) -> None:
        """
        :param algorithm:
        :param l2s:
        :param wordSimPOSFilters: POS Filters to be applied when a WordSim function is observed according to the IWordSimilarity interface (_RunSimilarity etc.).
        """
        # Pay attention to the order!! Normally, the IWordNetMeasure base is called twice. To prevent this, I removed the default super() calls in the bases. As far as I understand, this is normal. The best explanation I found is here: #https://stackoverflow.com/questions/29311504/multiple-inheritance-with-arguments
        IWordNet.__init__(self)
        IWordNetMeasures.__init__(self,algorithm,l2s)
        self._InformationContent = None
        self.WordSimPOSFilters:List[POSTypes] = wordSimPOSFilters
        if(self.WordSimPOSFilters is None): logp("WordSimPOSFilters is None!")
        logp("NLTKWordNet instance has been created. Potential member calls could take a while for once if it's the first nltk.wn call!")

    def HasSynset(self, synsetName) -> bool:
        from nltk.corpus.reader import WordNetError     # Takes time.
        try:
            from nltk.corpus import wordnet as wn       # Import takes time!
            x = wn.synset(synsetName)
            return True
        except(WordNetError):
            return False

    def GetAllLemmas(self,singleWordsOnly:bool = False, posFilters:List[POSTypes] = None)->Set[Lemma]:
        lemmaset:Set[Lemma] = set()
        if(posFilters is None or len(posFilters) == 0):
            logp("Reading all words from WordNet...")
            keyiterator = self._LoadAllLemmas(posFilter=None)
            self._FillSetFromKyeIterator(keyiterator,lemmaset,singleWordsOnly)
        else:
            logp("Reading all " + str(posFilters) + " words from WordNet...")
            for posFilter in posFilters:
                poschar:str = self._GetPosChar(posFilter)
                keyiterator = self._LoadAllLemmas(posFilter=poschar)
                self._FillSetFromKyeIterator(keyiterator,lemmaset,singleWordsOnly)
        return lemmaset

    def _FillSetFromKyeIterator(self, keyiterator, lemmaset, singleWordsOnly:bool = False):
        for s in keyiterator:
            if (singleWordsOnly):
                if (not str(s).__contains__("_")):      # Like dog_house
                    lemmaset.add(s)
            else:
                lemmaset.add(s)

    def LoadSynsets(self, lemma: str, posFilters:List[POSTypes] = None, lang="eng") -> List[Synset]:
        """
        Provides the ability to filter by more than one POS at the same time.
        :param lemma:
        :param posFilters:
        :param lang:
        :return:
        """
        from nltk.corpus import wordnet as wn

        if(posFilters is None or len(posFilters) == 0):
            return wn.synsets(lemma,None,lang)
        elif(len(posFilters) == 1):
            return wn.synsets(lemma, self._GetPosChar(posFilters[0]) ,lang)
        else:
            syns:List[Synset] = []
            distinctNames:Set[str] = set()
            for pos in posFilters:
                pchar = self._GetPosChar(pos)
                logv("Fetching synset: '" + lemma+"."+pchar + "'")
                _syns:List[Synset] = wn.synsets(lemma, pchar,lang)
                for _syn in _syns:
                    _name = _syn._name
                    if(not _name in distinctNames):     # Ensuring all synsets are distinct by their unique 'synset._name'
                        distinctNames.add(_name)
                        syns.append(_syn)
            return syns

    def LoadSynset(self, lemma:str, pos:POSTypes = None, senseOrder: int = 1)->Synset:
        """
        Provides access according to sense order for a single POS.
        :param lemma:
        :param pos:
        :param senseOrder:
        :return:
        """
        from nltk.corpus import wordnet as wn
        name:str = self._BuildSynsetName(lemma,pos,senseOrder)
        return wn.synset(name)

    def LoadSynsetByName(self, synsetName:str):
        from nltk.corpus import wordnet as wn
        return wn.synset(synsetName)

    def _BuildSynsetName(self, lemma:str, pos:POSTypes = None, senseOrder: int = 1)->str:
        return lemma + "." + self._GetPosChar(pos) + "." + str(senseOrder).zfill(2)

    def GetDerivationallyRelatedForms(self, lemma:Lemma)->List[Lemma]:
        return lemma.derivationally_related_forms()

    def LoadLemmas(self, word: str, pos:POSTypes=None, lang: str = "eng")->List[Lemma]:
        from nltk.corpus import wordnet as wn
        lemmas = wn.lemmas(word,self._GetPosChar(pos),lang)
        return lemmas

    #region Internal

    def _LoadAllLemmas(self, posFilter:str = None):     # TODO: The Lang 'eng' is constant for now! Pass the 'lang' for future use.
        from nltk.corpus import wordnet as wn           # Import takes time!
        return wn.all_lemma_names(lang='eng',pos=posFilter)

    def _GetPosChar(self, posType:POSTypes)->Optional[str]:
        """
        ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'     (ref:https://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html)
        :param posType:
        :return:
        """
        if (posType is None): return None
        if (posType == POSTypes.NOUN):
            return 'n'
        elif(posType == POSTypes.VERB):
            return "v"
        elif(posType == POSTypes.ADJ):
            return 'a'
        elif(posType == POSTypes.ADV):
            return 'r'
        else:
            raise NotImplementedError(posType)      # I didn't differentiate ADJ_SAT in my types.

    def _GetAllSynsets(self):
        from nltk.corpus import wordnet as wn       # Import takes time!
        return wn.all_synsets()

    def _GetAllUnrelatedLemmas(self):
        #1. Avoid looking at pairs within the same synset.
        #2. Take those with fewer senses.
        #3. Eliminate paired_words.
        synsets =self._GetAllSynsets()
        #print("synsets#" + str(len(synsets)))
        eliminatedPairs = set()

        wpSynthesizer = WordPairSynthesizer()

        s:int = 1
        for syn in synsets:
            #s:Synset
            #print(str(syn) + "\n")
            #print(syn.definition())

            # Eliminate synonyms(lemmas in the same synset)
            lemmas = syn.lemmas()
            #print("lemmas: " + str(len(lemmas)))
            if(len(lemmas) <= 1):
                s += 1
                continue
            lemmaPairGen = wpSynthesizer.GeneratePossibleWordPairs(lemmas,False,False)
            for lemmaPair in lemmaPairGen:
                wpCode = WordPair.ToOrderFreeUniqueStr(lemmaPair.Word1._name, lemmaPair.Word2._name)
                eliminatedPairs.add(wpCode)
            s += 1
            logpif(s,"synset",progressBatchSize=1000)
            logpif(len(eliminatedPairs),"eliminted wps",progressBatchSize=1000)

        # Report
        print("nr of eliminated wordpairs: " + str(len(eliminatedPairs)))

    #endregion

    #region Similarity Impl

    def _RunSimilarityImpl(self, methodName, w1:str, w2:str, l2s:Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations,informationContent = None)->Optional[float]:
        if(l2s != Lemma2SynsetMatching.UseFirstSense): return self._RunSimilarityImplMultipseSenses(methodName,w1,w2,l2s,informationContent)

        # Validate
        if(self.WordSimPOSFilters is None or len(self.WordSimPOSFilters) == 0): raise Exception("Cannot run in UseFirstSense mode while no posfilters defined. You must provide a single POSFilter to get the first sense of that POS!")
        if(len(self.WordSimPOSFilters) >1 ): raise Exception("Cannot run UseFirstSense while multiple posFilter defined. Please pass only one posFilter instead of " + str(self.WordSimPOSFilters))
        from nltk.corpus import wordnet as wn       # Import takes time!

        w1synName = w1+"." + self._GetPosChar(self.WordSimPOSFilters[0]) + ".01"        # First sense assumption!
        w2synName = w2+"." + self._GetPosChar(self.WordSimPOSFilters[0]) + ".01"
        if (not self.HasSynset(w1synName)): return None
        if (not self.HasSynset(w2synName)): return None
        syn1 = wn.synset(w1synName)
        m = getattr(syn1, methodName)
        try:
            sim = m(wn.synset(w2synName),l2s, informationContent)       # simulate_root=True by default
        except Exception as ex:
            sim = None
            print(ex)
        return sim

    def _RunSimilarityImplMultipseSenses(self, methodName, w1:str, w2:str, l2s:Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations,informationContent = None)->Optional[float]:
        """
        Calculates sim for every pair of senses and returns a single value according to the given aggr. parameter.
        :param methodName:
        :param w1:
        :param w2:
        :param l2s: Highest method works much better. I found values similar to what everyone reports ~75 with MC dataset. Average and First had low scores around 60-65.
        :param informationContent:
        :return:
        """
        from nltk.corpus import wordnet as wn       # Import takes time!

        # Getting all senses
        syns1 = self.LoadSynsets(w1, posFilters=self.WordSimPOSFilters)        # Case doesn't matter in this query!
        syns2 = self.LoadSynsets(w2, posFilters=self.WordSimPOSFilters)
        if len(syns1) == 0: return None
        if len(syns2) == 0: return None

        scores:List[float] = []
        for syn1 in syns1:
            for syn2 in syns2:
                m = getattr(syn1,methodName)
                try:        # Measures can throw errors.
                    sim = m(wn.synset(syn2._name), informationContent)          # Could yield None on cross-POS situations.
                except Exception as ex:
                    sim = None
                    print(ex)
                if(sim is not None): scores.append(sim)

        if(len(scores) == 0): return None

        # Aggregates
        if(l2s == Lemma2SynsetMatching.HighestScoreOfCombinations):
            return max(scores)
        elif(l2s == Lemma2SynsetMatching.AverageScoreOfCombinations):
            return mean(scores)
        raise Exception("Unsupported: " + str(l2s))

    def SimilarityScale(self) -> DiscreteScale:
        if(self.Algorithm == WordNetSimilarityAlgorithms.LCH
                or  self.Algorithm == WordNetSimilarityAlgorithms.JCN
                or  self.Algorithm == WordNetSimilarityAlgorithms.RES
        ): return DiscreteScale(0,None)
        return DiscreteScale(0,1)       # wn these sims always return 0-1 normalized.

    def WUPSimilarity(self, w1: str, w2: str, l2s:Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        return self._RunSimilarityImpl("wup_similarity", w1, w2,l2s)

    def PATHSimilarity(self, w1: str, w2: str, l2s:Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        return self._RunSimilarityImpl("path_similarity", w1, w2,l2s)

    def LCHSimilarity(self, w1: str, w2: str, l2s:Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        """
        LCH implementation is on a [0-Max] scale. We don't know what Max could be.
        While calculating the shortest path, it involves hypernym and instance hypernyms. I couldn't see other relationships.
        :param w1:
        :param w2:
        :return:
        """
        return self._RunSimilarityImpl("lch_similarity", w1, w2,l2s)

    def LINSimilarity(self, w1: str, w2: str, l2s:Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        return self._RunSimilarityImpl("lin_similarity", w1, w2, l2s, self.InformationContent)

    def JCNSimilarity(self, w1: str, w2: str, l2s:Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        rawsim = self._RunSimilarityImpl("jcn_similarity", w1, w2, l2s, self.InformationContent)
        return rawsim

    def RESSimilarity(self, w1: str, w2: str, l2s:Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        return self._RunSimilarityImpl("res_similarity", w1, w2,l2s, self.InformationContent)

    @property
    def InformationContent(self):
        if(self._InformationContent is None): self._InformationContent = self._CreateInformationContent()
        return self._InformationContent

    @InformationContent.setter
    def InformationContent(self, value):
        self._InformationContent = value

    def _CreateInformationContent(self):
        from nltk.corpus import wordnet_ic
        brown_ic = wordnet_ic.ic('ic-brown.dat')        # y
        #semcor_ic = wordnet_ic.ic('ic-semcor.dat')
        return brown_ic

    def DetectRoots(self, surface: str, priorPOS: POSTypes = None) -> List[str]:
        """
        Very roughly returns roots using Morphy in WordNet. The list of suffixes is fixed. 
        There are no grammar rules, no disambiguation, and no knowledge of the lexicon. 
        Only works when there are inflectional suffixes like (s) plural. 
        Can only return a single root. 
        http://www.nltk.org/howto/wordnet.html

        :param surface: The word to find the root for.
        :param priorPOS: The POS (Part of Speech) information of the surface. 
                        This parameter improves the accuracy of root detection. 
                        If the POS of the given surface is known, it especially reduces False Positive errors.
        :return: Returns List[] if no results are found.
        """
        from nltk.corpus import wordnet as wn  # Import is long!
        
        if priorPOS is None:  # Try until all are found
            possesByPriority = [POSTypes.NOUN, POSTypes.ADJ, POSTypes.VERB, POSTypes.ADV]  
            # The priority here is debatable. Verbs could be given higher priority.
            roots = []
            for pos in possesByPriority:
                p: str = self._GetPosChar(pos)
                root: str = wn.morphy(surface, p)
                if root is not None:
                    roots.append(root)
            return roots if len(roots) != 0 else []
        else:
            p2: str = self._GetPosChar(priorPOS)
            root = wn.morphy(surface, p2)
            return [root] if root else []

    #endregion

    #region Taxonomy
    def Is(self, thing:Synset, type:Synset, ru:RelationUsage = RelationUsage.CreateHypernymWithInstances())->Optional[bool]:
        """
        Does the given word belong to the specified type group according to the Hypernymy relation?
        Since it is in SynSet type, it also checks all homonyms (lemmas).
        :param rel:
        :param thing:
        :param type:
        :return:
        """
        synsets = self.GetTypeHierarchy(thing,ru)
        for syn in synsets:
            if (syn._name == type._name): return True
        return False

    def GetChildren(self,syn:Synset, ru:RelationUsage = RelationUsage.CreateHypernymWithInstances())->List[Synset]:
        """
        Returns the more concrete synsets one level below the given synset through its Relations. 
        The top parent is 'entity.' Children are more concrete, and parents are more abstract.
        :return: Returns None if there are no matches.
        """
        if(ru.URelation == URelations.HypernymHyponym):
            return list(syn.hyponyms() + list(syn.instance_hyponyms()))
        elif(ru.URelation == URelations.MeronymHolonym):
            return list(syn.part_holonyms()) + list(syn.substance_holonyms()) + list(syn.member_holonyms())
        elif(ru.URelation == URelations.AllCombined):
            return list(syn.hyponyms()) + list(syn.instance_hyponyms()) + \
                   list(syn.part_holonyms()) + list(syn.substance_holonyms()) + list(syn.member_holonyms())
        else:
            raise NotImplementedError(str(ru))

    def GetParents(self,syn:Synset, ru:RelationUsage = RelationUsage.CreateHypernymWithInstances())->List[Synset]:
        """
        Returns the more abstract synsets one level above the given synset through its Relations. 
        The top parent is 'entity.' Children are more concrete, and parents are more abstract.
        # There is information that hypernym relations make up 80% of all relations. ref- budanitsky06-p16
        :param syn:
        :param rel:
        :return: Returns None if there are no matches.
        """
        if(ru.URelation == URelations.HypernymHyponym):
            return list(syn.hypernyms()) + list(syn.instance_hypernyms())
        elif(ru.URelation == URelations.MeronymHolonym):
            return list(syn.part_meronyms()) + list(syn.substance_meronyms()) + list(syn.member_meronyms())
        elif(ru.URelation == URelations.AllCombined):
            return list(syn.hypernyms()) + list(syn.instance_hypernyms()) + \
                   list(syn.part_meronyms()) + list(syn.substance_meronyms()) + list(syn.member_meronyms())
        else:
            raise NotImplementedError(str(ru))

    def _CombineMeronyms(self, synset:Synset, direction:Directions = Directions.LeftToRight):
        """
        We are not parsing meronyms for now.
        :param synset:
        :return:
        """
        if(direction==Directions.LeftToRight):
            members = list(synset.closure(lambda s:s.member_meronyms()))
            parts = list(synset.closure(lambda s:s.part_meronyms()))
            substances = list(synset.closure(lambda s:s.substance_meronyms()))
            return members + parts + substances
        elif(direction==Directions.RightToLeft):
            members = list(synset.closure(lambda s:s.member_holonyms()))
            parts = list(synset.closure(lambda s:s.part_holonyms()))
            substances = list(synset.closure(lambda s:s.substance_holonyms()))
            return members + parts + substances
        elif(direction==Directions.Both):
            members = list(synset.closure(lambda s:s.member_holonyms())) + list(synset.closure(lambda s:s.member_meronyms()))
            parts = list(synset.closure(lambda s:s.part_holonyms())) + list(synset.closure(lambda s:s.part_meronyms()))
            substances = list(synset.closure(lambda s:s.substance_holonyms())) + list(synset.closure(lambda s:s.substance_meronyms()))
            return members + parts + substances

    def _CombineDomains(self, synset:Synset, direction:Directions = Directions.LeftToRight):

        warnings.warn("Directions for domains have not been deliberately decided!")
        if(direction==Directions.LeftToRight):
            topics = list(synset.closure(lambda s:s.topic_domains()))
            regions = list(synset.closure(lambda s:s.region_domains()))
            usages = list(synset.closure(lambda s:s.usage_domains()))
            return topics + regions + usages
        elif(direction==Directions.RightToLeft):
            topics = list(synset.closure(lambda s:s.in_topic_domains()))
            regions = list(synset.closure(lambda s:s.in_region_domains()))
            usages = list(synset.closure(lambda s:s.in_usage_domains()))
            return topics + regions + usages
        elif(direction==Directions.Both):
            topics = list(synset.closure(lambda s:s.topic_domains())) + list(synset.closure(lambda s:s.in_topic_domains()))
            regions = list(synset.closure(lambda s:s.region_domains())) + list(synset.closure(lambda s:s.in_region_domains()))
            usages = list(synset.closure(lambda s:s.usage_domains())) + list(synset.closure(lambda s:s.in_usage_domains()))
            return topics + regions + usages

    def _CombineHypernymsWithInstances(self, synset:Synset, hypernyms:List[Synset]):
        synsInstanceTypes = list(synset.closure(lambda s:s.instance_hypernyms()))
        for _syn in synsInstanceTypes:
            hypernyms.append(_syn)
            childs = list(_syn.closure(lambda s:s.hypernyms()))       #Assumption: I assumed instances are connected to types at one level.
            hypernyms = hypernyms + childs
        return hypernyms

    def GetTypeHierarchy(self,thing:Synset,ru:RelationUsage = RelationUsage.CreateHypernymWithInstances())->List[Synset]:
        """
        Type hierarchies go top-to-bottom from the most concrete instances. 
        Returns the entire hierarchy flat in a single query.
        :param thing:
        :param ru:
        :return:
        """
        if(ru.URelation == URelations.HypernymHyponym):
            relHypernym = lambda s:s.hypernyms()
            hypernyms = list(thing.closure(relHypernym))     #closure returns a generator.
            if(ru.IncludeInstances):
                return self._CombineHypernymsWithInstances(thing,hypernyms)
            return hypernyms

        elif(ru.URelation == URelations.MeronymHolonym):
            return self._CombineMeronyms(thing)

        elif(ru.URelation == URelations.AllCombined):
            #type-based
            relHypernym = lambda s:s.hypernyms()
            hypernyms = list(thing.closure(relHypernym))     #closure returns a generator.
            if(ru.IncludeInstances):
                hypernyms = self._CombineHypernymsWithInstances(thing,hypernyms)

            meronyms = self._CombineMeronyms(thing)
            return hypernyms + meronyms
        else:
            raise Exception("not supported!")

    def GetRelateds(self, thing: Synset, ru: RelationUsage = RelationUsage.CreateHypernymWithInstances()) -> List[Synset]:
        """
        Returns first-degree relations based on the given relation.
        :param thing:
        :param ru:
        :return:
        """
        #Hypernymy
        if(ru.URelation == URelations.HypernymHyponym):
            if(ru.Direction == Directions.LeftToRight):
                if(ru.IncludeInstances): return thing.hypernyms()
                else: return thing.hypernyms() + thing.instance_hypernyms()
            elif(ru.Direction == Directions.LeftToRight):
                if(ru.IncludeInstances): return thing.hyponyms()
                else: return thing.hyponyms() + thing.instance_hyponyms()
            else:
                if(ru.IncludeInstances): return thing.hypernyms() + thing.hyponyms()
                else: return thing.hypernyms() + thing.hyponyms() + thing.instance_hyponyms() + thing.instance_hypernyms()

        elif(ru.URelation == URelations.MeronymHolonym):
            return self._CombineMeronyms(thing,ru.Direction)

        elif(ru.URelation == URelations.AllCombined):
            raise NotImplementedError("URelations.AllCombined not supported!")

        elif(ru.URelation == URelations.Domains):
            return self._CombineMeronyms(thing,ru.Direction)

        else:
            raise NotImplementedError(str(ru))

    @staticmethod
    def ToTaxonomyType(synset:Synset)->TaxonomyType:
        tt:TaxonomyType = TaxonomyType(synset._name)
        for l in synset.lemma_names():
            tt.Synonyms.append(l)
        return tt

    def IsInType(self, thing:str, typeCode:str, sense:SenseStrategy=SenseStrategy.CombineAllSenses, ru:RelationUsage=RelationUsage.CreateAll(), wordPos:POSTypes = None) -> Optional[bool]:
        if(sense == SenseStrategy.CombineAllSenses): raise NotImplementedError("SenseStrategy")
        pos = POSTypes.NOUN if not wordPos else wordPos
        sThing:Synset = self.LoadSynset(thing,pos,1)        #first sense assumption
        sType:Synset = self.LoadSynset(typeCode,POSTypes.NOUN,1)
        return self.Is(sThing,sType,ru)

    def GetTypeCodesOfHierarchy(self, thing:str, sense:SenseStrategy = SenseStrategy.CombineAllSenses, ru:RelationUsage=RelationUsage.CreateAll(), wordPos:POSTypes = None)->List[TaxonomyType]:
        typeSynsets:List[Synset] = []
        posList = None if wordPos is None else [wordPos]
        if(sense == SenseStrategy.FirstSenseOnly):
            sThing:Synset = self.LoadSynset(thing,posList[0] if posList is not None else None,1)
            typeSynsets = self.GetTypeHierarchy(sThing,ru)
        else:
            syns = self.LoadSynsets(thing,posList)
            for syn in syns:
                typeSyns = self.GetTypeHierarchy(syn,ru)
                typeSynsets = typeSynsets + typeSyns
        if len(typeSynsets) == 0: return []
        #export
        out:List[TaxonomyType] = []
        for ts in typeSynsets:
            tt = self.ToTaxonomyType(ts)
            out.append(tt)
        return out

#endregion


    def GetDefinitions(self, word: str, forPOS:POSTypes = None)->List[str]:
        syns = self.LoadSynsets(word,[forPOS] if forPOS else [])
        defs = []
        for syn in syns:
            defs.append(syn.definition())
        return defs


class NLTKWordNetWrapperIntegrationTest(TestCase):

    def test_DetectRoot_WithPOSArgument_ReturnRoot(self):
        wordnet = NLTKWordNetWrapper()
        roots = wordnet.DetectRoots("dogs", None)  # Does not work with derivational suffixes!
        self.assertEqual("dog", roots[0])  # But it cannot convert 'colors' to 'color'! Do not rely on Morphy too much.

    def test_DetectRoot_WithPOSArgumentButExpectedNoMatchingForPOS_ReturnEmpty(self):
        wordnet = NLTKWordNetWrapper()
        roots = wordnet.DetectRoots("dogs", POSTypes.ADV)  # Since 'dogs' is not an adverb, it won't find its root. This parameter can reduce false positives.
        self.assertEqual(0, roots.__len__())

    def test_DetectRoot_WithoutAnyPOSArgument_ReturnFirstMatchingOrNone(self):
        wordnet = NLTKWordNetWrapper()
        self.assertEqual("deny", wordnet.DetectRoots("denied", None)[0])

    def test_DetectRoot_NoPOSArgAndNoMatching_ReturnEmptyList(self):
        wordnet = NLTKWordNetWrapper()
        roots = wordnet.DetectRoots("gokhancalar", None)
        self.assertEqual(0, roots.__len__())

    def test_DetectRoot_StemmerCases(self):
        wordnet = NLTKWordNetWrapper()
        cases = []
        cases.append(WordPair("tables", "table"))  # Surface, ExpectedRoot

        df = DataFrame()
        i = 1
        anyFailed = False
        for c in cases:
            expectedRoot = c.Word2
            surface = c.Word1
            actualRoots = wordnet.DetectRoots(surface, POSTypes.NOUN)
            df.at[i, "Surface"] = surface
            df.at[i, "ExpectedRoot"] = expectedRoot
            df.at[i, "ActualRoots"] = actualRoots
            passed = expectedRoot in actualRoots
            df.at[i, "Passed"] = "OK" if passed else "X"
            if not passed:
                anyFailed = True
            i = i + 1
        print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=FormatHelper._ThreeDigitFormat))
        if anyFailed:
            self.fail("Some cases failed!")
        else:
            print("All " + str(i) + " ThingIsType test cases passed.")

    def test_Is_ThingIsTypeCases(self):
        from nltk.corpus import wordnet as wn
        cases = []  # thing, type, expected
        cases.append([wn.synset('dog.n.01'), wn.synset('animal.n.01'), True])
        cases.append([wn.synset('animal.n.01'), wn.synset('entity.n.01'), True])
        cases.append([wn.synset('cancer.n.01'), wn.synset('illness.n.01'), True])
        cases.append([wn.synset('animal.n.01'), wn.synset('illness.n.01'), False])
        cases.append([wn.synset('ambystomid.n.01'), wn.synset('living_thing.n.01'), True])
        cases.append([wn.synset('ambystomatidae.n.01'), wn.synset('biological_group.n.01'), True])
        cases.append([wn.synset('table.n.01'), wn.synset('animal.n.01'), False])

        target = NLTKWordNetWrapper()
        df = DataFrame()
        i = 1
        anyFailed = False
        for case in cases:
            thing = case[0]
            type = case[1]
            expected = case[2]
            df.at[i, "Thing"] = str(thing)
            df.at[i, "Type"] = str(type)
            df.at[i, "Expected"] = expected
            actual = target.Is(thing, type, RelationUsage.CreateAll())
            df.at[i, "Actual"] = actual
            passed = actual == expected
            df.at[i, "Passed"] = "OK" if passed else "X"
            if not passed:
                anyFailed = True
            i = i + 1
        print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=FormatHelper._ThreeDigitFormat))
        if anyFailed:
            self.fail("Some cases failed!")
        else:
            print("All " + str(i) + " ThingIsType test cases passed.")

    def test_IsInType_WithPosValidNames_Return(self):
        target = NLTKWordNetWrapper()
        actual = target.IsInType("cat", "living_thing", SenseStrategy.FirstSenseOnly, RelationUsage(), POSTypes.NOUN)
        self.assertTrue(actual)

    def test_GetTypeCodesOfHierarchy_LemmaWithSynonmyLemmasInItsSense_ReturnSynonymsToo(self):
        target = NLTKWordNetWrapper()
        actuals = target.GetTypeCodesOfHierarchy("taxi", SenseStrategy.CombineAllSenses, RelationUsage.CreateHypernymWithInstances(), POSTypes.NOUN)  # taxi is a car. car is a synonym of automobile
        actual = actuals[0]
        self.assertTrue("automobile" in actual.Synonyms)

    def test_GetTypeCodesOfHierarchy_LemmaWithMultipleSenses_ReturnCombined(self):
        target = NLTKWordNetWrapper()
        actual: List[TaxonomyType] = target.GetTypeCodesOfHierarchy("cat", SenseStrategy.CombineAllSenses, RelationUsage.CreateAll(), POSTypes.NOUN)
        self.assertTrue(len(list(filter(lambda x: x.TypeCode == "entity.n.01", actual))) > 1)  # We know that the word 'cat' has multiple senses.

    def test_GetTypeCodesOfHierarchy_SynsetWithNoHypernymTypeHierachy_ReturnEmptyList(self):
        target = NLTKWordNetWrapper()
        actual = target.GetTypeCodesOfHierarchy("alcibiades", SenseStrategy.CombineAllSenses, RelationUsage(URelations.MeronymHolonym), POSTypes.NOUN)
        self.assertEqual(0, len(actual))

    def test_GetTypeCodesOfHierarchy_InstanceWord_ReturnTypeRelationsViaCombiningRelationsTypes(self):
        target = NLTKWordNetWrapper()
        actual = target.GetTypeCodesOfHierarchy("turkey", SenseStrategy.CombineAllSenses, RelationUsage.CreateHypernymWithInstances(), POSTypes.NOUN)
        self.assertTrue(len(actual) > 2)
        self.assertEqual("entity.n.01", actual[actual.__len__() - 1].TypeCode)

    def test_GetTypeCodesOfHierarchy_WordWithBothHypernymAndInstanceRelations_ReturnCombined(self):
        target = NLTKWordNetWrapper()
        actual: List[TaxonomyType] = target.GetTypeCodesOfHierarchy("turkey", SenseStrategy.CombineAllSenses, RelationUsage.CreateHypernymWithInstances(), POSTypes.NOUN)
        self.assertTrue(len(list(filter(lambda x: x.TypeCode == "country.n.02", actual))) == 1)
        self.assertTrue(len(list(filter(lambda x: x.TypeCode == "animal.n.01", actual))) == 1)

    def test_GetParents_SynsetWithParent_Return(self):
        target = NLTKWordNetWrapper()
        syn = target.LoadSynset("car", POSTypes.NOUN, 1)
        actual = target.GetParents(syn, RelationUsage(URelations.HypernymHyponym, False))  # Whether False|True does not matter for this case.
        self.assertEqual(1, actual.__len__())
        self.assertEqual("motor_vehicle.n.01", actual[0]._name)

    def test_GetParents_InstanceSynset_ReturnParent(self):
        target = NLTKWordNetWrapper()
        syn = target.LoadSynset("armenia", POSTypes.NOUN, 1)
        actual = target.GetParents(syn, RelationUsage())
        self.assertEqual(1, list(filter(lambda x: x._name == "asian_country.n.01", actual)).__len__())

    def test_GetRelateds_MemberOrMeronym_ReturnAsRelated(self):
        target = NLTKWordNetWrapper()
        syn = target.LoadSynset("muslim", POSTypes.NOUN, 1)
        actuals = target.GetRelateds(syn, RelationUsage(URelations.MeronymHolonym, Direction=Directions.RightToLeft))
        self.assertTrue(len(list(filter(lambda x: x._name == "islam.n.01", actuals))) == 1)

    def test_ToTaxonomyType(self):
        syn = NLTKWordNetWrapper().LoadSynset("car", POSTypes.NOUN, 1)
        actual: TaxonomyType = NLTKWordNetWrapper.ToTaxonomyType(syn)
        self.assertEqual("car.n.01", actual.TypeCode)
        self.assertEqual(5, actual.Synonyms.__len__())


def QueryLanguages():
    import nltk
    nltk.download('omw')
    from nltk.corpus import wordnet as wn

    # List languages supported by WordNet
    languages = wn.langs()
    print("Languages supported by WordNet:")
    print(languages)
    print(f"Total languages: {len(languages)}")

    # Check for a specific language WordNet
    # language_code = 'fra'  # Example for French
    # print(f"\nChecking if WordNet exists for '{language_code}':")
    stats = {}
    for lang in languages:
        lemmas = wn.all_lemma_names(lang=lang, pos=None)
        words:set = set()
        for lemma in lemmas:
            words.add(lemma)
        # print(f"{lang}\t{len(words)}")
        stats[lang] = len(words)

    stats_sorted = dict(sorted(stats.items(), key=lambda item: item[1],reverse=True))
    print(stats_sorted)
    # pprint.pprint(stats_sorted)

if __name__ == "__main__":
    QueryLanguages()
    exit()

    # unittest.main(verbosity=2)
    # exit()

    # Antonym check
    from nltk.corpus import wordnet as wn, words

    # good_lemma = wn.lemma('good.a.01.good')
    # print(good_lemma.antonyms())

    goods = wn.synsets('porte', lang="fra")
    print(goods)

    good = wn.synset('good.a.01')
    print(good.lemma_names("fra"))

    print(good.definition())
    print(good.antonyms())
    exit()

    wordnet = NLTKWordNetWrapper(l2s= Lemma2SynsetMatching.HighestScoreOfCombinations, wordSimPOSFilters=[POSTypes.NOUN], algorithm=WordNetSimilarityAlgorithms.LCH)
    # wordnet = NLTKWordNetWrapper(l2s= Lemma2SynsetMatching.UseFirstSense, wordSimPOSFilters=[POSTypes.NOUN])
    taxes: List[TaxonomyType] = wordnet.GetTypeCodesOfHierarchy("nation")
    print(taxes)

    # r1s = wordnet.DetectRoot("redeposition", None)
    # r1s = wordnet.DetectRoot("dogs", None)
    # r2s = wordnet.DetectRoot("depositing", None)  # Why doesn't 'Doggy' return 'dog'??
    # print(r1s[0] + " - " + r2s[0])
    # exit()

    # x = wordnet.WordSimilarity("dog", "cat")
    # lemmas = wordnet.GetAllLemmas(singleWordsOnly=False, posFilters=[POSTypes.NOUN, POSTypes.ADJ])

    # Count verbs in English
    # lemmas = wordnet.GetAllLemmas(singleWordsOnly=False, posFilters=[POSTypes.NOUN])
    # print(lemmas)

    # syns = wordnet.LoadSynsets("glass", [POSTypes.NOUN, POSTypes.NOUN, POSTypes.ADJ, POSTypes.VERB, POSTypes.ADV])
    syns2 = wordnet.LoadSynsetByName("state.n.02")
    print(syns2)
    print(syns2.lemmas())
    print(syns2.definition())
    # exit()

    # Testing InformationContent
    sim = wordnet.LCHSimilarity("turkish", "turkey", Lemma2SynsetMatching.HighestScoreOfCombinations)
    # sim2 = wordnet.LCHSimilarity("dog", "cat", Lemma2SynsetMatching.HighestScoreOfCombinations)
    print(sim)
    # print("dog, cat", sim2)
    # print("dog, dog", wordnet.LCHSimilarity("dog", "dog", Lemma2SynsetMatching.HighestScoreOfCombinations))
    print("group - communication (lch)", wordnet.LCHSimilarity("group", "communication", Lemma2SynsetMatching.HighestScoreOfCombinations))
    print("group - communication (wup)", wordnet.WUPSimilarity("group", "communication", Lemma2SynsetMatching.HighestScoreOfCombinations))
    print("turkey - turkish (wup)", wordnet.WUPSimilarity("turkey", "turkish", Lemma2SynsetMatching.HighestScoreOfCombinations))
    print("turkey - turkish (lch)", wordnet.LCHSimilarity("turkey", "turkish", Lemma2SynsetMatching.HighestScoreOfCombinations))
    print("turkey - country (lch)", wordnet.LCHSimilarity("turkey", "country", Lemma2SynsetMatching.HighestScoreOfCombinations))
    print("turkey - turkish (path)", wordnet.PATHSimilarity("turkey", "turkish", Lemma2SynsetMatching.HighestScoreOfCombinations))
    # sim = wordnet.WUPSimilarity("dog", "cat", Lemma2SynsetMatching.HighestScoreOfCombinations)
    # sim2 = wordnet.LINSimilarity("dog", "cat", Lemma2SynsetMatching.HighestScoreOfCombinations)
    # synset = wordnet.LoadSynset("socialism")
    #
    print("\n der-rel")
    lemmas = wordnet.LoadLemmas("activeness")
    for l in lemmas:
        der_rel = wordnet.GetDerivationallyRelatedForms(l)
        print(der_rel)

    # words = wordnet._GetAllUnrelatedLemmas()
    # words = wordnet.GetWords()
