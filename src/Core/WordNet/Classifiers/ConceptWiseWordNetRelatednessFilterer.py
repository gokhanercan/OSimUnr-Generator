import unittest
from typing import Optional, List, Tuple
from unittest import TestCase

from nltk.corpus.reader import Synset

from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Task.IWordRelatednessBinaryClassifier import IWordRelatednessBinaryClassifier
from src.Core.WordNet.IWordNet import IWordNet
from src.Core.WordNet.IWordTaxonomy import RelationUsage
from src.Core.WordNet.NLTKWordNetWrapper import NLTKWordNetWrapper


class ConceptWiseWordNetRelatednessFilterer(IWordRelatednessBinaryClassifier):
    """
    Filters out word pairs if their concepts match any prior known related concept pairs.
    Does not explicitly classify, as it is good at identifying related pairs but not unrelated ones.
    If both words in a word pair match a BlackListedConcept, they are filtered out.
    """

    def __init__(self, wordnet: IWordNet, relatedConcepts: List[Tuple[str, str]], pos: POSTypes = POSTypes.NOUN) -> None:  # SynsetName, SynsetName
        super().__init__()
        self.WN: IWordNet = wordnet
        self.RelatedConcepts: List[Tuple[str, str]] = relatedConcepts
        self.POS: POSTypes = pos

    def IsRelated(self, word1: str, word2: str) -> Optional[bool]:
        syns1: List[Synset] = self.WN.LoadSynsets(word1, posFilters=[self.POS])  # Assumption: This class accepts only one POS, whereas WN accepts multiple.
        syns2: List[Synset] = self.WN.LoadSynsets(word2, posFilters=[self.POS])
        h1: List[Synset] = []  # Hierarchy of synsets
        h2: List[Synset] = []
        for syn1 in syns1:
            h1 = h1 + self.WN.GetTypeHierarchy(syn1, RelationUsage.CreateHypernymWithInstances())
        for syn2 in syns2:
            h2 = h2 + self.WN.GetTypeHierarchy(syn2, RelationUsage.CreateHypernymWithInstances())

        # Region: Filter - RelatedConcepts
        for concept in self.RelatedConcepts:
            w1c1 = w1c2 = w2c1 = w2c2 = None  # Match combinations
            c1: str = concept[0].strip()
            c2: str = concept[1].strip()
            if sum(map(lambda x: x._name == c1, h1)) > 0:
                w1c1 = True
            if sum(map(lambda x: x._name == c1, h2)) > 0:
                w2c1 = True
            if sum(map(lambda x: x._name == c2, h1)) > 0:
                w1c2 = True
            if sum(map(lambda x: x._name == c2, h2)) > 0:
                w2c2 = True
            if (w1c1 and w2c2) or (w2c1 and w1c2):
                return True  # Matching concepts, e.g., c1 and c2
        return None


class ConceptWiseWordNetRelatednessFiltererTest(TestCase):

    def test_TwoIndirectInstances_ReturnRelated(self):
        wn = NLTKWordNetWrapper()
        concepts = [("religion.n.01", "religious_person.n.01")]
        filterer = ConceptWiseWordNetRelatednessFilterer(wn, concepts, POSTypes.NOUN)
        actual: bool = filterer.IsRelated("wahhabism", "wahabi")
        self.assertTrue(actual)

    def test_TwoIndirectInstancesInReverse_ReturnRelated(self):
        wn = NLTKWordNetWrapper()
        concepts = [("religious_person.n.01", "religion.n.01")]
        filterer = ConceptWiseWordNetRelatednessFilterer(wn, concepts, POSTypes.NOUN)
        actual: bool = filterer.IsRelated("wahhabism", "wahabi")
        self.assertTrue(actual)

    def test_OnlyOneMatchingUnrelatedInstances_ReturnNone(self):
        # Cannot classify as related or unrelated.
        wn = NLTKWordNetWrapper()
        concepts = [("religion.n.01", "religious_person.n.01")]
        filterer = ConceptWiseWordNetRelatednessFilterer(wn, concepts, POSTypes.NOUN)
        actual = filterer.IsRelated("wahhabism", "car")
        self.assertIsNone(actual)


if __name__ == "__main__":
    unittest.main()
