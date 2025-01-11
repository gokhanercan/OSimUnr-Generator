# -*- coding: utf-8 -*-
import unittest
from typing import List, Dict, Set
from unicode_tr import unicode_tr
from src.Core.Languages.Grammars.IGrammar import IGrammar
from src.Tools import StringHelper


class TRGrammar(IGrammar):

    def __init__(self) -> None:
        super().__init__()
        self._Vowels = {'a','e','i','ı','u','ü','o','ö','â','î','û','ê'}
        self._AccentMappings = {"â":"a", "î":"i", "û":"u", "ê":"e"}  # Uppercase support should be added. There may be different accent marks. Lowercased ones were enough for OSimUnr study.
        self._AccentChars:Set[str] = set()
        self.SetAccents(self._AccentMappings)

    def ToLowerCase(self, input:str)->str:
        ustr = unicode_tr(input)
        return ustr.lower()

    def ToUpperCase(self, input:str)->str:
        ustr = unicode_tr(input)
        return ustr.upper()

    def GetAlphabet(self) -> List[str]:
        return ["A","B","C","Ç","D","E","F","G","Ğ","H","I","İ","J","K","L","M","N","O","Ö","P","R","S","Ş","T","U","Ü","V","Y","Z"]

    def IsVowel(self, char:chr)->bool:
        """
        Returns whether it is a vowel.
        :param char:
        :return:
        """
        lchar:chr = self.ToLowerCase(char)
        return lchar in self._Vowels

    #region Accents
    def HasAccent(self, word:str)->bool:
        if(StringHelper.IsNullOrEmpty(word)): return False
        if any(w in word for w in self._AccentChars):
            return True
        return False

    def SetAccents(self, accentMappings:Dict[str,str]):
        self._AccentMappings = accentMappings
        for a in self._AccentMappings:
            self._AccentChars.add(a)

    def GetAccentChars(self)->Set[str]:
        return self._AccentChars

    def ReduceAccents(self, word:str)->str:
        """
        Converts the accented letters of the given word to their Latin equivalents.
        Only supports lowercased ones.
        :param word:
        :return:
        """
        if(not self.HasAccent(word)): return word
        res:str = word
        for k,v in self._AccentMappings.items():  # Not the most optimal method. We produced strings continuously.
            res = res.replace(k,v)
        return res

    #endregion



#UNITTEST
class TestTRGrammar(unittest.TestCase):
    def test_CapitalILetter_ToLowerCase(self):
        self.assertEqual(u"istanbul",TRGrammar().ToLowerCase(u"İSTANBUL"))
        self.assertEqual(u"ısparta",TRGrammar().ToLowerCase(u"ISPARTA"))

    def test_LowerILetter_ToUpperCase(self):
        self.assertEqual(u"İSTANBUL",TRGrammar().ToUpperCase(u"istanbul"))
        self.assertEqual(u"ISPARTA",TRGrammar().ToUpperCase(u"ısparta"))

    #region Accents
    def test_GetAccents_GetDefaults(self):
        self.assertEqual(4,TRGrammar().GetAccentChars().__len__())
    def test_HasAccents_Accent_True(self):
        self.assertTrue(TRGrammar().HasAccent("günahkârlık"))
    def test_HasAccents_Accent_False(self):
        self.assertFalse(TRGrammar().HasAccent("günahkarlık"))
    def test_ReduceAccents_AccentedWord_ReduceToLatin(self):
        self.assertEqual("günahkarlık", TRGrammar().ReduceAccents("günahkârlık"))
    def test_ReduceAccents_NonAccentedWord_DoNothing(self):
        self.assertEqual("günahkarlık", TRGrammar().ReduceAccents("günahkarlık"))
    #endregion


if __name__ == '__main__':
    unittest.main()