from typing import List

from src.Core.Dataset.DiscreteScale import DiscreteScale
from src.Core.Orthographic.IMetric import IMetric
from src.Core.WordPair import WordPair
from src.Core.WordSim.IWordSimilarity import IWordSimilarity


class EditDistance(IWordSimilarity, IMetric):
    """
    Copied from StringSimilarityFamily for Cython support.
    The normalized version is also an IWordSimilarity.
    """
    def WordSimilarity(self, w1: str, w2: str) -> float:
        return 1 - self.NormalizedDistance(w1, w2)

    def SimilarityScale(self) -> DiscreteScale:
        return DiscreteScale(0, 1)

    def NormalizedDistance(self, s0: str, s1: str):
        m_len = max(len(s0), len(s1))
        if m_len == 0:
            return 0.0
        return self.Distance(s0, s1) / m_len

    def Distance(self, s0: str, s1: str):
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 0.0
        if len(s0) == 0:
            return len(s1)
        if len(s1) == 0:
            return len(s1)

        v0 = [0] * (len(s1) + 1)
        v1 = [0] * (len(s1) + 1)

        for i in range(len(v0)):
            v0[i] = i

        for i in range(len(s0)):
            v1[0] = i + 1
            for j in range(len(s1)):
                cost = 1
                if s0[i] == s1[j]:
                    cost = 0
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            v0, v1 = v1, v0

        return v0[len(s1)]

    def __str__(self) -> str:
        return "nedit"

    def IsMetric(self):
        return None  # It includes both versions, so I cannot answer. IsMetric() is not a good question at the class level. The normalized version is not a metric.

if __name__ == "__main__":

    def CalculateEditDistances(wps: List[WordPair]):
        edit = EditDistance()
        for wp in wps:
            osim = 10 * (1 - edit.NormalizedDistance(wp.Word1, wp.Word2))
            print(str(wp) + "  " + str(osim))

    # Handpicked Examples
    wordpairs: List[WordPair] = []
    wordpairs.append(WordPair("processor", "professor"))
    wordpairs.append(WordPair("poison", "prison"))
    wordpairs.append(WordPair("academia", "academic"))
    wordpairs.append(WordPair("verification", "vivification"))
    wordpairs.append(WordPair("verbaliser", "verbalizer"))
    wordpairs.append(WordPair("shamelessness", "shapelessness"))
    wordpairs.append(WordPair("shakespeare", "shakespearean"))
    wordpairs.append(WordPair("assignment", "reassignment"))
    wordpairs.append(WordPair("westernisation", "westernization"))
    wordpairs.append(WordPair("vascularisation", "vascularization"))  # 0.93
    wordpairs.append(WordPair("unacceptability", "unadaptability"))
    wordpairs.append(WordPair("unpredictability", "unprofitability"))
    wordpairs.append(WordPair("viscount", "discount"))
    wordpairs.append(WordPair("action", "auction"))
    wordpairs.append(WordPair("tyrannosaur", "tyrannosaurus"))  # Did I solve this with WordNet? If so, include it.
    wordpairs.append(WordPair("article", "particle"))
    wordpairs.append(WordPair("banana", "bandana"))
    wordpairs.append(WordPair("natural", "contrary"))
    
    wordpairs.append(WordPair("car", "bar"))
    wordpairs.append(WordPair("glowing", "slowing"))
    wordpairs.append(WordPair("tablo", "kablo"))
    wordpairs.append(WordPair("biracılık", "kiracılık"))
    wordpairs.append(WordPair("mindlessness", "windlessness"))
    wordpairs.append(WordPair("tencerelerimizden", "pencerelerimizden"))
    wordpairs.append(WordPair("improve", "impover"))
    CalculateEditDistances(wordpairs)
