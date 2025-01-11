# coding=utf-8
import random
from typing import Optional

from src.Core.Task.IWordRelatednessBinaryClassifier import IWordRelatednessBinaryClassifier


class RandomWordRelatednessClassifier(IWordRelatednessBinaryClassifier):

    def IsRelated(self, word1: str, word2: str) -> Optional[bool]:
        return random.randint(0,1) == 0

    def __str__(self) -> str:
        return "rnd"

