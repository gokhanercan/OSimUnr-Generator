import unittest
from abc import ABC, abstractmethod
from typing import Optional, List, Set
from unittest import TestCase
from unittest.mock import patch

from src.Core.Morphology.POSTypes import POSTypes


class IRootDetector(ABC):
    """
    Returns only the root (gloss) form of a word given in the surface form.
    It is not a Disambiguator because it does not operate at the sentence level and does not produce alternative analyses.
    It is not a SegmentorBase because it does not produce affixes in metamorpheme, morpheme, or any other string form.
    Disambiguators and Segmentors inherently encompass the IRootDetector capability.
    """

    @abstractmethod
    def DetectRoots(self, surface:str, priorPOS:POSTypes = None)->List[str]:
        """
        Returns root detection suggestions in order of priority. 
        The first element is assumed to be the main root, while the others represent other roots and alternatives in compound words.
        :param surface: Word or lemma in surface form
        :param priorPOS: If known beforehand, the POS information of the given word. Not every model is required to evaluate this.
        :return: Returns an empty list if no root is found. If the root is equal to itself, it should return itself.
        """
        pass

    def DetectSingleRootOrNone(self, surface:str, priorPOS:POSTypes = None)->Optional[str]:
        """
        Returns the first detected root. Returns None if no root is found.
        :return:
        """
        roots:List[str] = self.DetectRoots(surface,priorPOS)
        if(roots.__len__() == 0): return None
        return roots[0]
