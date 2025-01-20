from abc import ABC, abstractmethod
from typing import List

from src.Core.IWordSource import IWordSource
from src.Core.Languages.LinguisticContext import LinguisticContext
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.IRootDetector import IRootDetector
from src.Core.Orthographic.NormalizedStringSimilarity.EditDistance import EditDistance
from src.Core.Segmentation.Tokenizers.ITokenizer import ITokenizer
from src.Core.Task.IWordRelatednessBinaryClassifier import IWordRelatednessBinaryClassifier
from src.Core.WordNet.Classifiers.BlacklistedConceptsWordNetRelatednessFilterer import \
    BlacklistedConceptsWordNetRelatednessFilterer
from src.Core.WordNet.Classifiers.ConceptWiseWordNetRelatednessFilterer import ConceptWiseWordNetRelatednessFilterer
from src.Core.WordNet.Classifiers.DefinitionBasedRelatednessClassifier import DefinitionBasedRelatednessClassifier
from src.Core.WordNet.IWordNet import IWordNet, WordNetSimilarityAlgorithms, Lemma2SynsetMatching
from src.Core.WordSim.IWordSimilarity import IWordSimilarity


class PipelineProviderBase(ABC):
    def __init__(self, ctx:LinguisticContext, osimAlgorithm:IWordSimilarity):
        self.Context:LinguisticContext = ctx
        self.OSimAlgorithm:IWordSimilarity = osimAlgorithm
        self._WordNet:IWordNet = None
        self._WordSource: IWordSource = None

    @abstractmethod
    def CreateWordNet(self)->IWordNet:
        pass

    @abstractmethod
    def CreateWordSource(self) -> IWordSource:
        pass

    @abstractmethod
    def CreateRootDetector(self) -> IRootDetector:
        pass

    @abstractmethod
    def CreateFastRootDetector(self) -> IRootDetector:
        pass

    @abstractmethod
    def CreateTokenizer(self) -> ITokenizer:
        pass

    #region Filterings
    @abstractmethod
    def CreateBlacklistedConceptsFilterer(self, pos: POSTypes) -> BlacklistedConceptsWordNetRelatednessFilterer:
        pass

    @abstractmethod
    def CreateConceptPairFilterer(self, pos: POSTypes) -> ConceptWiseWordNetRelatednessFilterer:
        pass

    @abstractmethod
    def CreateDefinitionBasedRelatednessClassifier(self, posFilter: POSTypes, rootDetector,fastRootDetector) -> DefinitionBasedRelatednessClassifier:
        pass

    @abstractmethod
    def CreateDerivationallyRelatedClassifier(self) -> IWordRelatednessBinaryClassifier:
        pass
    #endregion

    @abstractmethod
    def CreateWordNetSimAlgorithm(self) -> WordNetSimilarityAlgorithms:
        pass

    @abstractmethod
    def CreateWordNetForSimilarity(self, wnSimAlg: WordNetSimilarityAlgorithms,
                                   l2s: Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations,
                                   wordSimPOSFilters: List[POSTypes] = None):
        pass

    def GetWordNet(self):
        if(not self._WordNet):
            self._WordNet = self.CreateWordNet()
        return self._WordNet

    def GetWordSource(self):
        if(not self._WordSource):
            self._WordSource = self.CreateWordSource()
        return self._WordSource

    def GetOrthographicSimilarityAlgorithm(self) -> IWordSimilarity:
        return self.OSimAlgorithm

