import unittest
from array import array
from functools import partial
from typing import Set, List, Iterable, Tuple, Optional, cast
from unittest import TestCase, skip
from unittest.mock import patch
from nltk.corpus.reader import Synset

from src.Core.Languages.Grammars.IGrammar import IGrammar
from src.Core.Languages.LinguisticContext import LinguisticContext
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.IRootDetector import IRootDetector
from src.Core.Morphology.RootDetection.RootDetectorCacher import MonitorableCacheBase
from src.Core.Preprocessing.Preprocessors import Preprocessors
from src.Core.Segmentation.Tokenizers.ITokenizer import ITokenizer
from src.Core.Segmentation.Tokenizers.NLTKWhitespaceTokenizer import NLTKWhitespaceTokenizer
from src.Core.WordNet.IWordNet import IWordNet
from src.Core.WordNet.IWordTaxonomy import TaxonomyType, SenseStrategy, RelationUsage
from src.Core.WordPair import WordPair
from src.Tools.Logger import logl


class WordPairDefinitionSourceFilter(object):

    def __init__(self, wn:IWordNet, lingContext:LinguisticContext, forPOS:POSTypes = None, rootDetector:IRootDetector = None, fastRootDetector:IRootDetector = None, rootType:str="entity.n.01") -> None:
        """
        :param wn:
        :param lingContext:
        :param forPOS:
        :param rootDetector: The most advanced analyzer or stack.
        :param fastRootDetector: A stemmer expected to work quickly in more superficial scenarios (like inflections).
        """
        super().__init__()
        self.WN = wn
        self.ForPOS = forPOS
        self.LingContext = lingContext
        self.Grammar:IGrammar = LinguisticContext.BuildGrammar(lingContext)
        self.Processor = Preprocessors()
        self.RootDetector:IRootDetector = rootDetector
        self.FastRootDetector:IRootDetector = fastRootDetector
        self._ROOT_TYPE = rootType

    def AreReferencingEachOtherInDefinitions(self,wp:WordPair, tokenizer:ITokenizer, minRootLength) ->bool:
        """
        Checks if the main word appears in the other's definition.
        It checks by separating words from their punctuation.
        If there is a RootDetector, it converts word comparisons to root forms. A word can have multiple roots.
        :param minRootLength: The minimum length for a root to be considered a match. Equal to minWordLength.
        :param wp:
        :param tokenizer:
        :return:
        """
        #adding possible synonyms
        syns1:List[Synset] = self.WN.LoadSynsets(wp.Word1,[self.ForPOS])
        syns2:List[Synset] = self.WN.LoadSynsets(wp.Word2,[self.ForPOS])
        lemmas1,lemmas2 = [],[]
        for s1 in syns1:
            lemmas1 = lemmas1 + s1.lemma_names()
        for s2 in syns2:
            lemmas2 = lemmas2 + s2.lemma_names()

        synonyms1 = self._DecomposePhrasesOfSets(set(lemmas1),minRootLength-1) if syns1 else set()      #-1 because these are types, not definitions. The likelihood of containing unnecessary stopwords is relatively low.
        synonyms2 = self._DecomposePhrasesOfSets(set(lemmas2),minRootLength-1) if syns2 else set()
        synonyms1.add(wp.Word1)
        synonyms2.add(wp.Word2)
        syncommon = synonyms1 & synonyms2
        if(syncommon): return True,syncommon            #if there is a direct synonym match, return without extending.

        #length control
        effwords1:Set[str] = set(filter(lambda x:len(x) >= minRootLength,synonyms1))      #Short words are directly exempt
        effwords2:Set[str] = set(filter(lambda x:len(x) >= minRootLength,synonyms2))

        #defs
        def1:str = self.Grammar.ToLowerCase(self.Processor.RemovePunctuation(self.WN.GetMergedDefinitions(wp.Word1,self.ForPOS)))
        def2:str = self.Grammar.ToLowerCase(self.Processor.RemovePunctuation( self.WN.GetMergedDefinitions(wp.Word2,self.ForPOS)))
        tokens1 = tokenizer.Tokenize(def1)
        tokens2 = tokenizer.Tokenize(def2)

        word1Refs,word2Refs = False,False
        shared1,shared2 = None,None

        #region Cache Trace (Optional if RootDetector is MonitorableCacheBase)
        if(self.RootDetector):      #may not be present during testing, not every ICacher may implement it
            if isinstance(self.RootDetector,MonitorableCacheBase):
                cache:MonitorableCacheBase = self.RootDetector
                if(cache.Attempt > 10000):      #do not set to 1000, it logs too much in batch operations.
                    print("\t cache miss/all: " + str(round(cache.MissRatio()*100,2))+"%")
                    cache.ResetCounters()
                    logl(str( cache.CachedItemCount()),"cached items",anyMode=True)
        #endregion

        for _w2 in effwords2:
            word1Refs,shared1 = self._IsWordRootInDefinition(_w2,tokens1,minRootLength)     #Slowdown here! And for each word. Up to this point, it is quite fast.
            if(word1Refs == True): break
        for _w1 in effwords1:
            word2Refs,shared2 = self._IsWordRootInDefinition(_w1,tokens2,minRootLength)
            if(word2Refs == True): break
        return word1Refs or word2Refs, shared1 or shared2       #If either references the other, it is true. TO: For trace, it can be returned who referenced whom in the future.

    def _IsWordRootInDefinition(self, w:str, defTokens, minRootLength)->Tuple[bool,Optional[str]]:
        """
        Checks if the root of the given word appears among the roots of the given tokens.
        :param w:
        :param defTokens:
        :param minRootLength:
        :return:
        """
        w = self.Grammar.ToLowerCase(w)
        if(not self.RootDetector):
            return (w in defTokens), w

        effDefTokens = list(filter(lambda x : len(x) >= minRootLength, defTokens))  #Do not pass as filter instead of list, filter empties after the first loop.

        #def
        fwords = self.RootDetector.DetectRoots(w, self.ForPOS)      #Loops can be optimized more but I tested, DetectRoots takes more time, despite the cache. I expect the process to speed up as the cache increases!
        if(w not in fwords): fwords.append(w)    #surface form can also match. root forms are additional!

        for fw in fwords:
            for df in effDefTokens:
                if(df == fw): return True,df                       #First, check if the surface form matches

                #roots
                rs = set(self.RootDetector.DetectRoots(df, self.ForPOS))         #if multiple roots come, def-root is recalculated repeatedly!!!
                for r in rs:
                    if(len(r) >= minRootLength):
                        if(r == fw):
                            return True, ("root:'"+ r + "' by '" + df + "' matches '" + fw + "<" + w + "")       #We also add the previous forms of the root for trace purposes. #< means root of.
        return False,None

    def _BuildRootTokens(self, tokens:Iterable[str], minRootLength:int)->Set[str]:
        """
        Adds root versions to the given tokens.
        :param tokens:
        :param minRootLength:
        :return:
        """
        tokens2 = set()
        for t in tokens:
            tokens2.add(t)      #token's own form should also be included
            roots:List[str] = self.FastRootDetector.DetectRoots(t,self.ForPOS)
            bigroots:List[str] = [x for x in roots if len(x) >= minRootLength]
            for r in bigroots:
                tokens2.add(r)
            #Compounding - Small roots may have been eliminated above but maybe they will produce a compound. Ex: (tape)(worm)s -> tapeworm
            rCompounds = self._ExtractTwoSegmentPhrases(bigroots)      #We try the possibility of being a compound word by sequentially combining the roots. In TR, very small roots like de, değ can come and produce strange words like değde. We applied minRoot while trying the compound of roots. That's why there are bigroots.
            for rc in rCompounds:
                tokens2.add(rc.replace(" ",""))
        return tokens2

    def _GetTypes(self,w:str, typeDepthRatio:float):
        typesForAllSenses:List[TaxonomyType] = self.WN.GetTypeCodesOfHierarchy(w,SenseStrategy.CombineAllSenses, RelationUsage.CreateHypernymWithInstances(),self.ForPOS)
        return WordPairDefinitionSourceFilter._TrimTypesByDepthRatio(self._ROOT_TYPE,typesForAllSenses,typeDepthRatio)

    @staticmethod
    def _TrimTypesByDepthRatio(rootType:str,types:List[TaxonomyType],typeDepthRatio:float):
        """
        Analyzes the type hierarchy containing multiple senses in depth and extracts concrete types.
        :param w:
        :param typeDepthRatio:
        :return:
        """
        finalTypes:List[str] = []
        i:int = 0
        senseStart:int=0
        for s in types:
            if(s.TypeCode == rootType):       #If it somehow does not have a root, type information is ignored, an empty list is returned.
                sSize:int = i - senseStart+1
                sDepth:float = int(sSize * typeDepthRatio)      #effective size for that sense.
                sTypes = types[senseStart:senseStart+sDepth]
                finalTypes = finalTypes + sTypes
                #new sense
                senseStart = i+1
            i += 1
        return finalTypes

    def ContainsKeywordInTypeHierarchy(self,wp:WordPair,tokenizer:ITokenizer, minRootLength:int, typeDepthRatio:float = 0.75) ->bool:
        """
        If one appears in the other's type hierarchy and the other appears in the definition.
        :param minRootLength: The minimum word length to provide intersection: to avoid intersections like part, of.
        :type typeDepthRatio: If 0.5, only 1/2 of the concrete types in the entire type hierarchy are considered. To avoid matching words like organism, entity at the bottom.
        :return:
        """

        #region Types
        t1:List[TaxonomyType] = self._GetTypes(wp.Word1,typeDepthRatio)
        t2:List[TaxonomyType] = self._GetTypes(wp.Word2,typeDepthRatio)
        types1 = set()
        types2 = set()
        for t1_ in t1:
            words = t1_.AllWords()
            for w in words:
                types1.add(w)
        for t2_ in t2:
            words = t2_.AllWords()
            for w in words:
                types2.add(w)

        #Phrases for Types
        decomposePhrases:bool = True
        if(decomposePhrases):
            types1 = self._DecomposePhrasesOfSets(types1,minRootLength)
            types2 = self._DecomposePhrasesOfSets(types2,minRootLength)

        if(self.FastRootDetector):          #Types are also reduced to root form. For example, cultivation should match with cultivator.
            types1 = self._BuildRootTokens(types1,minRootLength+2)      #Increased the threshold because it is dangerous for types to match very general roots.
            types2 = self._BuildRootTokens(types2,minRootLength+2)
        #end region

        #region Definitions
        def1:str = self.Grammar.ToLowerCase(self.Processor.RemovePunctuation(self.WN.GetMergedDefinitions(wp.Word1,self.ForPOS)))
        def2:str = self.Grammar.ToLowerCase(self.Processor.RemovePunctuation( self.WN.GetMergedDefinitions(wp.Word2,self.ForPOS)))
        defTokens1:Iterable[str] = tokenizer.Tokenize(def1)
        defTokens2:Iterable[str] = tokenizer.Tokenize(def2)
        defRootTokens1:Set[str] = set()
        defRootTokens2:Set[str] = set()

        #Root Enrichment (MRootDetector works very slowly (x3) and is useful in 1/1000 scenarios, so we use FRootDetector.)
        if(self.FastRootDetector):
            defRootTokens1 = self._BuildRootTokens(defTokens1,minRootLength)
            defRootTokens2 = self._BuildRootTokens(defTokens2,minRootLength)

        #finals
        defSet1 = set(defTokens1) | defRootTokens1 | WordPairDefinitionSourceFilter._ExtractTwoSegmentPhrases(defTokens1)            #Phrases should be after rootDetection!. Phrases do not consist of root forms.
        defSet2 = set(defTokens2) | defRootTokens2 | WordPairDefinitionSourceFilter._ExtractTwoSegmentPhrases(defTokens2)
        #endregion

        commons1 = defSet1 & types2
        commons2 = defSet2 & types1

        #Last length filter
        hasAnyCommon:bool = commons1.__len__()>0 or commons2.__len__() >0
        return (True,(commons1 | commons2)) if hasAnyCommon else (False,None)

    @staticmethod
    def _ExtractTwoSegmentPhrases(tokens:List[str])->Set[str]:
        """
        Returns the given tokens as two-segment phrases from left to right.
        :param tokens:
        :return:
        """
        if(len(tokens) < 2): return set()
        i = 0
        blocks:Set[str] = set()
        for t in tokens:
            if(i==0):
                i += 1
                continue
            blocks.add(tokens[i-1] + " " + t)
            i += 1
        return blocks

    @staticmethod
    def _DecomposePhrasesOfSets(myset:Set[str], minRootLength:int, includePhraseItself:bool = True)->Set[str]:
        """Splits phrases into words. Skips very small words."""
        new:Set[str] = set()
        for s in myset:
            segments = s.strip().replace("_", " ").split(" ")     #English synset names are with _, TR ones are with spaces !!!
            if(segments.__len__() == 1): new.add(s)
            else:
                for seg in segments:
                    seg = seg.strip()
                    if(len(seg) >= minRootLength):
                        new.add(seg)
                if(includePhraseItself): new.add(s.replace("_"," "))        #Do not separate with _ again.
        return new

