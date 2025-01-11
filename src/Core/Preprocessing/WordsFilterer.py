# coding=utf-8
import unittest
from typing import List, Set, Iterable, Tuple
from unittest import TestCase

from src.Core.Preprocessing.Preprocessors import Preprocessors


class WordsFilterer(object):
    """
    Applies various filters to words.
    """
    def __init__(self) -> None:
        super().__init__()

    def ToFiltered(self, words: Iterable[str], minLength: int = None, allowPunctuation: bool = True, allowNumbers: bool = False, allowWhitespaces: bool = False) -> Tuple[List[str], int]:
        """
        Filters words at the word level. Words that do not meet the criteria are filtered out.
        :param words: Iterable of words to filter.
        :param minLength: Minimum length of words to keep.
        :param allowPunctuation: Whether punctuation is allowed in words.
        :param allowNumbers: Can a word be a standalone number, e.g., '333'?
        :param allowWhitespaces: Can a word contain spaces? In other words, do we accept phrases?
        :return: Tuple containing the filtered list of words and the count of removed words.
        """
        anyFiltersOn: bool = (minLength is not None) or (not allowPunctuation) or (not allowNumbers) or (not allowWhitespaces)
        if not anyFiltersOn:
            return list(words), 0
        words2: List[str] = list(words)
        removed: int = 0
        preprocessor: Preprocessors = Preprocessors()
        for w in words:
            # 1-MinLength
            if minLength:
                if len(w) < minLength:
                    words2.remove(w)
                    removed += 1
                    continue
            # 2-AllowPunctuation
            if not allowPunctuation:
                hasPunct: bool = preprocessor.ContainsPunctuation(w)
                if hasPunct:
                    words2.remove(w)
                    removed += 1
                    continue
            # 3-Number
            if not allowNumbers:
                if w.isnumeric():
                    words2.remove(w)
                    removed += 1
                    continue
            # 4-Whitespaces
            if not allowWhitespaces:
                if " " in w:
                    words2.remove(w)
                    removed += 1
                    continue

        return words2, removed


class WordsFiltererTest(TestCase):

    def test_ToFiltered_UnderThresholdWords_Remove(self):
        words = {"gokhan", "test", "ercan", "ercan", "mahsun", "123"}

        wFiltered, removed = WordsFilterer().ToFiltered(words, minLength=5)

        self.assertEqual(3, len(wFiltered))
        self.assertEqual(True, "gokhan" in wFiltered)
        self.assertEqual(True, "mahsun" in wFiltered)
        self.assertEqual(False, "test" in wFiltered)
        self.assertEqual(False, "123" in wFiltered)

    def test_ToFiltered_WordsWithPuncts_RemoveWordsWithPunts(self):
        words = {"gokhan", "gokhan-ercan", "ercan", "fısıldasın;"}

        wFiltered, removed = WordsFilterer().ToFiltered(words, allowPunctuation=False)

        self.assertEqual(2, len(wFiltered))
        self.assertEqual(True, "gokhan" in wFiltered)
        self.assertEqual(True, "ercan" in wFiltered)
        self.assertEqual(False, "gokhan-ercan" in wFiltered)
        self.assertEqual(False, "fısıldasın;" in wFiltered)


if __name__ == '__main__':
    unittest.main()
