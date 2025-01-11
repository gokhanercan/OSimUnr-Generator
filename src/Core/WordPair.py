import unittest
from unittest import TestCase

class WordPair(object):

    def __init__(self, word1:str, word2:str, goldSimilarity:float=None):
        """
        :OtherSimilarity columns: Represents the value calculated by the system determined as the final result \n
        :GoldSimilarity: Represents the known ground truth values a priori. Always the fixed 3rd column.
        """
        self.Word1:str = word1
        self.Word2:str = word2
        self.GoldSimilarity:float = goldSimilarity
        self.Note = None            # For information notes related to the WordPair.
        self.IsOOV:bool = None      # Optionally, this flag can be set externally so that the word pair can be skipped according to the OOV strategy during evaluations.

    def SetOtherSimilarity(self, simType:str, sim:float):
        """
        To set different similarity values instead of gold similarity. For example: You can enter Orthographic.
        Always saves the sim field name by converting it to lowercase.
        :param simType:
        :return:
        """
        self.__setattr__(simType.lower() + "Similarity",sim)

    @property
    def goldSimilarity(self):
        return self.GoldSimilarity

    @goldSimilarity.setter
    def goldSimilarity(self, value):
        self.GoldSimilarity = value

    def GetOtherSimilarity(self, simType:str)->float:
        val = self.__getattribute__(simType.lower() + "Similarity")
        return float(val) if val >= 0 else None

    def __str__(self):
        return str(vars(self))

    def __repr__(self) -> str:
        return str(vars(self))

    def ToKey(self):
        """
        Returns the unique key independent of the order of the words.
        :return:
        """
        return self.ToOrderFreeUniqueStr(self.Word1,self.Word2)

    def ToPairDisplay(self)->str:
        return self.Word1.ljust(24) + "- " + self.Word2.ljust(24)

    @staticmethod
    def ToOrderFreeUniqueStr(w1:str, w2:str):
        """
        Produces a unique string by placing the smaller word first so that we can express two pairs uniquely independent of order.
        :param w1:
        :param w2:
        :return:
        """
        firstOneSmall:bool = w1 < w2
        return w1+"-"+w2 if firstOneSmall else w2+"-"+w1


class WordPairTest(TestCase):

    def test_TwoSymetticalyWordPairs_ReturnSameHashes(self):
        hash1:str = WordPair.ToOrderFreeUniqueStr("gokhan","ercan")
        hash2:str = WordPair.ToOrderFreeUniqueStr("ercan","gokhan")
        self.assertEqual(hash1,hash2)

if __name__ == '__main__':
    unittest.main()