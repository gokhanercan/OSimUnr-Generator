import unittest
from unittest import TestCase

from src.Core.Orthographic.OverlappingMeasures import Dice, Jaccard, OverlapCoefficient
from src.Core.Segmentation.Ngram import Ngram


class OverlappingMeasuresTests(TestCase):

    #Dice
    def test_AnyMeasure_MeasureOverlapImpl_NoGrams_0(self):
        self.assertEqual(0,Dice(None)._MeasureOverlapImpl(set(), {"gokhan","ercan"}))

    def test_Dice_MeasureOverlapImpl_SameWords_1(self):
        self.assertEqual(1,Dice(None)._MeasureOverlapImpl({"gokhan","ercan"}, {"gokhan","ercan"}))

    def test_Dice_MeasureOverlapImpl_NoOverlaps_0(self):
        self.assertEqual(0,Dice(None)._MeasureOverlapImpl({"gokhan","ercan"}, {"ahmet","ayse"}))

    def test_Dice_MeasureOverlapImpl_HalfMatch_066(self):
        self.assertEqual(2/3,Dice(None)._MeasureOverlapImpl({"gokhan","ercan"}, {"gokhan"}))

    #Jaccard
    def test_Jaccard_MeasureOverlapImpl_SameWords_1(self):
        self.assertEqual(1,Jaccard(None)._MeasureOverlapImpl({"gokhan","ercan"}, {"gokhan","ercan"}))

    def test_Jaccard_MeasureOverlapImpl_NoOverlaps_0(self):
        self.assertEqual(0,Jaccard(None)._MeasureOverlapImpl({"gokhan","ercan"}, {"ahmet","ayse"}))

    def test_Dice_MeasureOverlapImpl_HalfMatch_05(self):
        self.assertEqual(1/2,Jaccard(None)._MeasureOverlapImpl({"gokhan","ercan"}, {"gokhan"}))

    #Overlap Coefficient
    def test_Overlap_MeasureOverlapImpl_SameWords_1(self):
        self.assertEqual(1,OverlapCoefficient(None)._MeasureOverlapImpl({"gokhan","ercan"}, {"gokhan","ercan"}))

    def test_Overlap_MeasureOverlapImpl_NoOverlaps_0(self):
        self.assertEqual(0,OverlapCoefficient(None)._MeasureOverlapImpl({"gokhan","ercan"}, {"ahmet","ayse"}))

    def test_Overlap_MeasureOverlapImpl_HalfMatch_05(self):
        self.assertEqual(1,OverlapCoefficient(None)._MeasureOverlapImpl({"gokhan","ercan"}, {"gokhan"}))

    #With Segmentor
    def test_AnyMeasure_WordSimilarity_WithNgramExtractor_NoGramsToGenerate_0(self):
        self.assertEqual(0,Dice(Ngram(2)).WordSimilarity("a","gokhan"))

    def test_AnyMeasure_WordSimilarity_WithNgramAsExtractor_DistinctGrams_Half(self):
        self.assertEqual(1,OverlapCoefficient(Ngram(2)).WordSimilarity("go","gogo"))


if __name__ == '__main__':
    unittest.main()