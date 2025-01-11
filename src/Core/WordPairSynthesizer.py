# coding=utf-8
import random
import unittest
from typing import List
from unittest import TestCase

from src.Core.WordPair import WordPair


class WordPairSynthesizer(object):

    def GeneratePossibleWordPairs(self, uniqueWords: List[str], allowSameWordsInAPair: bool = False, allowSymetricalPairs=False):
        """
        Combines all possible word pairs.
        Implemented with a Python generator. https://anandology.com/python-practice-book/iterators.html
        Cython does not support generators, if I remember correctly.
        :param wordSource:
        :param allowSymetSameWordsInAPair: Do not allow the reverse order of the same pair.
        :param uniqueWords: Words must be sent as unique.
        :return:
        """
        for i in range(0, len(uniqueWords)):
            w1: str = uniqueWords[i]
            for j in range(0 + i, len(uniqueWords)):
                w2: str = uniqueWords[j]
                if (not allowSameWordsInAPair) and (i == j):
                    continue  # The same word pair, this can also be made optional in the future.

                # Do
                wp: WordPair = None
                if (not allowSymetricalPairs):
                    firstOneSmall: bool = w1 < w2
                    wp = WordPair(w1, w2) if firstOneSmall else WordPair(w2, w1)  # The smaller word always comes first.
                else:
                    wp: WordPair = WordPair(w1, w2)
                yield wp

    def GenerateRandomWordPairs(self, words: List[str], resultLimit: int = 100):
        """
        Continuously selects random pairs from the given set.
        :param resultLimit: How many generated word pairs are required. Mandatory.
        :param uniqueWords:
        :return:
        """
        generated: int = 0
        while (generated < resultLimit):
            i1: int = random.randint(0, len(words) - 1)
            i2: int = random.randint(0, len(words) - 1)
            w1: str = words[i1]
            w2: str = words[i2]
            generated += 1
            yield WordPair(w1, w2)

class WordPairSynthesizerTest(TestCase):

    def test_GeneratePossibleWordPairs_RegularSet_AvoidSymetricalDuplicates(self):
        words = ["gokhan", "ercan", "ahmet"]

        wpGenerator = WordPairSynthesizer().GeneratePossibleWordPairs(words, allowSymetricalPairs=False, allowSameWordsInAPair=False)
        results = []
        for wp in wpGenerator:
            results.append(wp)

        self.assertEqual(3, len(results))

if __name__ == '__main__':
    unittest.main()
