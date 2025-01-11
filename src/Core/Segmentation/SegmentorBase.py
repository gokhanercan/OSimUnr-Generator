import unittest
from abc import ABC, abstractmethod
from typing import List, Iterator, Iterable, Dict
from unittest import TestCase
from unittest.mock import patch

from src.Core.IConfigValueable import IConfigValueable
from src.Core.Morphology.SegmentedWord import SegmentedWord
from src.Core.Segmentation.Tokenizers.ITokenizer import ITokenizer


class SegmentorBase(ITokenizer, IConfigValueable):
    """
    Performs word-level segmentation. Sentence-level segmentation will be referred to as Disambiguator.
    Segment order is important. There can be multiple instances of the same segment.
    Implementations are assumed to perform morphological annotation. If they don't, conventions like root+affix+affix are used.
    If it has no relation to morphology, ``ITokenizer`` should be used.
    """
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def SegmentImpl(self, word: str) -> SegmentedWord:
        pass

    def Segment(self, word: str) -> SegmentedWord:
        return self.SegmentImpl(word)

    def Tokenize(self, text: str) -> Iterable[str]:
        """Works under the assumption of prefixes + root + suffixes."""
        sword = self.Segment(text)
        return sword.ToMorphemes()

    def SegmentMultipleImpl(self, words: Iterable[str]) -> Dict[str, SegmentedWord]:
        """
        Can be overridden by those wanting to implement a more optimal version (e.g., Service Wrappers).
        """
        dict = {}
        for word in words:
            dict[word] = self.Segment(word)
        return dict

    def SegmentMultiple(self, words: Iterable[str]) -> Dict[str, SegmentedWord]:
        return self.SegmentMultipleImpl(words)

    @staticmethod
    def ParseConfigValue(cfgvalue: str):
        pair = cfgvalue.split("|")
        key = pair[0]
        params = None
        if len(pair) > 1:
            params = pair[1].split(',')
        cfg = key, params
        return cfg


class SegmentorBaseTest(TestCase):

    @patch.multiple(SegmentorBase, __abstractmethods__=set())  # Stub creation. https://stackoverflow.com/questions/9757299/python-testing-an-abstract-base-class
    def test_ParseConfigValue_FullWithMultipleParams_Parse(self):
        target = SegmentorBase()
        actual = target.ParseConfigValue("nlpt|turkish_dictionary2,turkish_finite_state_machine2")
        self.assertEqual("nlpt", actual[0])
        self.assertEqual("turkish_dictionary2", actual[1][0])
        self.assertEqual("turkish_finite_state_machine2", actual[1][1])

    @patch.multiple(SegmentorBase, __abstractmethods__=set())
    def test_ParseConfigValue_NoParams_Parse(self):
        target = SegmentorBase()
        actual = target.ParseConfigValue("inmem")
        self.assertEqual("inmem", actual[0])
        self.assertIsNone(actual[1])

    @patch.multiple(SegmentorBase, __abstractmethods__=set())
    def test_Iterate_FullMorphologyWithRecurringMorphemes_PreserveRecurringOrdering(self):
        from functools import partial
        target = SegmentorBase()
        def fake(self, word: str):
            return SegmentedWord("root", ["suf1", "suf1", "suf2"], prefixes=["pre"])
        target.Segment = partial(fake, target)
        actual = list(target.Tokenize("dummy"))
        self.assertEqual(5, len(actual))
        self.assertEqual("pre", actual[0])
        self.assertEqual("root", actual[1])
        self.assertEqual("suf2", actual[4])


if __name__ == '__main__':
    unittest.main()
