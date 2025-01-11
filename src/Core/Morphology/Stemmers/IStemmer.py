from abc import ABC, abstractmethod

class IStemmer(ABC):
    """
    We use the same schema for Stem/Lemmatize.
    """

    @abstractmethod
    def Stem(self, word:str):
        """
        We use the same schema for Stem/Lemmatize. Both mean finding the root rather than analyzing.
        Generally, stem is used as a superficial string operation and lemmatize as a morphological operation. But in practice, their schemas are the same. https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html
        :param word:
        :return: Returns the root/lemma/stem as a string. Does not return analysis.
        """
        pass
