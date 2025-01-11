import unittest
import warnings
from typing import Optional, List, Tuple, Set
from unittest import TestCase

from nltk.corpus.reader import Synset

from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Task.IWordRelatednessBinaryClassifier import IWordRelatednessBinaryClassifier
from src.Core.WordNet.IWordNet import IWordNet
from src.Core.WordNet.IWordTaxonomy import RelationUsage
from src.Core.WordNet.NLTKWordNetWrapper import NLTKWordNetWrapper


class BlacklistedConceptsWordNetRelatednessFilterer(IWordRelatednessBinaryClassifier):
    """
    RelatedConcepts, filters out if it matches the known pair of concept relationships as Prior.
    I don't give the full classifier name because: it knows well how to find the related one, but not the other.
    If both words in a word pair correspond to a BlackListedConcept, it is filtered out.
    """

    def __init__(self, wordnet:IWordNet, blacklistedConcepts:List[str], pos:POSTypes = POSTypes.NOUN)-> None:        #SynsetName,SynsetName
        super().__init__()
        self.WN:IWordNet = wordnet
        self.POS:POSTypes = pos
        self._BlacklistedConcepts:List[str] = blacklistedConcepts
        self._BlacklistedConceptsSet:Set[str] = set(self._BlacklistedConcepts)

    def IsRelated(self, word1: str, word2: str) -> Optional[bool]:
        syns1:List[Synset] = self.WN.LoadSynsets(word1,posFilters=[self.POS])       #Ass: This class accepts only one pos, whereas wn accepts more than one.
        syns2:List[Synset] = self.WN.LoadSynsets(word2,posFilters=[self.POS])
        h1:List[Synset] = []        #hierarchy of synsets
        h2:List[Synset] = []
        for syn1 in syns1:
            h1 = h1 + self.WN.GetTypeHierarchy(syn1,RelationUsage.CreateHypernymWithInstances())
        for syn2 in syns2:
            h2 = h2 + self.WN.GetTypeHierarchy(syn2,RelationUsage.CreateHypernymWithInstances())

        #region F)BlackListedConcepts
        s1 = set(map(lambda x:x._name,h1))
        s2 = set(map(lambda x:x._name,h2))
        c1 = s1 & self._BlacklistedConceptsSet
        c2 = s2 & self._BlacklistedConceptsSet
        if(c1.__len__() > 0 and c2.__len__()>0): return True
        #endregion

        else: return None       #Filterers return None, not False.

class BlacklistedConceptsWordNetRelatednessFiltererTest(TestCase):

    def test_WordpairsInTwoDifferentBlacklistedConcepts_ReturnRelated(self):
        wn = NLTKWordNetWrapper()
        bconcepts = ["ill_health.n.01","disorder.n.01",
                                 "pathologic_process.n.01",
                                 "plant_part.n.01","biological_group.n.01","medical_procedure.n.01",
                                 "animal.n.01","microorganism.n.01","plant.n.02",
                                 "chemical.n.01","substance.n.07",
                                 "symptom.n.01"]      #order is important! From general to specific..
        filterer = BlacklistedConceptsWordNetRelatednessFilterer(wn, bconcepts, POSTypes.NOUN)
        actual:bool = filterer.IsRelated("adrenalectomy","lion")        #medical_procedure - animal
        self.assertTrue(actual)


if __name__ == "__main__":
    unittest.main()

