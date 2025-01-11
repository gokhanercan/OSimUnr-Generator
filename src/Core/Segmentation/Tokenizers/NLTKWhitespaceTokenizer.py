import unittest
from collections.abc import Iterable
from unittest import TestCase

from src.Core.Segmentation.Tokenizers.ITokenizer import ITokenizer


class NLTKWhitespaceTokenizer(ITokenizer):
    """
    Wraps NLTK: Tokenize a string on whitespace (space, tab, newline). In general, users should use the string split() method instead.
    Does not handle case, it is case-sensitive.
    https://www.nltk.org/api/nltk.tokenize.html
    """

    def __init__(self) -> None:
        from nltk import WhitespaceTokenizer
        self._Tokenizer=WhitespaceTokenizer()

    def Tokenize(self, text: str) -> 'Iterable[str]':
        return self._Tokenizer.tokenize(text)


class NLTKWhitespaceTokenizerTest(TestCase):

    def test_Tokenize_DoubleWhiteSpace_TokenizeTrimmed(self):
        target = NLTKWhitespaceTokenizer()
        actual = target.Tokenize("gokhan  ercan")
        self.assertEqual(2,len(actual))
        self.assertEqual("gokhan",actual[0])
        self.assertEqual("ercan",actual[1])

    def test_Tokenize_CaseDifference_TokenizeCaseSensitive(self):
        target = NLTKWhitespaceTokenizer()
        actual = target.Tokenize("Gokhan Ercan")
        self.assertEqual(2,len(actual))
        self.assertEqual("Gokhan",actual[0])
        self.assertEqual("Ercan",actual[1])

if __name__ == "__main__":
    unittest.main()

