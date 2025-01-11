# coding=utf-8
from abc import abstractmethod
from typing import Set, Dict

from src.Core.IConfigValueable import IConfigValueable


class IGramExtractor(IConfigValueable):
    """
    Unlike Tokenizer and Segmentor, it only creates sets of Distinct sequences.
    """

    @abstractmethod
    def ExtractGrams(self, word: str) -> 'Set[str]':
        """
        Unlike Tokenizer and Segmentor, it only creates sets of Distinct sequences.
        """
        pass


class ICountableGramExtractor(IConfigValueable):

    @abstractmethod
    def ExtractGramsWithCounts(self, word: str) -> 'Dict[str]':
        """
        Unlike Tokenizer and Segmentor, it only creates sets of Distinct sequences.
        """
        pass
