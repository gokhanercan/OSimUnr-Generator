from abc import ABC, abstractmethod
from typing import List, Dict
from unittest import TestCase


from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.IRootDetector import IRootDetector

class ICacher(ABC):

    @abstractmethod
    def CachedItemCount(self):
        pass

class MonitorableCacheBase(ICacher):

    def __init__(self) -> None:
        super().__init__()
        self.Hit = 0
        self.Miss = 0
        self.Attempt = 0

    def MissRatio(self)->float:
        return self.Miss / (self.Attempt)

    def ResetCounters(self):
        self.Hit = 0
        self.Miss = 0
        self.Attempt = 0

class RootDetectorCacher(IRootDetector,MonitorableCacheBase):
    """
    Wraps a RootDetector and caches the results. Provides cache statistics and operations.
    """
    def __init__(self, rootDetector:IRootDetector) -> None:
        super().__init__()
        self.RootDetector:IRootDetector = rootDetector
        self._Cache:Dict[str,List[str]] = {}  #expr(w+pos), roots

    def DetectRoots(self, surface: str, priorPOS: POSTypes = None) -> List[str]:
        expr:str = surface+ ("" if priorPOS is None else "-" + str(priorPOS.name))
        cached = self._Cache.get(expr)
        self.Attempt = self.Attempt + 1
        if (cached is None):
            self.Miss = self.Miss + 1
            cached = self.RootDetector.DetectRoots(surface,priorPOS)
            self._Cache[expr] = cached
        else:
            self.Hit = self.Hit + 1
        return cached

    def CachedItemCount(self):
        return len(self._Cache)

