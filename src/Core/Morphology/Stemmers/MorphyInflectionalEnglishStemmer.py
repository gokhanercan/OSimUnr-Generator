from typing import Dict
from unittest import TestCase

from src.Core.Morphology.Stemmers.IStemmer import IStemmer
from src.Tools import FormatHelper


class MorphyInflectionalEnglishStemmer(IStemmer):
    """
    Returns the stem by removing different inflections using Nltk.Morphy.
    Nltk SnowballStemmer (englishStemmer) contained suffixes to be removed in 7 levels to also remove derivational suffixes. It is not used.
    http://www.nltk.org/howto/wordnet.html
    http://snowball.tartarus.org/algorithms/english/stemmer.html
    Other lemmatizers, stemmers: wordnet (new name morphy), spacy, textblob, stanford, pattern, gensim, treetagger.
    Comparing lemmatizers: https://www.machinelearningplus.com/nlp/lemmatization-examples-python/#comparingnltktextblobspacypatternandstanfordcorenlp
    """

    def __init__(self) -> None:
        super().__init__()

    def Stem(self, word: str):
        from nltk.corpus import wordnet as wn
        stemmed = wn.morphy(word)
        # 2nd pass
        if (stemmed is None or stemmed == word):
            stemmed = wn.morphy(word,
                                pos='v')  # specifically solves ing when I request it as v. Therefore, I send a second attempt only for ing.
        return stemmed


class MorphyInflectionalEnglishStemmerTest(TestCase):

    def test_ALL_INFLECTIONS(self):
        stemmer = MorphyInflectionalEnglishStemmer()

        cases: Dict[str, str] = {}
        cases["cats"] = "cat"
        cases["denied"] = "deny"
        cases["churches"] = "church"
        cases["built"] = "build"
        cases["scripting"] = "script"  # Noun+ing
        cases["walking"] = "walk"  # Verb+ing
        cases["building"] = "build"

        from tabulate import tabulate
        from pandas import DataFrame
        df = DataFrame()
        index = 1
        anyFail = False
        for word, expected in cases.items():
            actual: str = stemmer.Stem(word)
            if (not actual): actual = "-NONE-"
            df.at[index, "Word"] = word
            df.at[index, "Expected"] = expected
            df.at[index, "Actual"] = actual
            passed: bool = expected == actual
            if not passed: anyFail = True
            self.assertTrue(passed, actual + " != " + expected)
            index = index + 1
        if (not anyFail): self.assertTrue("All " + str(index) + " passed!")
        print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=FormatHelper._ThreeDigitFormat))


if __name__ == "__main__":
    pass
