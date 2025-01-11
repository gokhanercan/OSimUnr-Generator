# coding=utf-8
import unittest
from typing import Dict, Set, Optional
from unittest import TestCase, skip

from src.Core.IWordSource import IWordSource
from src.Core.Morphology.MorphoLex.MorphoLexSegmentedDataset import MorphoLexSegmentedDataset
from src.Core.Morphology.SegmentedWord import SegmentedWord
from src.Core.Morphology.Stemmers.IStemmer import IStemmer
from src.Core.Morphology.Stemmers.MorphyInflectionalEnglishStemmer import MorphyInflectionalEnglishStemmer
from src.Tools import Resources, FormatHelper
from src.Tools.Logger import logp


class MorphoLexEnglishMorphologicalSegmentor(MorphoLexSegmentedDataset):
    """
    A generative analyzer converted from the MorphoLex ready derivational dataset with simple stemmer algorithms.
    In fact, MorphoLex also includes many inflection scenarios by canceling inflectional suffixes like ing, s, ed. For example: elevate, elevated, elevates
    But we implement extra inflection in case not all words are present.
    """
    def __init__(self, dsFilePath: str, autoLoad: bool = True, loadMetadataOnly: bool = False,caseSensitive=True, extraLexicon:IWordSource = None, stemmer:IStemmer = None) -> None:
        super().__init__(dsFilePath, autoLoad, loadMetadataOnly, caseSensitive)
        self.ExtraLexicon = extraLexicon
        if(not stemmer): self.Stemmer:IStemmer = MorphyInflectionalEnglishStemmer()
        self._Lexicon:set[str] = None
        from src.Core.WordNet.IWordNet import IWordNet
        self.WordNet:IWordNet

    def SegmentImpl(self, word: str) -> SegmentedWord:
        expr = self.Segmentations.get(word)
        if(expr is None):       #If OOV dataset! If not in the dataset, stem comes into play. MorphoLex actually includes many inflectional forms.
            stemmedWord = self._StemOrNone(word)        #inflectional
            if(stemmedWord):        #stem does exist.
                expr = self.Segmentations.get(stemmedWord)
                if(expr):
                    return super().SegmentImpl(stemmedWord)
                else:
                    #Simple Suffixation (Derivational)
                    sword = self._ApplySimpleSuffixations(word)
                    if(not sword): return SegmentedWord(word)
                    return sword
            else:
                #Simple Suffixation (Derivational)
                sword = self._ApplySimpleSuffixations(word)
                if(not sword): return SegmentedWord(word)
                return sword
        return super().SegmentImpl(word)

    def _StemOrNone(self, word:str)->Optional[str]:
        """
        If it does not return a different stem, it returns None.
        Manually stems for ing.
        :param word:
        :return:
        """
        stemmedWord:str = self.Stemmer.Stem(word)
        if(stemmedWord):        #stem does exist.
            if(stemmedWord != word): return stemmedWord
        else:
            #In case the stemmer (Morphy) cannot solve ing, we perform an extra manual ing suffixation process.
            if(word.endswith("ing")):
                mutated:str = word[:len(word)-len("ing")]       #I stem ing but actually this creates a new noun, i.e., derivational. But since MorphoLex does not accept ing as derivation, this is my solution for now. If I include it among the suffixes, I will conflict with MorphoLex's ready analyses.
                if(mutated in self._GetLexicon()):
                    return mutated
        return None

    def _GetLexicon(self):
        if self._Lexicon is None:
            morphlexLexicon:Set[str] = self.Roots.union(self.Segmentations.keys())       #We consider both Root and Surface as lexicon.
            logp("Using MorphoLex's roots and surfaces as the base lexicon. Total: " + str(len(morphlexLexicon)))
            if(self.ExtraLexicon):
                logp("Loading extra lexicon from IWordSource: " + str(type(self.ExtraLexicon)) + " ...",True)
                wordnetLexicon = self.ExtraLexicon.GetWords()
                logp("ExtraLexicon size: " + str(len(wordnetLexicon)))
                finalLexicon:Set[str] = morphlexLexicon.union(wordnetLexicon)
                self._Lexicon = finalLexicon
                logp("Using combined MorphoLex and ExtraLexicon as lexicon. Total: " + str(len(self._Lexicon)))
            else:
                self._Lexicon = morphlexLexicon
        return self._Lexicon

    def _ApplySimpleSuffixations(self, word:str)->Optional[SegmentedWord]:
        """
        We try to find a valid analysis in the dictionary with one level of suffix and prefix additions.
        This block is largely copied from EnglishRootDetectionStack. Because it actually needs to use the analyzer directly.

        :param word:
        :return:
        """
        #OneLevelPrefixRemoval
        for prefix in self.MetaPrefixes:
            pre = prefix.lower()
            starts:bool = word.startswith(pre)
            if (not starts): continue
            mutated:str = word[len(pre):]
            if (mutated in self._GetLexicon()):
                exprMutated = self.Segmentations.get(mutated)           #If it has segmentation, it already has lexicon in the previous line.
                if(exprMutated):
                    sword = self.TryParseToSegmentedWordOrDefault(exprMutated)
                    sword.Prefixes.insert(0,pre)    #We add it to the beginning in case it is a prefix in the original parse.
                else:
                    sword = SegmentedWord(mutated)
                    sword.Prefixes.insert(0,pre)
                return sword

        #OneLevelSuffixRemoval
        for suffix in self.MetaSuffixes:
            suf = suffix.lower()
            ends:bool = word.endswith(suf)
            if (not ends): continue
            mutated:str = word[:len(word)-len(suf)]
            if (mutated in self._GetLexicon()):
                exprMutated = self.Segmentations.get(mutated)           #If it has segmentation, it already has lexicon in the previous line.
                if(exprMutated):
                    sword = self.TryParseToSegmentedWordOrDefault(exprMutated)
                    sword.Suffixes.append(suf)          #It should come at the end of the original parse.
                else:
                    sword = SegmentedWord(mutated)
                    sword.Suffixes.append(suf)
                return sword
        return None

    @staticmethod
    def LoadFromText(path:str, loadMetadatas:bool = False, caseSensitive:bool = True, extraLexicon:IWordSource = None):
        dsWrapper:MorphoLexEnglishMorphologicalSegmentor = MorphoLexEnglishMorphologicalSegmentor(path,autoLoad=False, caseSensitive=caseSensitive,extraLexicon= extraLexicon, stemmer=None)
        dsOriginal = MorphoLexSegmentedDataset.LoadFromText(path,loadMetadatas,caseSensitive)
        dsWrapper.Segmentations = dsOriginal.Segmentations
        dsWrapper.Roots = dsOriginal.Roots
        dsWrapper.MetaSuffixes = dsOriginal.MetaSuffixes
        dsWrapper.MetaPrefixes = dsOriginal.MetaPrefixes
        return dsWrapper

