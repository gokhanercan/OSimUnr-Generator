import unittest
from enum import Enum
from unittest import TestCase
from src.Tools import StringHelper


class UnitForms(Enum):
    Surface = 0
    Root = 1
    Suffix = 2  # Prefix or Suffix
    Expression = 3
    Prefix = 4


class ModelConvensions(object):
    """
    Our conventions do not yet support AlternativeRoot, but they do support OtherRoots. Full linear structure support is available.
    """

    def __init__(self):
        self.FormPrefixes: FormPrefixes = FormPrefixes()        #This term prefix is not linguistic prefix, but a term for the first character of a word.

    def IsRoot(self, word: str):
        if StringHelper.IsNullOrEmpty(word):
            return False
        return (
            word[0] == self.FormPrefixes.Root
            and word.count(self.FormPrefixes.Suffix) == 0
            and word.count(self.FormPrefixes.Root) == 1
        )  # Checking if it has only a single root.

    def IsPrefix(self, word: str):
        return word[0] == self.FormPrefixes.Prefix and (not self.HasRoot(word)) and word.count(self.FormPrefixes.Suffix) == 0

    def HasPrefix(self, expr: str):
        """
        Returns whether the entire expression contains a prefix.
        :param word:
        :return:
        """
        return expr[0] == self.FormPrefixes.Prefix

    def HasRoot(self, expr: str):
        """
        Returns whether the entire expression contains a root. Multiple roots are allowed.
        :param word:
        :return:
        """
        return expr.__contains__(self.FormPrefixes.Root)

    def RootCount(self, expr: str):
        """
        Returns the total number of roots, including Root and OtherRoots.
        :param expr:
        :return:
        """
        return expr.count(self.FormPrefixes.Root)

    def IsSuffix(self, word: str):
        return word[0] == self.FormPrefixes.Suffix and (word.count(self.FormPrefixes.Suffix) == 1) and (word.count(self.FormPrefixes.Root) == 0)

    def IsSurface(self, word: str):
        return (not word.__contains__(self.FormPrefixes.Root)) and (not word.__contains__(self.FormPrefixes.Suffix))

    def IsExpression(self, unit: str):
        """
        Determines if the given string is an expression.
        :return:
        """
        if unit is None:
            return False
        hasRoot: bool = self.HasRoot(unit)
        if not hasRoot:
            return False
        multipleRoots: bool = self.RootCount(unit) > 1
        hasSuffix: bool = unit.__contains__(self.FormPrefixes.Suffix)
        return hasRoot and (hasSuffix or self.HasPrefix(unit) or multipleRoots)  # Must have at least one prefix or suffix to be an expression. Later, having multiple roots was also accepted.

    def FindUnitForm(self, unit: str):
        if self.IsSuffix(unit):
            return UnitForms.Suffix
        if self.IsRoot(unit):
            return UnitForms.Root
        if self.IsSurface(unit):
            return UnitForms.Surface
        if self.IsExpression(unit):
            return UnitForms.Expression
        if self.IsPrefix(unit):
            return UnitForms.Prefix
        raise Exception("Unit cannot be detected for unit: '" + unit + "'")


class ModelConvensionsTest(TestCase):

    def test_FormQueries(self):
        conv = ModelConvensions()
        self.assertEqual(True, conv.IsRoot("_göz"))
        self.assertEqual(False, conv.IsRoot("_göz+lHk"))
        self.assertEqual(False, conv.IsRoot("göz"))

        self.assertEqual(True, conv.IsSuffix("+lHK"))
        self.assertEqual(False, conv.IsSuffix("+lHK+CH"))
        self.assertEqual(False, conv.IsSuffix("+lHK_CH"))
        self.assertEqual(False, conv.IsSuffix("_root"))

        self.assertEqual(True, conv.IsSuffix("+gözlük"))
        self.assertEqual(False, conv.IsSuffix("_göz"))

        self.assertEqual(True, conv.IsPrefix("-a"))
        self.assertEqual(False, conv.IsPrefix("_göz"))

        self.assertEqual(True, conv.HasPrefix("-a_sosyal"))
        self.assertEqual(True, conv.HasPrefix("-anti-a_sosyal"))
        self.assertEqual(False, conv.HasPrefix("_sosyal+lHk"))
        self.assertEqual(False, conv.HasPrefix("_sosyal"))

        self.assertEqual(True, conv.HasRoot("_göz"))
        self.assertEqual(True, conv.HasRoot("-anti-a_sosyal"))
        self.assertEqual(False, conv.HasRoot("-anti+lHk"))
        self.assertEqual(False, conv.HasRoot("sosyal"))

    def test_DefaultConv_IsExpression(self):
        conv = ModelConvensions()
        self.assertEqual(False, conv.IsExpression("göz"))  # surface
        self.assertEqual(False, conv.IsExpression("+göz"))  # affix
        self.assertEqual(False, conv.IsExpression("_göz"))  # root
        self.assertEqual(False, conv.IsExpression("-göz"))  # prefix

        self.assertEqual(True, conv.IsExpression("-a_göz+lük"))
        self.assertEqual(True, conv.IsExpression("_göz+lük"))
        self.assertEqual(True, conv.IsExpression("_göz+lük+çü"))

        self.assertEqual(True, conv.IsExpression("-anti-a_sosyal"))
        self.assertEqual(True, conv.IsExpression("_air_craft_men"))  # Multiple root support.

    def test_DefaultConv_FindUnitForm(self):
        conv = ModelConvensions()
        self.assertEqual(UnitForms.Surface, conv.FindUnitForm("göz"))
        self.assertEqual(UnitForms.Root, conv.FindUnitForm("_göz"))
        self.assertEqual(UnitForms.Suffix, conv.FindUnitForm("+CH"))
        self.assertEqual(UnitForms.Expression, conv.FindUnitForm("_göz+CH"))
        self.assertEqual(UnitForms.Expression, conv.FindUnitForm("_göz+CH+lHk"))
        self.assertEqual(UnitForms.Expression, conv.FindUnitForm("-a_sosyal+lHk+lAr"))
        self.assertEqual(UnitForms.Expression, conv.FindUnitForm("-a_sosyal+lHk+lAr"))
        self.assertEqual(UnitForms.Expression, conv.FindUnitForm("_air_craft_men"))  # multiple root expr.

        # invalid expr.
        self.assertRaises(Exception, lambda: conv.FindUnitForm("+göz+lHk"))
        self.assertRaises(Exception, lambda: conv.FindUnitForm("-a+lHk"))

    def test_RootCount_WithOthers_Count(self):
        self.assertEqual(3, ModelConvensions().RootCount("_air_craft_men"))

    def test_IsExpression_Invalid_ReturnFalse(self):
        self.assertFalse(ModelConvensions().IsExpression(""))
        self.assertFalse(ModelConvensions().IsExpression(" "))
        self.assertFalse(ModelConvensions().IsExpression(None))
        self.assertFalse(ModelConvensions().IsExpression(";"))

    def test_IsRoot_Invalid_ReturnFalse(self):
        self.assertFalse(ModelConvensions().IsRoot(""))
        self.assertFalse(ModelConvensions().IsRoot(" "))
        self.assertFalse(ModelConvensions().IsRoot(None))


class FormPrefixes(object):

    def __init__(self):
        self.Root: str = "_"
        self.Suffix: str = "+"
        self.Prefix: str = "-"


if __name__ == '__main__':
    unittest.main()
