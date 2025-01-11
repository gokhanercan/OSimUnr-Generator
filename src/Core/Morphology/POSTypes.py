# coding=utf-8
from enum import unique, Enum

@unique
class POSTypes(Enum):
    NOUN = 0,
    VERB = 1,
    ADJ = 2,
    ADV = 3,

    @staticmethod
    def GetFullPOSList(self):
        return [POSTypes.NOUN,POSTypes.ADJ,POSTypes.VERB,POSTypes.ADV]

