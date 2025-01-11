from abc import ABC, abstractmethod
from enum import unique, Enum
from typing import Optional, Set, List
from unittest import TestCase
from dataclasses import dataclass  # Introduced in Python 3.7 but can be used in 3.6 with the package.

from src.Core.Morphology.POSTypes import POSTypes


@unique
class SenseStrategy(Enum):
    """
    Strategy to use when converting/binding a word (lemma) to a sense (synsets).
    """
    FirstSenseOnly = 0
    CombineAllSenses = 1  # Usually the default strategy. We have an explicit strategy for first sense assumption.


@unique
class Relations(Enum):  # Reference: https://wordnet.princeton.edu/ 'Relations' sections.
    """
    All kinds of semantic or non-semantic relations that can be defined between linguistic units.
    """
    Hypernymy = 0  # Default
    InstanceHypernymy = 1


@unique
class Directions(Enum):
    LeftToRight = 0
    RightToLeft = 1
    Both = 2


@unique
class URelations(Enum):
    """
    UndirectedRelations (direction-independent) for all relation types.
    """
    AllCombined = 0  # Use all available relations. Even if the provider does not support all, it should use as many as possible.
    HypernymHyponym = 1  # ParentToChild, including InstanceHypernyms!
    MeronymHolonym = 2  # PartToWhole == ParentToChild - Part is more broad, so part is parent.
    Domains = 3  # TopicDomain and Region bidirectional + UsageDomain


@dataclass
class RelationUsage:
    """
    Represents different usage scenarios of relations.
    """
    URelation: URelations = URelations.AllCombined
    IncludeInstances: bool = True
    Direction: Directions = Directions.LeftToRight

    def __str__(self) -> str:
        return self.URelation.name + ("I" if self.IncludeInstances else "")

    @staticmethod
    def CreateAll():
        """
        Default config: all supported relations including instances.
        """
        return RelationUsage(URelations.AllCombined, IncludeInstances=True, Direction=Directions.Both)

    @staticmethod
    def CreateHypernymWithInstances():
        return RelationUsage(URelations.HypernymHyponym, IncludeInstances=True)


class TaxonomyType(object):
    """
    Represents a taxonomy concept containing its synonym words.
    Essentially a synset, but not directly tied to WordNet terminology.
    """

    def __init__(self, typeCode: str) -> None:
        super().__init__()
        self.TypeCode: str = typeCode  # e.g., car.n.01 - contains the synset name.
        self.Synonyms: List[str] = []  # e.g., car|auto|automobile - includes the main synset name as well.

    @staticmethod
    def ToTypeCodeList(ttList) -> List[str]:
        return list(map(lambda x: x.TypeCode, ttList))

    def AllWords(self):
        """
        Returns all word forms available in the type, including synonyms and synset names if they differ.
        Supports TR and EN synset name formats, extracting their friendly text representations.
        """
        return self.Synonyms + [self.TypeCode.split(".")[0]]  # TR: "ülke.n.01=TUR10-0561830" EN: "entity.n.01"

    def __str__(self) -> str:
        return self.TypeCode + ("|" + str.join("|", self.Synonyms) if self.Synonyms else "")

    def __repr__(self) -> str:
        return self.__str__()


class TaxonomyTypeTest(TestCase):

    def test_str(self):
        tt = TaxonomyType("car.n.01")
        tt.Synonyms = ["automobile", "auto"]
        s: str = tt.__str__()
        self.assertEqual("car.n.01|automobile|auto", s)


class IWordTaxonomy(ABC):
    """
    Contains the schema for querying taxonomic relations at the string level.
    Taxonomy relations are not limited to Hypernym as in WordNet.
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def IsInType(self, thing: str, typeCode: str, sense: SenseStrategy = SenseStrategy.CombineAllSenses,
                 ru: RelationUsage = RelationUsage.CreateAll(), wordPos: POSTypes = None) -> Optional[bool]:
        """
        Checks if the concept represented by a word is a superclass of another concept represented by the typeCode.
        Examples: dog is an animal, cancer is a disease, etc.
        :param ru: RelationUsage
        :param sense: SenseStrategy
        :param wordPos: If the POS of the word is known, it should be provided for better results.
        :param thing: Word
        :param typeCode: Type code
        :return: True/False/None
        """
        pass

    @abstractmethod
    def GetTypeCodesOfHierarchy(self, thing: str, sense: SenseStrategy = SenseStrategy.CombineAllSenses,
                                ru: RelationUsage = RelationUsage.CreateAll(), wordPos: POSTypes = None) -> List[TaxonomyType]:
        pass

    @staticmethod
    def GetAllTypeCodes(self) -> Set[str]:
        """
        Unique Taxonomy Type names we generically accept.
        These generic taxonomy names allow us to build implementation-independent taxonomy models for categories like animals, plants, etc.
        Initially, WordNet synset names are used.
        """
        return {"living_thing", "biological_group"}


if __name__ == "__main__":

    def test(r: RelationUsage = RelationUsage()):
        return str(r)

    u2 = RelationUsage.CreateAll()
    u3 = u2
    print(str(u2))
    u2.IncludeInstances = False
    u1 = RelationUsage(URelations.AllCombined)
    print(u1)
    test()
    print("done")
