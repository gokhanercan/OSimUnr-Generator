# coding=utf-8
from abc import ABC, abstractmethod

class Dataset(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def Name(self):
        return self._Name

    def Load(self):
        return self

    @abstractmethod
    def Persist(self, newFilename:str):
        pass