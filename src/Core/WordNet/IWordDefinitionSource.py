from abc import ABC, abstractmethod
from typing import List

from src.Core.Morphology.POSTypes import POSTypes


class IWordDefinitionSource(ABC):
    """
    Any kind of KnowledgeBase that has definitions of words
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def GetDefinitions(self, word:str, forPOS:POSTypes = None)->List[str]:
        """
        Returns the definition string of the word.
        :param word:
        :return: Can return multiple definitions. If none found, returns an empty list.
        """
        pass

    def GetMergedDefinitions(self, word:str, forPOS:POSTypes = None)->str:
        """
        Returns multiple definitions combined as a single string.
        :param word:
        :param forPOS:
        :return: If no definitions, returns an empty string.
        """
        defs = self.GetDefinitions(word,forPOS)
        if defs is None or defs.__len__() == 0: return ""
        return "\n".join(defs)