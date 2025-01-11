import string
import unittest
from abc import ABC, abstractmethod
from typing import Set, List, Optional


class IGrammar(ABC):
    """
    Abstracts the grammar operations of languages.
    """

    @abstractmethod
    def ToUpperCase(self,input:str)->str:
        pass

    @abstractmethod
    def ToLowerCase(self, input:str)->str:
        pass

    @abstractmethod
    def GetAlphabet(self)->List[str]:
        """
        Returns the alphabet in uppercase as a list of characters.
        :return:
        """

    def GetNextCharInAlphabet(self, chr:str)->Optional[str]:
        """
        Returns the next character in the alphabet.
        :param chr:
        :return:
        """
        alphabet = self.GetAlphabet()
        index:int = alphabet.index(self.ToUpperCase(chr))
        if(index == 0): return None
        return alphabet[index+1]

    def GetPreviousCharInAlphabet(self, chr:str)->Optional[str]:
        """
        Returns the previous character in the alphabet.
        :param chr:
        :return:
        """
        alphabet = self.GetAlphabet()
        index:int = alphabet.index(self.ToUpperCase(chr))
        if(index == 0): return None
        return alphabet[index-1]

    @abstractmethod
    def HasAccent(self, word:str)->bool:
        pass
    @abstractmethod
    def ReduceAccents(self, word:str)->str:
        pass

#UNITTEST
from unittest.mock import patch
from functools import partial
class TestIGrammar(unittest.TestCase):

    @patch.multiple(IGrammar, __abstractmethods__=set())
    def test_GetPreviousCharInAlphabet_b_ReturnA(self):
        target = IGrammar()
        def fake(self):
            return list(string.ascii_uppercase)
        target.GetAlphabet = partial(fake,target)
        def fakeUpper(self,str):
            return "B"
        target.ToUpperCase = partial(fakeUpper,target)
        self.assertEqual("A",target.GetPreviousCharInAlphabet('b'))

    @patch.multiple(IGrammar, __abstractmethods__=set())
    def test_GetPreviousCharInAlphabet_Z_ReturnY(self):
        target = IGrammar()
        def fake(self):
            return list(string.ascii_uppercase)
        target.GetAlphabet = partial(fake,target)
        def fakeUpper(self,str):
            return "Z"
        target.ToUpperCase = partial(fakeUpper,target)
        self.assertEqual("Y",target.GetPreviousCharInAlphabet('Z'))

    @patch.multiple(IGrammar, __abstractmethods__=set())
    def test_GetPreviousCharInAlphabet_A_ReturnNone(self):
        target = IGrammar()
        def fake(self):
            return list(string.ascii_uppercase)
        target.GetAlphabet = partial(fake,target)
        def fakeUpper(self,str):
            return "A"
        target.ToUpperCase = partial(fakeUpper,target)
        self.assertEqual(None,target.GetPreviousCharInAlphabet('A'))

    @patch.multiple(IGrammar, __abstractmethods__=set())
    def test_GetNextCharInAlphabet_y_ReturnZ(self):
        target = IGrammar()
        def fake(self):
            return list(string.ascii_uppercase)
        target.GetAlphabet = partial(fake,target)
        def fakeUpper(self,str):
            return "Y"
        target.ToUpperCase = partial(fakeUpper,target)
        self.assertEqual("Z",target.GetNextCharInAlphabet('y'))

if __name__ == '__main__':
    unittest.main()