class WordPairDefinitionSourceFilterTest(TestCase):

    def test_ExtractTwoSegmentPhrases_HasPhrases_Extact(self):
        actual:Set[str] = WordPairDefinitionSourceFilter._ExtractTwoSegmentPhrases(["one","to","one"])
        self.assertEqual(2,actual.__len__())
        self.assertEqual(1, len(list(filter(lambda x:x == "one to",actual))))
        self.assertEqual(1, len(list(filter(lambda x:x == "to one",actual))))

    def test_ExtractTwoSegmentPhrases_SingleWord_ReturnEmpty(self):
        actual:Set[str] = WordPairDefinitionSourceFilter._ExtractTwoSegmentPhrases(["word1"])
        self.assertEqual(0,actual.__len__())

    #@patch.multiple(IWordDefinitionSource, __abstractmethods__=set())
    @patch.multiple(IWordNet, __abstractmethods__=set())
    def test_AreReferencingEachOtherInDefinitions_DefinitionsReferEachOther_ReturnMatched(self):
        defsource = IWordNet
        def fakeGetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
            if(word == "biochemist"): return "works on the field biochemistry"
            return "another definiiton text"
        defsource.GetMergedDefinitions = partial(fakeGetMergedDefinitions,defsource)
        def fakeLoadSynsets(self, lemma:str, pos:POSTypes=POSTypes.NOUN,senseOrder:int=1):
            return [Synset(None)]
        defsource.LoadSynsets = partial(fakeLoadSynsets,defsource)
        target = WordPairDefinitionSourceFilter(defsource,LinguisticContext.BuildEnglishContext())
        actual:bool = target.AreReferencingEachOtherInDefinitions(WordPair("biochemist","biochemistry"),NLTKWhitespaceTokenizer(),minRootLength=3)
        self.assertTrue(actual)

    @patch.multiple(IWordNet, __abstractmethods__=set())
    def test_AreReferencingEachOtherInDefinitions_DefinitionsReferEachOtherWordsNearPuncts_RemovePunctsAndReturnMatched(self):
        wn = IWordNet()
        def fakeGetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
            if(word == "saclant"): return "commanding officer of ACLANT; a general "
            return "another dummy definition"
        wn.GetMergedDefinitions = partial(fakeGetMergedDefinitions,wn)
        def fakeLoadSynsets(self, lemma:str, pos:POSTypes=POSTypes.NOUN,senseOrder:int=1):
            return [Synset(None)]
        wn.LoadSynsets = partial(fakeLoadSynsets,wn)
        target = WordPairDefinitionSourceFilter(wn,LinguisticContext.BuildEnglishContext())
        actual,shared = target.AreReferencingEachOtherInDefinitions(WordPair("saclant","aclant"),NLTKWhitespaceTokenizer(),minRootLength=3)
        self.assertTrue(actual)

    @patch.multiple(IWordNet, __abstractmethods__=set())
    @patch.multiple(IRootDetector, __abstractmethods__=set())
    def test_AreReferencingEachOtherInDefinitions_DefinitionsReferWordsConstituteOfSynonyms_ExplodeSynonymsAndMatch(self):
        wn = IWordNet()
        rootDetector = IRootDetector()

        def fakeGetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
            if(word == "w2"): return "drugs in humans"
            return ""
        wn.GetMergedDefinitions = partial(fakeGetMergedDefinitions,wn)

        def fakeLoadSynsets(self, lemma:str, pos:POSTypes=POSTypes.NOUN,senseOrder:int=1):
            if(lemma == "w1"):
                s = Synset(None)
                def fakeLemmaNames(self):
                    return ["drug_company"]
                s.lemma_names = partial(fakeLemmaNames,s)
                return [s]
            return [Synset(None)]
        wn.LoadSynsets = partial(fakeLoadSynsets,wn)

        rootDetector = IRootDetector()
        def fakeDetectRoots(self, surface:str, priorPOS:POSTypes = None):
            if(surface == "drugs"): return {"drug"}
            return []
        rootDetector.DetectRoots = partial(fakeDetectRoots,rootDetector)

        target = WordPairDefinitionSourceFilter(wn,LinguisticContext.BuildEnglishContext(),rootDetector=rootDetector)
        actual,shared = target.AreReferencingEachOtherInDefinitions(WordPair("w1","w2"),NLTKWhitespaceTokenizer(),minRootLength=3)
        self.assertTrue(actual)

    @patch.multiple(IWordNet, __abstractmethods__=set())
    def test_ContainsKeywordInTypeHierarchy_OneDefReferencingOthersTypeInHierarchy_ReturnTrue(self):            #geçen word diğerinin type bilgisinde geçiyor.
        wn = IWordNet()
        def fakeGetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
            if(word == "aphagia"): return "loss of the ability to swallow "
            return "another dummy definition"
        def fakeGetTypeCodesOfHierarchy(self,thing:str, sense:SenseStrategy=SenseStrategy.CombineAllSenses, ru:RelationUsage=RelationUsage.CreateAll(), wordPos:POSTypes = None):
            if(thing == "aerophagia"):
                return [TaxonomyType("conrete.n.01"),TaxonomyType("swallow.n.01"),TaxonomyType("abstraction.n.01"),TaxonomyType("entity.n.01")]
            else:
                return []
        wn.GetMergedDefinitions = partial(fakeGetMergedDefinitions,wn)
        wn.GetTypeCodesOfHierarchy = partial(fakeGetTypeCodesOfHierarchy,wn)
        target = WordPairDefinitionSourceFilter(wn,LinguisticContext.BuildEnglishContext())
        actual,shared = target.ContainsKeywordInTypeHierarchy(WordPair("aerophagia","aphagia"),NLTKWhitespaceTokenizer(),minRootLength=5,typeDepthRatio=0.5)
        self.assertTrue(actual)

    @patch.multiple(IWordNet, __abstractmethods__=set())
    def test_ContainsKeywordInTypeHierarchy_OneDefReferencingSynonymOfATypeInHierarchy_ReturnTrue(self):
        wn = IWordNet()
        def fakeGetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
            if(word == "w2"): return "brain is the synonym of on of the types"
            return "another dummy definition"
        def fakeGetTypeCodesOfHierarchy(self,thing:str, sense:SenseStrategy=SenseStrategy.CombineAllSenses, ru:RelationUsage=RelationUsage.CreateAll(), wordPos:POSTypes = None):
            if(thing == "w1"):
                tt = [TaxonomyType("conrete.n.01"),TaxonomyType("beyin.n.01"),TaxonomyType("abstraction.n.01"),TaxonomyType("entity.n.01")]
                tt[1].Synonyms.append("brain")     #adding synonym
                return tt
            else:
                return []
        wn.GetMergedDefinitions = partial(fakeGetMergedDefinitions,wn)
        wn.GetTypeCodesOfHierarchy = partial(fakeGetTypeCodesOfHierarchy,wn)
        target = WordPairDefinitionSourceFilter(wn,LinguisticContext.BuildEnglishContext())
        actual,shared = target.ContainsKeywordInTypeHierarchy(WordPair("w1","w2"),NLTKWhitespaceTokenizer(),minRootLength=5,typeDepthRatio=0.8)
        self.assertTrue(actual)

    @patch.multiple(IWordNet, __abstractmethods__=set())
    @patch.multiple(IRootDetector, __abstractmethods__=set())
    def test_ContainsKeywordInTypeHierarchy_OneRootInDefReferencingOthersTypeInHierarchy_ReturnTrue(self):
        #region stub1
        wn = IWordNet()
        def fakeGetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
            if(word == "w2"): return "unable to see colors"
            return "another dummy definition"
        def fakeGetTypeCodesOfHierarchy(self,thing:str, sense:SenseStrategy=SenseStrategy.CombineAllSenses, ru:RelationUsage=RelationUsage.CreateAll(), wordPos:POSTypes = None):
            if(thing == "w2"):
                return [TaxonomyType("color_blindness.n.01"),TaxonomyType("swallow.n.01"),TaxonomyType("abstraction.n.01"),TaxonomyType("entity.n.01")]
            else:
                return []
        wn.GetMergedDefinitions = partial(fakeGetMergedDefinitions,wn)
        wn.GetTypeCodesOfHierarchy = partial(fakeGetTypeCodesOfHierarchy,wn)
        #endregion

        #stub2
        rootDetector = IRootDetector()
        def fakeDetectRoots(self, surface:str, priorPOS:POSTypes = None):
            return ["color"]
        rootDetector.DetectRoots = partial(fakeDetectRoots,rootDetector)

        target = WordPairDefinitionSourceFilter(wn,LinguisticContext.BuildEnglishContext(),fastRootDetector=rootDetector)
        actual,shared = target.ContainsKeywordInTypeHierarchy(WordPair("w1","w2"),NLTKWhitespaceTokenizer(),minRootLength=5,typeDepthRatio=0.5)
        self.assertTrue(actual)

    @patch.multiple(IWordNet, __abstractmethods__=set())
    def test_ContainsKeywordInTypeHierarchy_OneDefReferencingOthersTypeInViaPhraseHierarchy_MatchViaMatchingPhraseSegment(self):
        wn = IWordNet()
        def fakeGetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
            if(word == "aphagia"): return "yet another organism"
            return "another dummy definition"
        def fakeGetTypeCodesOfHierarchy(self,thing:str, sense:SenseStrategy=SenseStrategy.CombineAllSenses, ru:RelationUsage=RelationUsage.CreateAll(), wordPos:POSTypes = None):
            if(thing == "aerophagia"):
                return [TaxonomyType("conrete.n.01"),TaxonomyType("swallow.n.01"),TaxonomyType("living_organism.n.01"),TaxonomyType("entity.n.01")]
            else:
                return []
        wn.GetMergedDefinitions = partial(fakeGetMergedDefinitions,wn)
        wn.GetTypeCodesOfHierarchy = partial(fakeGetTypeCodesOfHierarchy,wn)
        target = WordPairDefinitionSourceFilter(wn,LinguisticContext.BuildEnglishContext())
        actual,shared = target.ContainsKeywordInTypeHierarchy(WordPair("aerophagia","aphagia"),NLTKWhitespaceTokenizer(),minRootLength=5,typeDepthRatio=0.8)
        self.assertTrue(actual)

    @patch.multiple(IWordNet, __abstractmethods__=set())
    def test_ContainsKeywordInTypeHierarchy_OneDefReferencingOthersTypeInViaPhraseHierarchy_MatchViaFullPhraseMatch(self):
        wn = IWordNet()
        def fakeGetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
            if(word == "word1"): return "type should match with the block red algae"
            return "another dummy definition"
        def fakeGetTypeCodesOfHierarchy(self,thing:str, sense:SenseStrategy=SenseStrategy.CombineAllSenses, ru:RelationUsage=RelationUsage.CreateAll(), wordPos:POSTypes = None):
            if(thing == "word2"):
                return [TaxonomyType("red_algae.n.01"),TaxonomyType("swallow.n.01"),TaxonomyType("living_organism.n.01"),TaxonomyType("entity.n.01")]
            else:
                return []
        wn.GetMergedDefinitions = partial(fakeGetMergedDefinitions,wn)
        wn.GetTypeCodesOfHierarchy = partial(fakeGetTypeCodesOfHierarchy,wn)
        target = WordPairDefinitionSourceFilter(wn,LinguisticContext.BuildEnglishContext())
        actual,shared = target.ContainsKeywordInTypeHierarchy(WordPair("word1","word2"),NLTKWhitespaceTokenizer(),minRootLength=5,typeDepthRatio=0.8)
        self.assertTrue(actual)

    @patch.multiple(IWordNet, __abstractmethods__=set())
    def test_ContainsKeywordInTypeHierarchy_OneDefReferencingOthersTypeViaPhrasePrepositionHierarchy_IgnoreShortSegmentsInPhrases(self):
        wn = IWordNet()
        def fakeGetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
            if(word == "aphagia"): return "description with the preposition of"
            return "another dummy definition"
        def fakeGetTypeCodesOfHierarchy(self,thing:str, sense:SenseStrategy=SenseStrategy.CombineAllSenses, ru:RelationUsage=RelationUsage.CreateAll(), wordPos:POSTypes = None):
            if(thing == "aerophagia"):
                return [TaxonomyType("conrete.n.01"),TaxonomyType("swallow.n.01"),TaxonomyType("part_of_something_organism.n.01"),TaxonomyType("entity.n.01")]
            else:
                return []
        wn.GetMergedDefinitions = partial(fakeGetMergedDefinitions,wn)
        wn.GetTypeCodesOfHierarchy = partial(fakeGetTypeCodesOfHierarchy,wn)
        target = WordPairDefinitionSourceFilter(wn,LinguisticContext.BuildEnglishContext())
        actual,shared = target.ContainsKeywordInTypeHierarchy(WordPair("aerophagia","aphagia"),NLTKWhitespaceTokenizer(),minRootLength=5, typeDepthRatio=0.8)
        self.assertFalse(actual)

    @patch.multiple(IWordNet, __abstractmethods__=set())
    def test_ContainsKeywordInTypeHierarchy_MultiSenseAndNoReferenceButEntity_ReturnFalse(self):
        wn = IWordNet()
        def fakeGetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
            if(word == "aphagia"): return "an arbitrary entity "
            return "another dummy definition"
        def fakeGetTypeCodesOfHierarchy(self,thing:str, sense:SenseStrategy=SenseStrategy.CombineAllSenses, ru:RelationUsage=RelationUsage.CreateAll(), wordPos:POSTypes = None):
            if(thing == "aerophagia"):
                return [TaxonomyType("swallow.n.01"),TaxonomyType("another.n.01"),TaxonomyType("another.n.02"),TaxonomyType("person.n.01"),TaxonomyType("living_thing.n.01"),TaxonomyType("thing.n.01"),TaxonomyType("entity.n.01")]
            else:
                return []
        wn.GetMergedDefinitions = partial(fakeGetMergedDefinitions,wn)
        wn.GetTypeCodesOfHierarchy = partial(fakeGetTypeCodesOfHierarchy,wn)
        target = WordPairDefinitionSourceFilter(wn,LinguisticContext.BuildEnglishContext())
        actual,shared = target.ContainsKeywordInTypeHierarchy(WordPair("aerophagia","aphagia"),NLTKWhitespaceTokenizer(),minRootLength=5,typeDepthRatio=0.7)
        self.assertFalse(actual)

    @patch.multiple(IWordNet, __abstractmethods__=set())
    def test_ContainsKeywordInTypeHierarchy_NoWordLengthFilteringForRawMatches_True(self):      #lamb'i match ettirirken minword filter'lara takılmalı
        wn = IWordNet()
        def fakeGetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
            if(word == "w2"): return "skin of a lamb"
            return ""
        def fakeGetTypeCodesOfHierarchy(self,thing:str, sense:SenseStrategy=SenseStrategy.CombineAllSenses, ru:RelationUsage=RelationUsage.CreateAll(), wordPos:POSTypes = None):
            if(thing == "w1"):
                return [TaxonomyType("lamb.n.01"),TaxonomyType("animal.n.01"),TaxonomyType("entity.n.01")]
            else:
                return []
        wn.GetMergedDefinitions = partial(fakeGetMergedDefinitions,wn)
        wn.GetTypeCodesOfHierarchy = partial(fakeGetTypeCodesOfHierarchy,wn)
        target = WordPairDefinitionSourceFilter(wn,LinguisticContext.BuildEnglishContext())
        actual,shared = target.ContainsKeywordInTypeHierarchy(WordPair("w2","w1"),NLTKWhitespaceTokenizer(),minRootLength=5,typeDepthRatio=1)       #MinRoot
        self.assertTrue(actual)


    def test_TrimTypesByDepthRatio_TwoSensesWithFullDepth(self):
        types = [TaxonomyType("gokhan.n.01"),TaxonomyType("yazılımcı.n.01"),TaxonomyType("insan.n.01"),TaxonomyType("entity.n.01"),
                 TaxonomyType("basketbolcu.n.01"),TaxonomyType("sporcu.n.01"),TaxonomyType("insan.n.01"),TaxonomyType("entity.n.01")]
        types = WordPairDefinitionSourceFilter._TrimTypesByDepthRatio("entity.n.01",types,1)
        self.assertEqual(8,len(types))

    def test_TrimTypesByDepthRatio_SingleWithHalfDepth_ReturnFirstHalf(self):
        types = [TaxonomyType("gokhan.n.01"),TaxonomyType("yazılımcı.n.01"),TaxonomyType("insan.n.01"),TaxonomyType("entity.n.01")]
        types = WordPairDefinitionSourceFilter._TrimTypesByDepthRatio("entity.n.01",types,0.5)
        self.assertEqual(2,len(types))

    def test_TrimTypesByDepthRatio_HierWithNoEntity_NoEffectiveTypes(self):
        types = [TaxonomyType("gokhan.n.01"),TaxonomyType("yazılımcı.n.01"),TaxonomyType("insan.n.01")]
        types = WordPairDefinitionSourceFilter._TrimTypesByDepthRatio("entity.n.01",types,1)
        self.assertEqual(0,len(types))

    def test__DecomposePhrasesOfSets_ENTypeCodes_SplitUnderscores(self):
        actual = WordPairDefinitionSourceFilter._DecomposePhrasesOfSets({"science_fiction"},4,False)
        self.assertTrue(actual.__contains__("science"))
        self.assertTrue(actual.__contains__("fiction"))
        self.assertEqual(2,len(actual))

    def test__DecomposePhrasesOfSets_TRTypeCodes_SplitUnderscores(self):
        actual = WordPairDefinitionSourceFilter._DecomposePhrasesOfSets({"bilim adamı"},4, True)
        self.assertTrue(actual.__contains__("bilim"))
        self.assertTrue(actual.__contains__("adamı"))
        self.assertTrue(actual.__contains__("bilim adamı"))
        self.assertEqual(3,len(actual))


if __name__ == "__main__":
    unittest.main()
