# coding=utf-8
from abc import abstractmethod
from typing import Optional
from unittest import TestCase

from src.Core.Dataset.DiscreteScale import DiscreteScale


class IWordSimilarity(object):
    """
    The semantic, syntactic, or orthographic similarity between two words in the range of (0-1).
    It can represent similarity in any sense.
    """
    @abstractmethod
    def WordSimilarity(self, w1: str, w2: str) -> Optional[float]:
        pass

    @staticmethod
    def ApplyScaling(score: Optional[float], scoreScale: DiscreteScale, finalScale: DiscreteScale) -> Optional[float]:
        """
        Provides a static MinMax scaling algorithm.
        Not only scales but also returns the min or max values in finalScale if the given scores exceed the boundary limits.
        Example: If you send 10.1 on a 0-10 scale, it converts it to 10.
        :param self:
        :param score: The original score to be scaled.
        :param w1:
        :param w2:
        :param scoreScale: The scale of the original score.
        :param finalScale: The scale to which it will be converted.
        :return:
        """
        if(score is None): return None
        if(not scoreScale): raise Exception("The WordSim source did not provide the DiscreteScale type SimilarityScale information that specifies the scale of the given score!")
        if(not scoreScale.IsNormalized()): return score

        # Validate boundary cases
        if finalScale is None: return score  # If no finalScale is given, return the original score without scaling.
        if (not finalScale.IsNormalized()): return score  # If the finalScale is open, again cannot scale, so return the original score.
        if(scoreScale.Max == 0): return 0  # If max is 0, the entire dataset is 0, and the given score is also 0.

        # Scale the original score
        scoreDiff = scoreScale.Max - scoreScale.Min
        scorePerc = (score - scoreScale.Min) / scoreDiff

        # Add the original score to the final and scale the final
        finalDiff = finalScale.Max - finalScale.Min
        f = finalScale.Min + (scorePerc * finalDiff)

        # Return minmax if out-of-bounds
        if(f > finalScale.Max): return finalScale.Max
        if(f < finalScale.Min): return finalScale.Min
        return f

    def WordSimilarityInScale(self, w1: str, w2: str, finalScale: DiscreteScale) -> Optional[float]:
        """
        Returns the value not with the original scale but with the desired scale.
        :param w1:
        :param w2:
        :param finalScale:
        :return:
        """
        score = self.WordSimilarity(w1, w2)
        return self.ApplyScaling(score, self.SimilarityScale(), finalScale)

    @abstractmethod
    def SimilarityScale(self) -> DiscreteScale:
        """
        Indicates the scale in which the scores are returned.
        :return:
        """
        pass


class IWordSimilarityTest(TestCase):

    def test_ApplyScaling_MinIsNotZero(self):
        dsScale = DiscreteScale(1, 5)  # I later realized that MTurk771 is 1-5. The unrelated region looked completely empty.
        self.assertEqual(0,   IWordSimilarity.ApplyScaling(1, dsScale, DiscreteScale(0, 1)))
        self.assertEqual(0.25, IWordSimilarity.ApplyScaling(2, dsScale, DiscreteScale(0, 1)))
        self.assertEqual(0.5, IWordSimilarity.ApplyScaling(3, dsScale, DiscreteScale(0, 1)))
        self.assertEqual(0.75, IWordSimilarity.ApplyScaling(4, dsScale, DiscreteScale(0, 1)))
        self.assertEqual(1,   IWordSimilarity.ApplyScaling(5, dsScale, DiscreteScale(0, 1)))
        # Out of bounds
        self.assertEqual(0,   IWordSimilarity.ApplyScaling(0, dsScale, DiscreteScale(0, 1)))
        self.assertEqual(1,   IWordSimilarity.ApplyScaling(6, dsScale, DiscreteScale(0, 1)))

    def test_ApplyScaling_SameScales_ReturnSame(self):
        self.assertEqual(0.45, IWordSimilarity.ApplyScaling(0.45, DiscreteScale(0, 1), DiscreteScale(0, 1)))
        self.assertEqual(0, IWordSimilarity.ApplyScaling(0, DiscreteScale(0, 1), DiscreteScale(0, 1)))
        self.assertEqual(1, IWordSimilarity.ApplyScaling(1, DiscreteScale(0, 1), DiscreteScale(0, 1)))
        # Out of bounds
        self.assertEqual(0, IWordSimilarity.ApplyScaling(-0.004, DiscreteScale(0, 1), DiscreteScale(0, 1)))
        self.assertEqual(1, IWordSimilarity.ApplyScaling(1.000001, DiscreteScale(0, 1), DiscreteScale(0, 1)))

    def test_ApplyScaling_DiffScale_Scale(self):
        self.assertEqual(4.5, IWordSimilarity.ApplyScaling(0.45, DiscreteScale(0, 1), DiscreteScale(0, 10)))
        self.assertEqual(0, IWordSimilarity.ApplyScaling(0, DiscreteScale(0, 1), DiscreteScale(0, 10)))
        self.assertEqual(10, IWordSimilarity.ApplyScaling(1, DiscreteScale(0, 1), DiscreteScale(0, 10)))
        # Out of bounds
        self.assertEqual(0, IWordSimilarity.ApplyScaling(-0.001, DiscreteScale(0, 1), DiscreteScale(0, 10)))
        self.assertEqual(10, IWordSimilarity.ApplyScaling(1.1111, DiscreteScale(0, 1), DiscreteScale(0, 10)))
