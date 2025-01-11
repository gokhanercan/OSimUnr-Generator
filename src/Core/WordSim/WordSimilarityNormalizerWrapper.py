# coding=utf-8
import unittest
from typing import Optional, List, Dict
from unittest import TestCase

from src.Core.Dataset.DiscreteScale import DiscreteScale
from src.Core.WordPair import WordPair
from src.Core.WordSim.IWordSimilarity import IWordSimilarity
from src.Core.WordSim.WordSimDataset import WordSimDataset
from src.Tools import ValueHelper
from src.Tools.Logger import logp
from src.Tools.Progressor import Progressor


class WordSimilarityNormalizerWrapper(IWordSimilarity):
    """
    Enables Min-Max scaling of the WordSimilarity model by assuming the min-max values of a specific wordpair set.
    It makes sense to use it for models with 'open' scale values.
    If there are POSITIVE_INFINITIVE values in the series, it sets them to the series max.
    """

    def __init__(self, wrappedWordSimilarity: IWordSimilarity, wordpairs: List[WordPair], normalizationScale: DiscreteScale) -> None:
        """
        Automatically normalizes any IWordSimilarity model by wrapping it.
        :param wrappedWordSimilarity:
        :param wordPairs:
        :param finalScale: The scale to be achieved as a result.
        """
        super().__init__()
        self._WrappedWordSimilarity = wrappedWordSimilarity
        self.OriginalWordPairs: List[WordPair] = wordpairs
        self.NormalizationScale: DiscreteScale = normalizationScale
        self._ScaledScores: Dict[WordPair, float] = None
        self._IsNormalized = False
        if(len(wordpairs) <= 10):
            logp("Min-max normalization may not give good results with such a small wordpair list!!!! Only " + str(len(wordpairs)) + " wordpairs. Ensure at least Min and Max values exist!!")
        self._Normalize()  # Works eagerly along with the ctor stage. Essential because it needs the min/max of the entire dataset!

    def _Normalize(self):
        """
        Does not need to be called externally. Does not manipulate the input dataset.
        Processes and scales all pairs at once.
        The normalized values need to be retrieved later using self._ScaledScores.
        :param wordPairs:
        :return:
        """
        self._ScaledScores: Dict[WordPair, float] = {}
        m: IWordSimilarity = self._WrappedWordSimilarity
        mScale = m.SimilarityScale()

        # Originals
        logp("WordSimilarityNormalizerWrapper.Eagerly normalizing " + str(self.OriginalWordPairs.__len__()) + " wordpairs ...", anyMode=True)
        prog = Progressor(expectedIteration=self.OriginalWordPairs.__len__())
        iter = 0
        for wp in self.OriginalWordPairs:
            # print(str(iter))
            prog.logpif(iter, iterstr="wordpair", progressBatchSize=int(self.OriginalWordPairs.__len__() / 100), anyMode=True)
            sim = m.WordSimilarityInScale(wp.Word1, wp.Word2, self.NormalizationScale)
            self._ScaledScores[wp.ToKey()] = sim
            iter = iter + 1

        # Normalizing
        minval: float = mScale.Min if mScale.Min is not None else min(filter(None, self._ScaledScores.values()))
        inf = ValueHelper.POSITIVE_INF
        maxval: float = max(filter(None,
                            filter(lambda x: x != inf, self._ScaledScores.values())  # Skip INF values while finding max.
                        ))
        dynamicScale = DiscreteScale(minval, maxval)
        i = 0
        for wp in self.OriginalWordPairs:
            wpkey = wp.ToKey()
            sim = self._ScaledScores.get(wpkey)
            if(sim is None): continue
            if(sim == inf): sim = maxval  # If INF exists, set it to max.
            normalized = self.ApplyScaling(sim, dynamicScale, self.NormalizationScale)
            if(normalized is not None):
                self._ScaledScores[wpkey] = normalized
            i = i + 1
        self._IsNormalized = True
        logp("WordSimilarityNormalizerWrapperNormalization completed!", anyMode=True)

    def WordSimilarity(self, w1: str, w2: str) -> Optional[float]:
        return self._ScaledScores[WordPair(w1, w2).ToKey()]

    def WordSimilarityInScale(self, w1: str, w2: str, finalScale: DiscreteScale):
        # The normalized scale and finalScale are still different. FinalScale: The projection scale aimed at the end. Normalization is the result of MinMax scaling.
        if(self._IsNormalized):
            simNormalized = self._ScaledScores.get(WordPair(w1, w2).ToKey())
            if(simNormalized is None):  return None  # OOV
            return self.ApplyScaling(simNormalized, self.SimilarityScale(), finalScale)
        else:
            return self._WrappedWordSimilarity.WordSimilarityInScale(w1, w2, finalScale)

    def SimilarityScale(self) -> DiscreteScale:
        return self.NormalizationScale if self._IsNormalized else self._WrappedWordSimilarity.SimilarityScale()

    def ToNewWordPairs(self):
        """
        Sets the GoldSimilarity field of the WordPairs in the newly returned list.
        :return:
        """
        wp2: List[WordPair] = []
        for owp in self.OriginalWordPairs:
            wp2.append(WordPair(owp.Word1, owp.Word2, self.WordSimilarity(owp.Word1, owp.Word2)))
        return wp2


class WordSimilarityNormalizerWrapperTest(TestCase):

    def test_CtorWrap_NormalizedMetric_ScaleOnly(self):
        ds = WordSimDataset(scale=DiscreteScale(0, 1))
        wps = []
        wps.append(WordPair("wp1_1", "wp1_2", 1))
        wps.append(WordPair("wp2_1", "wp2_2", 0.5))
        ds.LoadWithWordPairs(wps)
        normalizerWrapper = WordSimilarityNormalizerWrapper(ds, wps, DiscreteScale(0, 10))
        self.assertEqual(10, normalizerWrapper.WordSimilarity("wp1_1", "wp1_2"))
        self.assertEqual(5, normalizerWrapper.WordSimilarity("wp2_1", "wp2_2"))

    def test_CtorWrapAndToNewWordPairs_UnnormalizedMetric_Normalize(self):
        ds = WordSimDataset(scale=DiscreteScale(0, 10))
        wps = []
        wps.append(WordPair("wp1_1", "wp1_2", 2))
        wps.append(WordPair("wp2_1", "wp2_2", 5))  # max=5, factor would be x2
        ds.LoadWithWordPairs(wps)
        normalizerWrapper = WordSimilarityNormalizerWrapper(ds, wps, DiscreteScale(0, 10))
        self.assertEqual(4, normalizerWrapper.WordSimilarity("wp1_1", "wp1_2"))
        self.assertEqual(10, normalizerWrapper.WordSimilarity("wp2_1", "wp2_2"))

        normalizedCopy = normalizerWrapper.ToNewWordPairs()
        self.assertEqual(4, normalizedCopy[0].GoldSimilarity)
        self.assertEqual(10, normalizedCopy[1].GoldSimilarity)

if __name__ == "__main__":
    unittest.main()
