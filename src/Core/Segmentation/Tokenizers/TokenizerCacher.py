import unittest
from typing import List, Dict
from unittest import TestCase
from src.Core.Morphology.RootDetection.RootDetectorCacher import ICacher
from src.Core.Segmentation.Tokenizers.ITokenizer import ITokenizer
from src.Core.Segmentation.Tokenizers.NLTKWhitespaceTokenizer import NLTKWhitespaceTokenizer


class TokenizerCacher(ITokenizer, ICacher):

    def __init__(self, tokenizer: ITokenizer) -> None:
        self.Tokenizer: ITokenizer = tokenizer
        self._Cache: Dict[str, List[str]] = {}  # word, tokens

    def Tokenize(self, text: str) -> 'Iterable[str]':
        cached = self._Cache.get(text)
        if cached is None:
            cached = self.Tokenizer.Tokenize(text)
            self._Cache[text] = cached
        return cached

    def CachedItemCount(self):
        return len(self._Cache)


class NLTKWhitespaceTokenizerTest(TestCase):

    def test_CacheWrapping_TwoTimes(self):
        tokenizer = NLTKWhitespaceTokenizer()
        target = TokenizerCacher(tokenizer)
        actual = target.Tokenize("gokhan  ercan")
        self.assertEqual(2, len(actual))
        self.assertEqual("gokhan", actual[0])
        self.assertEqual("ercan", actual[1])
        self.assertEqual("ali", target.Tokenize("ali ")[0])                 # test if the cacher mixes two cache keys
        self.assertEqual("gokhan", target.Tokenize("gokhan  ercan")[0])     # check if it retrieves this value from the cache
        self.assertEqual(2, target.CachedItemCount())


if __name__ == "__main__":
    unittest.main()