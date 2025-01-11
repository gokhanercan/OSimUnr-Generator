# coding=utf-8
from abc import ABC, abstractmethod
from typing import Optional


class IStringDistance(ABC):
    """
    Orthographic distance between two strings. Not normalized.
    """

    @abstractmethod
    def Distance(self, w1: str, w2: str) -> Optional[float]:
        pass


class INormalizedStringDistance(ABC):
    """
    Normalized orthographic distance between two strings.
    """

    @abstractmethod
    def NormalizedDistance(self, w1: str, w2: str) -> Optional[float]:
        pass
