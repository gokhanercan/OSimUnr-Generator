# coding=utf-8
from abc import ABC, abstractmethod
from typing import Optional, Tuple


class IWordRelatednessBinaryClassifier(ABC):
    """
    Determines whether there is a relationship between two words as binary.
    This task is independent of what kind of relation (derivational, orthographic etc.) the relation is.
    """

    @abstractmethod
    def IsRelated(self, word1:str, word2:str)->Optional[bool]:
        """
        Are the given two words related to each other?
        :param word1:
        :param word2:
        :return: Returns null if there is no opinion. For example, Filterers should only return one class and return None for the other side.
        """
        pass
