from typing import List, Dict, Tuple, Set
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.IRootDetectorStack import IRootDetectorStack
from src.Core.Morphology.RootDetection.RootDetectorCacher import MonitorableCacheBase


class RootDetectorStackCacher(IRootDetectorStack,MonitorableCacheBase):
    """
    Wraps a RootDetectorStack and caches the results. Provides cache statistics and operations. Refer to behavior tests for more information.

    """
    def __init__(self, rootDetectorStack:IRootDetectorStack) -> None:
        super().__init__()
        self.RootDetectorStack:IRootDetectorStack = rootDetectorStack
        self._Cache:Dict[str,List[str]] = {}  #expr(w+pos), roots

    def DetectRootsInStack(self, surface:str, priorPOS:POSTypes = None)->Tuple[Set[str],str,Set[str]]:
        expr:str = surface+ ("" if priorPOS is None else "-" + str(priorPOS.name))
        cached = self._Cache.get(expr)
        self.Attempt = self.Attempt + 1
        if (cached is None):
            self.Miss = self.Miss + 1
            cached = self.RootDetectorStack.DetectRootsInStack(surface,priorPOS)
            self._Cache[expr] = cached
        else:
            self.Hit = self.Hit + 1
        return cached

    def CachedItemCount(self):
        return len(self._Cache)