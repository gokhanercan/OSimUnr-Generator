# coding=utf-8
import unittest
from typing import List, Set
from unittest import TestCase

class Preprocessors(object):

    def __init__(self, punctuations=None)->None:
        super().__init__()
        self.Punctuations:Set[chr] = punctuations
        if (self.Punctuations is None): self.Punctuations = Preprocessors.DefaultPunctuations()

    @staticmethod
    def DefaultPunctuations()->set:
        return {".",",","-","?","_","!",":",";","'","(",")"}

    @staticmethod
    def NormalizeWhitespaces(text):
        #from gensim.parsing.preprocessing import strip_multiple_whitespaces        #very long, no need to load.
        return text.strip()

    def RemovePunctuation(self, text:str)->str:
        newText:List[chr] = []
        i:int = 0
        for c in text:
            if (not self.Punctuations.__contains__(c)):
                newText.append(c)
        return ''.join(newText)

    def ContainsPunctuation(self, text:str)->bool:
        """
        :param text:
        :return:
        """
        for p in self.Punctuations:
            if(text.__contains__(p)):
                return True
        return False

class PreprocessorsTest(TestCase):

    def test_ContainsPunctuation_Hypens_ReturnTrue(self):
        self.assertEqual(True,Preprocessors().ContainsPunctuation("life-style"))

    def test_ContainsPunctuation_PlainText_ReturnFalse(self):
        self.assertEqual(False,Preprocessors().ContainsPunctuation("gokhan"))

    def test_RemovePunctuation_Hypens_Remove(self):
        self.assertEqual("lifestyle",Preprocessors().RemovePunctuation("life-style"))


if __name__ == '__main__':
    unittest.main()