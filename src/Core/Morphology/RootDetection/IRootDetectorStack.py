from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Set
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.IRootDetector import IRootDetector


class IRootDetectorStack(IRootDetector):
    """
    In addition to RootDetector, it can also return the detector information and secondary OOL (Out-Of-Lexicon) roots during detection.
    """

    @abstractmethod
    def DetectRootsInStack(self, surface: str, priorPOS: POSTypes = None) -> Tuple[Set[str], str, Set[str]]:  # roots, detectors str, oolroots
        """
        Returns roots without underscores.
        :param surface: Word or lemma in surface form
        :param priorPOS: If known, the POS information of the given word
        :return: A tuple containing roots, detector information, and OOL roots
        """
        pass

    def DetectRoots(self, surface: str, priorPOS: POSTypes = None) -> List[str]:
        roots, detectors, oolroots = self.DetectRootsInStack(surface, priorPOS)
        return list(roots)
