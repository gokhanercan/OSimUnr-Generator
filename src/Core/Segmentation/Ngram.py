import unittest
from collections import OrderedDict
from typing import List
from unittest import TestCase

from src.Core.Morphology.SegmentedWord import SegmentedWord
from src.Core.Segmentation.IGramExtractor import IGramExtractor, ICountableGramExtractor
from src.Core.Segmentation.SegmentorBase import SegmentorBase


class Ngram(IGramExtractor,ICountableGramExtractor,SegmentorBase):
    """
    Initially, the default usage is as an IGramExtractor: it produces distinct n-grams along with their frequencies.
    However, when used as a Segmentor, it can optionally return ordered and recurring items.
    QGram uses this Segmentor but is a completely different StringDistance measure.
    """

    def __init__(self,n:int) -> None:
        super().__init__()
        self.N:int = n

    def ExtractGramsWithCounts(self, word:str)-> 'Dict[str]':
        """
        Since it uses a dict, it does not return shingles/ngrams/qgrams in order. It also counts how many of each gram there are.
        :param word:
        :return:
        """
        grams = dict()
        for i in range(len(word) - self.N + 1):
            shingle = word[i:i + self.N]
            old = grams.get(shingle)
            if old:
                grams[str(shingle)] = int(old + 1)
            else:
                grams[str(shingle)] = 1
        return grams


    def ExtractOrderedGramsWithCounts(self, word: str) -> 'Dict[str]':
        """
        Unlike the other, it returns an ordered list so it can also be used in Segmentation.
        :param word:
        :return:
        """
        grams = OrderedDict()
        for i in range(len(word) - self.N + 1):
            shingle = word[i:i + self.N]
            old = grams.get(shingle)
            if old:
                grams[str(shingle)] = int(old + 1)
            else:
                grams[str(shingle)] = 1
        return grams

    def ExtractGrams(self, word: str)-> 'Set[str]':
        """
        Only returns distinct grams. Does not preserve order.
        DRY note: To avoid performance issues, I did not use the dict-returning method above to prevent unnecessary datatype creation.
        :param word:
        :return:
        """
        grams = set()
        for i in range(len(word) - self.N + 1):
            gram = word[i:i + self.N]
            if(not grams in grams):
                grams.add(gram)
        return grams

    def ExtractRecurringGrams(self, word: str) -> 'List[str]':
        """
        In its simplest form, it returns n-grams that repeat the same segments like a Tokenizer or Segmentor.
        :argument
        :param word:
        :return:
        """
        grams = list()
        for i in range(len(word) - self.N + 1):
            gram = word[i:i + self.N]
            grams.append(gram)
        return grams

    def SegmentImpl(self, word: str)-> SegmentedWord:
        """
        When used as a Segmentor, it works in ordered and recurring mode. Uses ExtractRecurringGrams.
        :param word:
        :return:
        """
        grams:List[str] = self.ExtractRecurringGrams(word)
        sword:SegmentedWord = SegmentedWord.FromStrList(grams)
        return sword

    def ToConfigValue(self) -> str:
        return "ngr" + str(self.N)


class NgramSegmentorTest(TestCase):

    def test_ExtractGrams_2Gram_2GramWithRecurringGrams(self):
        actual = Ngram(2).ExtractGrams("gokhango")
        self.assertEqual(6,actual.__len__())

    def test_ExtractOrderedGrams_2Gram_2GramWithRecurringGrams(self):
        actual:OrderedDict = Ngram(2).ExtractOrderedGramsWithCounts("gokhango")
        actualList = list(actual)
        self.assertEqual(6,actual.__len__())
        self.assertEqual("go",actualList[0])

    def test_ExtractRecurringGrams_2Gram_2GramWithRecurringGrams(self):
        actual = Ngram(2).ExtractRecurringGrams("gokhango")
        actualList = list(actual)
        self.assertEqual(7,actual.__len__())
        self.assertEqual("go",actualList[0])
        self.assertEqual("go",actualList[6])

    def test_SegmentImpl_2Gram_2GramWithRecurringGrams_PreserveRecurringsAsASegmentor(self):
        actual:SegmentedWord = Ngram(2).Segment("gokhango")
        self.assertEqual("go",actual.Root)
        self.assertEqual("ok",actual.Suffixes[0])
        self.assertEqual(0,actual.Prefixes.__len__())
        self.assertEqual(6,actual.SuffixCount())

if __name__ == '__main__':
    unittest.main()