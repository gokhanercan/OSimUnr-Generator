# coding=utf-8
from typing import Optional

from src.Core.Task.IWordRelatednessBinaryClassifier import IWordRelatednessBinaryClassifier


class WordRelatednessClassifierStub(IWordRelatednessBinaryClassifier):

    def __init__(self, related:bool) -> None:
        super().__init__()
        self.Related:bool = related

    def IsRelated(self, word1: str, word2: str) -> Optional[bool]:
        return self.Related

    def __str__(self) -> str:
        return "stub"

    def __repr__(self) -> str:
        return self.__str__()
