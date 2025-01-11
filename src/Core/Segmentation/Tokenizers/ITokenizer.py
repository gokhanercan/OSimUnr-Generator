# coding=utf-8
from abc import abstractmethod, ABC
from collections.abc import Iterable


class ITokenizer(ABC):
    """
    Performs simple string-level operations, unlike a Segmentor, which cannot perform morphological segmentation.
    Similar to a Segmentor, it preserves the order of items.
    Maintains the order of items and can contain multiple occurrences of the same item.
    """

    @abstractmethod
    def Tokenize(self, text: str) -> 'Iterable[str]':  # Added quotes to avoid "'ABCMeta' object is not subscriptable" error: https://stackoverflow.com/questions/45883939/function-annotation-for-a-list-containing-abcmeta-instances
        pass
