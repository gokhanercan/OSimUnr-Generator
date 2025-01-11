# coding=utf-8
from abc import ABC

class IMetric(ABC):
    """
    Specifies that implementing classes represent metrics adhering to MetricSpace rules such as the 'Triangle Inequality.'
    Currently, it is used solely for informational purposes. It has no functional role and was introduced to create self-awareness.
    https://mathworld.wolfram.com/MetricSpace.html
    """
    def __init__(self) -> None:
        super().__init__()

    def IsMetric(self):
        return True
