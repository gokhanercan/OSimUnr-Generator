# coding=utf-8
from abc import ABC, abstractmethod
from typing import Set

from src.Core.Morphology.POSTypes import POSTypes


class IWordSource(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def GetWords(self, posFilter:POSTypes = None)->Set[str]:
        pass