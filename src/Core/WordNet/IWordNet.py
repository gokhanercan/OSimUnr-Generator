from abc import abstractmethod
from enum import Enum, unique
from typing import List, Set, Optional

from nltk.corpus.reader import Synset, Lemma

from src.Core.Dataset.DiscreteScale import DiscreteScale
from src.Core.IWordSource import IWordSource
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.WordNet.IWordTaxonomy import IWordTaxonomy, RelationUsage
from src.Core.WordSim.IWordSimilarity import IWordSimilarity


class IWordNet(IWordSource, IWordTaxonomy):
    """
    Although this is an abstraction, NLTK data types (lemma, synset) are accepted to avoid redefining the same structures.
    """

    @abstractmethod
    def GetAllLemmas(self, singleWordsOnly: bool = False, posFilters: List[POSTypes] = None):
        pass

    def GetWords(self, posFilter: POSTypes = None) -> Set[str]:
        """
        Returns words when using WordNet as a WordSource, not semantically.
        """
        return self.GetAllLemmas(singleWordsOnly=True, posFilters=posFilter if posFilter is None else [posFilter])

    @abstractmethod
    def HasSynset(self, name) -> bool:
        pass

    @abstractmethod
    def LoadSynsetByName(self, synsetName: str):
        pass

    @abstractmethod
    def GetDerivationallyRelatedForms(self, lemma: Lemma) -> List[Lemma]:
        pass

    @abstractmethod
    def LoadLemmas(self, word: str, pos: POSTypes = None, lang: str = "eng") -> List[Lemma]:
        pass

    @abstractmethod
    def LoadSynsets(self, lemma: str, posFilters: List[POSTypes] = None, lang="eng") -> List[Synset]:
        pass

    @abstractmethod
    def LoadSynset(self, lemma: str, pos: POSTypes = POSTypes.NOUN, senseOrder: int = 1) -> Synset:
        pass

    # region Taxonomy
    @abstractmethod
    def Is(self, thing: Synset, type: Synset, rel: RelationUsage = RelationUsage.CreateHypernymWithInstances()) -> Optional[bool]:
        """
        Checks if the synset `thing` is a type of `type` based on the given relation.
        Default relation for WordNet is Hypernym.
        """
        pass

    @abstractmethod
    def GetTypeHierarchy(self, thing: Synset, rel: RelationUsage = RelationUsage.CreateHypernymWithInstances()) -> List[Synset]:
        pass

    @abstractmethod
    def GetRelateds(self, thing: Synset, ru: RelationUsage = RelationUsage.CreateHypernymWithInstances()) -> List[Synset]:
        """
        Returns the direct neighbors of the synset based on the given relation.
        """
        pass

    @abstractmethod
    def GetChildren(self, syn: Synset, rel: RelationUsage = RelationUsage.CreateHypernymWithInstances()) -> List[Synset]:
        pass

    @abstractmethod
    def GetParents(self, syn: Synset, rel: RelationUsage = RelationUsage.CreateHypernymWithInstances()) -> List[Synset]:
        pass

    # endregion


@unique
class Lemma2SynsetMatching(Enum):
    """
    Defines how a given lemma (string) is linked to a synset for path algorithms, as they work on synsets.
    """
    UseFirstSense = 0
    HighestScoreOfCombinations = 1
    AverageScoreOfCombinations = 2


@unique
class WordNetSimilarityAlgorithms(Enum):
    WUP = 0  # Wu and Palmer
    LIN = 1
    JCN = 2
    PATH = 3
    RES = 4
    LCH = 5

    @staticmethod
    def GetAll():
        return [WordNetSimilarityAlgorithms.WUP, WordNetSimilarityAlgorithms.PATH, WordNetSimilarityAlgorithms.LCH,
                WordNetSimilarityAlgorithms.LIN, WordNetSimilarityAlgorithms.JCN, WordNetSimilarityAlgorithms.RES]


class IWordNetMeasures(IWordSimilarity):
    """
    Represents WordNet-based similarity/relatedness measures.
    """

    def __init__(self, algorithm: WordNetSimilarityAlgorithms = WordNetSimilarityAlgorithms.WUP,
                 l2s: Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations) -> None:
        self.Algorithm: WordNetSimilarityAlgorithms = algorithm
        self.Lemma2SynsetMatching = l2s

    @abstractmethod
    def PATHSimilarity(self, w1: str, w2: str, l2s: Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        pass

    @abstractmethod
    def LCHSimilarity(self, w1: str, w2: str, l2s: Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        pass

    @abstractmethod
    def LINSimilarity(self, w1: str, w2: str, l2s: Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        pass

    @abstractmethod
    def JCNSimilarity(self, w1: str, w2: str, l2s: Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        """
        Jiang-Conrath
        """
        pass

    @abstractmethod
    def RESSimilarity(self, w1: str, w2: str, l2s: Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        """
        Resnik
        """
        pass

    @abstractmethod
    def WUPSimilarity(self, w1: str, w2: str, l2s: Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations):
        """
        Wu and Palmer similarity.
        """
        pass

    def WordSimilarity(self, w1: str, w2: str) -> float:
        """
        Should be normalized, but currently isn't.
        """
        simMethodName: str = self.Algorithm.name.__str__() + "Similarity"
        simMethod = getattr(self, simMethodName)
        return simMethod(w1, w2, self.Lemma2SynsetMatching)

    def SimilarityScale(self) -> DiscreteScale:
        return DiscreteScale(0, 1)  # Default; override for algorithms with different scales.
