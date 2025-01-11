# coding=utf-8
from typing import Optional
from unittest import TestCase


class DiscreteScale(object):
    """
    Represents the min-max range for discrete intervals.
    By default, we accept 0-10 as in WordSim.
    """
    def __init__(self, min:Optional[float] = 0, max:Optional[float] = 10) -> None:
        super().__init__()
        self.Min:Optional[float] = min
        self.Max:Optional[float] = max

    def IsNormalized(self)->bool:
        """
        If normalized (Closed), it means min and max values exist. If at least one is missing (None), it is considered open.
        :return:
        """
        return (self.Max is not None) and (self.Min is not None)

    def __str__(self) -> str:
        return str(self.Min if self.Min is not None else "-∞") + \
               " | " + \
               str(self.Max if self.Max is not None else "∞")


class DiscreteScaleTest(TestCase):

    def test_IsNormalized_0_10_Normalized(self):
        self.assertEqual(True,DiscreteScale(0,10).IsNormalized())

    def test_IsNormalized_MinInfMax10_False(self):
        self.assertEqual(False,DiscreteScale(None,10).IsNormalized())

    def test_IsNormalized_Min0MaxInf_False(self):
        self.assertEqual(False,DiscreteScale(0,None).IsNormalized())

    def test_IsNormalized_BothInf_False(self):
        self.assertEqual(False,DiscreteScale(None,None).IsNormalized())

    def test_str_Normalized(self):
        self.assertEqual("0 | 10",DiscreteScale(0,10).__str__())

    def test_str_NotNormalized(self):
        self.assertEqual("-∞ | 10",DiscreteScale(None,10).__str__())

    def test_str_NotNormalizedMaxInf(self):
        self.assertEqual("0 | ∞",DiscreteScale(0,None).__str__())
