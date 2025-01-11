from typing import Dict

from src.Core.Languages.Grammars.IGrammar import IGrammar
from src.Core.Languages.Grammars.InvariantGrammar import InvariantGrammar
from src.Core.Languages.Grammars.TRGrammar import TRGrammar
from src.Core.Languages.Language import Language


class LinguisticContext(object):
    """
    Object that holds language, culture, and other context information dependent on the language.
    All parameters for different languages should be parsable with this context.
    """
    def __init__(self, language:Language, grammar:IGrammar = None) -> None:
        super().__init__()
        self.Language:Language = language
        if(not self.Language): raise Exception("Language cannot be None!")
        self.Grammar = grammar
        if(not grammar): self.Grammar = self.BuildGrammar()

    def BuildGrammar(self)->IGrammar:
        return LinguisticContext.BuildGrammarByCode(self.Language.Code)

    @staticmethod
    def BuildGrammarByCode(langCode:str)->IGrammar:
        if(langCode == LinguisticContext.GetTurkishCode()):
            return TRGrammar()
        elif(langCode == LinguisticContext.GetEnglishCode()):
            return InvariantGrammar()
        else:
            raise NotImplementedError("IGrammar is not supported for the language! lang: " + langCode)

    @staticmethod
    def GetAllLanguages()->Dict[str,Language]:
        """
        Returns the list of all registered languages in the system with their codes.
        Currently, only Turkish and English are supported. Relationships with multilingual frameworks have not been established yet.
        :return:
        """
        langs = {}
        langs[LinguisticContext.GetEnglishCode()] = Language(LinguisticContext.GetEnglishCode(),"English")       # For now, we are using nltk codes, not Polyglot's. https://polyglot.readthedocs.io/en/latest/Detection.html#supported-languages
        langs[LinguisticContext.GetTurkishCode()] = Language(LinguisticContext.GetTurkishCode(),"Turkish")
        return langs

    @staticmethod
    def GetTurkishCode():
        return "tr"     #ISO 639 standard is 'tur'.

    @staticmethod
    def GetEnglishCode():
        return "eng"

    def BuildContextWithInvariantGrammar(langCode:str, langName:str):
        """
        Builds a language context with default invariant grammar. Use this method when the language does not contain a specific grammar.
        :return:
        """
        return LinguisticContext(Language(langCode,langName), InvariantGrammar())

    @staticmethod
    def BuildContextByCode(langCode:str):
        lang = LinguisticContext.GetAllLanguages()[langCode]
        return LinguisticContext(lang)

    @staticmethod
    def BuildEnglishContext():
        """
        Produces context for English without needing to know the English code.
        :return:
        """
        lang = LinguisticContext.GetAllLanguages()[LinguisticContext.GetEnglishCode()]
        return LinguisticContext(lang)

    @staticmethod
    def BuildTurkishContext():
        """
        Produces context for Turkish without needing to know the Turkish code.
        :return:
        """
        lang = LinguisticContext.GetAllLanguages()[LinguisticContext.GetTurkishCode()]
        return LinguisticContext(lang)

    def __str__(self) -> str:
        return str(self.Language) + " Context"

if __name__ == '__main__':

    print(LinguisticContext.GetAllLanguages())

