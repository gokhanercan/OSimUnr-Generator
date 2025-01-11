# coding=utf-8
import string
from typing import List
from src.Core.Languages.Grammars.IGrammar import IGrammar


class InvariantGrammar(IGrammar):

    """
    Contains default grammar operations for strings as much as Python can handle. Does not contain information specific to languages.
    """
    def ToUpperCase(self, input: str) -> str:
        return input.upper()

    def ToLowerCase(self, input: str) -> str:
        return input.lower()

    def GetAlphabet(self) -> List[str]:
        return list(string.ascii_uppercase)

    def HasAccent(self, word:str) -> bool:
        """
        Since it is invariant, it does not know the accent of any language.
        :param word:
        :return:
        """
        return False

    def ReduceAccents(self, word:str) -> str:
        return word