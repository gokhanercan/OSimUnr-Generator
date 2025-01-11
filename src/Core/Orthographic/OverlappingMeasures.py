# coding=utf-8
from abc import abstractmethod
from typing import Optional, Set

from src.Core.Dataset.DiscreteScale import DiscreteScale
from src.Core.Orthographic.IStringDistance import INormalizedStringDistance
from src.Core.Segmentation.IGramExtractor import IGramExtractor
from src.Core.WordSim.IWordSimilarity import IWordSimilarity


class OverlappingMeasureBase(IWordSimilarity, INormalizedStringDistance):

    def __init__(self,gramExtractor:IGramExtractor) -> None:
        super().__init__()
        self.GramExtractor= gramExtractor

    def WordSimilarity(self, w1: str, w2: str) -> Optional[float]:
        grams1 = self.GramExtractor.ExtractGrams(w1)
        grams2 = self.GramExtractor.ExtractGrams(w2)
        if(grams1 and grams2):
            return self.MeasureOverlap(grams1,grams2)
        else:
            return 0    # If one of them has no n-grams, there's nothing to do, returning 0. If this gramming cannot match texts of this length, we return 0.

    def SimilarityScale(self) -> DiscreteScale:
        return DiscreteScale(0,1)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.MeasureName() + "_" + self.GramExtractor.ToConfigValue()

    def MeasureOverlap(self, grams1:Set[str],grams2:Set[str])-> Optional[float]:
        if(grams1 is None): return 0
        if(grams2 is None): return 0
        return self._MeasureOverlapImpl(grams1,grams2)

    def NormalizedDistance(self, w1: str, w2: str) -> Optional[float]:
        return 1-self.WordSimilarity(w1,w2)

    def IntersectionCount(self,set1:Set,set2:Set,union:Set):
        """
        Built-in intersections create new sets, this is created to count intersections without initializing new objects.
        If we have the Union, it quickly calculates through set counts without looping unnecessarily.
        :param set1:
        :param set2:
        :param union:
        :return:
        """
        return (len(set1) + len(set2)) - len(union)

    @abstractmethod
    def _MeasureOverlapImpl(self, grams1:Set[str],grams2:Set[str])-> Optional[float]:
        pass

    @abstractmethod
    def MeasureName(self)->str:
        pass

class Dice(OverlappingMeasureBase):
    """
    Dice/Sorensen
    """
    def _MeasureOverlapImpl(self, grams1: Set[str], grams2: Set[str]) -> Optional[float]:
        union = grams1.union(grams2)
        inter = self.IntersectionCount(grams1,grams2,union)
        return 2.0 * inter / (len(grams1) + len(grams2))

    def MeasureName(self) -> str:
        return "dice"

class Jaccard(OverlappingMeasureBase):

    def _MeasureOverlapImpl(self, grams1: Set[str], grams2: Set[str]) -> Optional[float]:
        union = grams1.union(grams2)
        inter = self.IntersectionCount(grams1,grams2,union)
        return inter / len(union)

    def MeasureName(self) -> str:
        return "jacc"


class OverlapCoefficient(OverlappingMeasureBase):

    def _MeasureOverlapImpl(self, grams1: Set[str], grams2: Set[str]) -> Optional[float]:
        union = grams1.union(grams2)
        inter = self.IntersectionCount(grams1,grams2,union)
        return inter / min(len(grams1),len(grams2))

    def MeasureName(self) -> str:
        return "over"
