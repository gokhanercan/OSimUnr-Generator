from typing import Optional, List, Set

from pandas import DataFrame
from tabulate import tabulate

from src.Core.Task.IWordRelatednessBinaryClassifier import IWordRelatednessBinaryClassifier
from src.Core.WordNet.IWordNet import IWordNet
from src.Core.WordNet.NLTKWordNetWrapper import NLTKWordNetWrapper
from src.Core.WordPair import WordPair
from src.Tools import FormatHelper


class WordNetDerivationallyRelatedBinaryClassifier(IWordRelatednessBinaryClassifier):
    """
    Determines whether two words are related based on WordNet's DerivationallyRelated information.
    """

    def __init__(self, wordnet: IWordNet) -> None:
        super().__init__()
        self.WordNet = wordnet

    def IsRelated(self, word1: str, word2: str) -> Optional[bool]:
        if not word1 or not word2:
            return None
        # Word1
        w1Relateds: Set[str] = set(self._ExtractDerivationalRelatedLemmaNames(word1))
        if len(w1Relateds) == 0:
            return False
        # Word2
        w2Relateds: Set[str] = set(self._ExtractDerivationalRelatedLemmaNames(word2))
        if len(w2Relateds) == 0:
            return False
        return len(w1Relateds.intersection(w2Relateds)) > 0

    def _ExtractDerivationalRelatedLemmaNames(self, word: str) -> List[str]:
        extracted: List[str] = []
        lemmas = self.WordNet.LoadLemmas(word)
        if not lemmas:
            return []
        for lemma in lemmas:
            relateds = self.WordNet.GetDerivationallyRelatedForms(lemma)
            if len(relateds) > 0:
                for related in relateds:
                    extracted.append(related._name)
        return extracted


if __name__ == "__main__":

    wordnet = NLTKWordNetWrapper()
    classifier: WordNetDerivationallyRelatedBinaryClassifier = WordNetDerivationallyRelatedBinaryClassifier(wordnet)

    def RunExperiments(wps: List[WordPair]):
        df = DataFrame()
        index = 1
        for wp in wps:
            result = classifier.IsRelated(wp.Word1, wp.Word2)
            df.at[index, "WordPair"] = wp.ToPairDisplay()
            df.at[index, "IsRelated"] = result
            index = index + 1
        print(tabulate(df, headers="keys", tablefmt="psql", floatfmt=FormatHelper._TwoDigitFormat))

    wps: List[WordPair] = []
    wps.append(WordPair("dog", "dogs"))
    wps.append(WordPair("socialism", "socialist"))
    wps.append(WordPair("athleticism", "athletics"))
    wps.append(WordPair("atheist", "theist"))
    wps.append(WordPair("broadcast", "rebroadcast"))
    wps.append(WordPair("bucharest", "bucharesti"))
    wps.append(WordPair("buddhism", "buddhist"))
    wps.append(WordPair("cambodia", "cambodian"))
    wps.append(WordPair("sociolinguist", "sociolinguistics"))
    wps.append(WordPair("tourism", "tourist"))
    wps.append(WordPair("transfer", "transferee"))
    wps.append(WordPair("transition", "transitive"))
    wps.append(WordPair("activating", "activation"))
    wps.append(WordPair("activism", "activist"))
    wps.append(WordPair("biologism", "biologist"))
    wps.append(WordPair("biophysicist", "biophysics"))
    wps.append(WordPair("cardiogram", "cardiograph"))
    wps.append(WordPair("cardiography", "radiography"))
    wps.append(WordPair("cinematographer", "cinematography"))
    wps.append(WordPair("coffea", "coffee"))  # HUMAN?
    wps.append(WordPair("diploma", "diplomat"))
    wps.append(WordPair("direction", "indirection"))
    wps.append(WordPair("experiment", "experimenter"))
    wps.append(WordPair("fatigue", "fatigues"))
    wps.append(WordPair("checker", "checkers"))
    wps.append(WordPair("wrestle", "wrestler"))
    wps.append(WordPair("abbreviation", "abbreviator"))
    wps.append(WordPair("atheism", "atheist"))
    wps.append(WordPair("athene", "athens"))
    wps.append(WordPair("aristotelian", "aristotelianism"))
    RunExperiments(wps)
