# coding=utf-8
from abc import ABC, abstractmethod


class IConfigValueable(ABC):

    @abstractmethod
    def ToConfigValue(self)->str:
        pass