class MorphoLexEnglishMorphologicalSegmentorIntegrationTest(TestCase):

    def test_ApplySimpleSuffixations_HasSegmentationAfterSuffixation(self):
        analyzer:MorphoLexEnglishMorphologicalSegmentor = MorphoLexEnglishMorphologicalSegmentor("",autoLoad=False)
        analyzer.MetaSuffixes = {"ER"}
        analyzer._Lexicon = {"cinematograph"}
        analyzer.Segmentations["cinematograph"]="{(cinema)}>tograph>]"
        sword:SegmentedWord = analyzer._ApplySimpleSuffixations("cinematographer")
        self.assertEqual("_cinema+tograph+er",sword.BuildUnitExpression())

    def test_ApplySimpleSuffixations_HasNoSegmentationAfterSuffixationButInLexicon(self):
        analyzer:MorphoLexEnglishMorphologicalSegmentor = MorphoLexEnglishMorphologicalSegmentor("",autoLoad=False)
        analyzer.MetaSuffixes = {"ER"}
        analyzer._Lexicon = {"cinematograph"}
        sword:SegmentedWord = analyzer._ApplySimpleSuffixations("cinematographer")
        self.assertEqual("_cinematograph+er",sword.BuildUnitExpression())

    def test_ApplySimpleSuffixations_HasNoSegmentationAfterPrefixationButInLexicon(self):
        analyzer:MorphoLexEnglishMorphologicalSegmentor = MorphoLexEnglishMorphologicalSegmentor("",autoLoad=False)
        analyzer.MetaPrefixes = {"A"}
        analyzer._Lexicon = {"social"}
        sword:SegmentedWord = analyzer._ApplySimpleSuffixations("asocial")
        self.assertEqual("-a_social",sword.BuildUnitExpression())

    def test_ApplySimpleSuffixations_HasSegmentationAfterPrefixation(self):
        analyzer:MorphoLexEnglishMorphologicalSegmentor = MorphoLexEnglishMorphologicalSegmentor("",autoLoad=False)
        analyzer.MetaPrefixes = {"PRE"}
        analyzer.Segmentations["caution"] = "{(caut)>ion>}"
        analyzer._Lexicon = {"caution"}
        sword:SegmentedWord = analyzer._ApplySimpleSuffixations("precaution")
        self.assertEqual("-pre_caut+ion",sword.BuildUnitExpression())

    def test_ALL_ENGLISH_MORPHOLOGICAL_ANALYSIS_SCENARIOS_intergration(self):       #integration test
        from pandas import DataFrame
        from tabulate import tabulate
        txtpath: str = Resources.GetOthersPath("MorphoLEX2.txt")
        from src.Core.WordNet.NLTKWordNetWrapper import NLTKWordNetWrapper
        extraLexicon:IWordSource = NLTKWordNetWrapper()
        analyzer: MorphoLexEnglishMorphologicalSegmentor = MorphoLexEnglishMorphologicalSegmentor.LoadFromText(
            txtpath, loadMetadatas=True, caseSensitive=False, extraLexicon=extraLexicon)

        #scenarios
        cases:Dict[str,str] = {}            #word, expectedExpr
        cases["revisioning"] = "-re_vise+ion"      #Actually it escapes from the stemmer but I solved the ing's for simple suffixation myself.
        cases["description"] = "-de_script+ion"             #Directly in morphlex. There is an extra suffix and plus at the end.
        cases["flies"] = "_fly"
        cases["script"] = "_script"                     #single root
        cases["broadcast"] = "_broad_cast"              #the second root is treated as a suffix! Will this cause a problem??
        cases["scripting"] = "_script"                  #MorphoLex oov. ing is removed by stem.
        cases["rebroadcast"] = "-re_broad_cast"         #OOV
        cases["cinematographer"] = "_cinema+tograph+er"     #OOV but after the stem, er goes and the remaining is INVoc.
        cases["worthwhileness"] = "_worth_while+ness"         #OOV in MorphoLex, exists in WordNet. Simple suffixation parses +ness
        cases["sustaining"] = "-sus_tain"           #the original word itself should not return as another root suggestion. sustain should not return as another root here.

        df = DataFrame()
        index = 1
        anyFail = False
        for word,expectedExpr in cases.items():
            sword:SegmentedWord = analyzer.Segment(word)
            actualExpr:str = sword.BuildUnitExpression()
            df.at[index,"Word"] = word
            df.at[index,"Expected"] = expectedExpr
            df.at[index,"Actual"] = actualExpr
            passed:bool = expectedExpr == actualExpr
            if not passed: anyFail = True
            self.assertTrue(passed, word + "-> actual: '" + actualExpr + "' != " + " expected: '" + expectedExpr + "'")
            index = index + 1
        if(not anyFail): self.assertTrue("All " + str(index) + " passed!")
        print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=FormatHelper._ThreeDigitFormat))       #Prints the table to the screen if all tests pass.

if __name__ == "__main__":
    unittest.main()     #NOTE: Delete cython version first in order to run unit tests!

