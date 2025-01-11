# coding=utf-8
import unittest
from typing import Dict, Optional, Tuple, List
from unittest import TestCase

from pandas import DataFrame

from src.Core.Dataset.Dataset import Dataset
from src.Core.Languages.LinguisticContext import LinguisticContext
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.IRootDetector import IRootDetector
from src.Core.Morphology.SegmentedWord import SegmentedWord
from src.Core.Preprocessing.Preprocessors import Preprocessors
from src.Core.Segmentation.SegmentorBase import SegmentorBase
from src.Tools import StringHelper
from src.Tools.Logger import logp


class MorphoLexSegmentedDataset(SegmentorBase, Dataset, IRootDetector):
    """
    For English, a 70K derivational morphology dataset.
    xlrd must also be installed for Excel. "pip install xlrd" "Install xlrd >= 0.9.0 for Excel support"
    This dataset omits inflectional suffixes in segmentation. For example: surefootedness --> {(sure)}{(foot)}>ness> or typesetters --> {(typo)}{(set)}>er>
    In addition to providing all prefixes, roots, and affixes, the dataset also provides derivational bases. I interpret a base as a root transforming into another root through derivation.
    For example: in {(socio)>al>}>ism>, the main root is socio, but in social, it has become a root by taking a suffix. In such cases, I consider the extra root information as other roots.from typing import Optional, List, Dict, Set
    """

    def __init__(self, dsFilePath: str, autoLoad: bool = True, loadMetadataOnly: bool = False,
                 caseSensitive=True) -> None:
        SegmentorBase.__init__(self)
        Dataset.__init__(self)
        IRootDetector.__init__(self)

        self.DSFilePath = dsFilePath
        self._DFSeg: DataFrame = None
        self.Segmentations: Dict[str, str] = {}
        self.MetaSuffixes = set()
        self.MetaPrefixes = set()
        self.Roots = set()
        self.LoadMetadataOnly: bool = loadMetadataOnly
        self.CaseSensitive: bool = caseSensitive
        if (autoLoad): self._Load()
        self.LinContext: LinguisticContext = LinguisticContext.BuildEnglishContext()

    def SegmentImpl(self, word: str) -> SegmentedWord:
        expr = self.Segmentations.get(word)
        if (expr is None): return SegmentedWord(word)
        return self.TryParseToSegmentedWordOrDefault(expr)

    def ToConfigValue(self) -> str:
        return self.Name().lower()

    def DetectRoots(self, surface: str, priorPOS: POSTypes = None) -> List[str]:
        expr = self.Segmentations.get(surface)  # Actually, this dataset also has POS information. I'm not using it for now.
        if (expr is None): return []
        sword: SegmentedWord = self.ParseToSegmentedWord(expr)
        if (sword is None): return [surface]
        oroots = [o.replace("_", "") for o in sword.OtherRoots]
        return [sword.Root.replace("_",
                                   "")] + oroots  # AlternativeRoots are not available in MorphoLex. It only returns linear OtherRoots.

    def Name(self):
        return "MorphoLex"

    def Persist(self, path: str):
        """
        Writes to a separate flat file instead of the original excel file
        Additionally, it saves the Metas to flat files.
        """
        logp("Saving process is starting...", anyMode=True)

        # segmentations
        if (len(self.Segmentations) > 0):
            # sort first
            list: List[str, str] = []
            for k, v in self.Segmentations.items():
                if (k and v):
                    list.append([str(k), str(v)])
            list.sort()

            # persist
            f = open(path, "w+")
            for pair in list:
                f.write(pair[0] + "\t" + pair[1] + "\n")  # tab-seperated
            f.close()
            logp("Saving process finished. Path: " + path, anyMode=True)
        else:
            logp("Skipping the saving process of segmentations. Only processing metadata.")

        # persist metadatas
        logp("Persisting metadatas..", True)
        extension: str = path.split(".")[1]

        # prefix
        prefixesPath = path.replace("." + extension, "-MetaPrefixes." + extension)
        f = open(prefixesPath, "w+")
        sortedMetaPrefixes = sorted(self.MetaPrefixes)
        for prefix in sortedMetaPrefixes:
            f.write(prefix + "\n")
        f.close()

        # suffixes
        suffixesPath = path.replace("." + extension, "-MetaSuffixes." + extension)
        f = open(suffixesPath, "w+")
        sortedMetaSuffixes = sorted(self.MetaSuffixes)
        for suffix in sortedMetaSuffixes:
            f.write(suffix + "\n")
        f.close()

        # roots
        rootsPath = path.replace("." + extension, "-Roots." + extension)
        f = open(rootsPath, "w+")
        sortedRoots = sorted(self.Roots)
        for r in sortedRoots:
            f.write(r + "\n")
        f.close()

        logp("All done!", anyMode=True)

    def _FormatToUpperMetaMorpheme(self, originalAffix: str) -> str:
        """
        Converts to uppercase and removes leading and trailing symbols to convert to our standard metamorpheme.
        :param originalMorpheme:
        :return:
        """
        return originalAffix.replace("<", "").replace(">", "").upper()

    @staticmethod
    def TryParseToSegmentedWordOrDefault(morphoLex: str) -> Optional[SegmentedWord]:
        """
        If it cannot parse for some reason, it returns the entire surface as a default segment.
        :return:
        """
        try:
            return MorphoLexSegmentedDataset.ParseToSegmentedWord(morphoLex)
        except:
            return SegmentedWord(morphoLex)

    @staticmethod
    def ParseToSegmentedWord(morphoLex: str) -> Optional[SegmentedWord]:
        # fixes
        morphoLex = morphoLex.replace("_", "")  # fix for https://github.com/hugomailhot/MorphoLex-en/issues/4
        morphoLex = morphoLex.replace("'", "")  # fix for D'ETAT  {d'etat} case
        newExpr: str = morphoLex

        # prefixes
        prefixCount = int(newExpr.count("<") / 2)
        prefixes = []
        for prefixIndex in range(0, prefixCount):
            prefix = StringHelper.FindFirstBlockInBetween(newExpr, "<", "<")
            if (prefix):
                prefixes.append(prefix)
                newExpr = newExpr.replace("<" + prefix + "<", "")

        # suffixes
        newExpr = StringHelper.RemoveLastChar(newExpr).replace(">>", ">").replace(">", "+")
        newExpr = StringHelper.RemoveLastCharIf(newExpr, '+')

        # root (single root assumption on expression)
        newExpr = newExpr.replace("{", "").replace("}", "").replace("++", "+").replace("(", "_").replace(")",
                                                                                                         "").replace(
            "__",
            "_")  # Parentheses are now considered other roots, not suffixes.
        newExpr = newExpr.replace("+_",
                                  "+")  # Parentheses and curly braces should not start after the suffix. For example: {(violon)(cello)>ist>} here ism should actually be a suffix.
        newExpr = StringHelper.RemoveLastCharIf(newExpr, '+')
        if newExpr[0] == '+': newExpr = "_" + newExpr[1:]

        # segmentation
        sword: SegmentedWord = SegmentedWord.ParseUnitExpression(newExpr)
        if (sword is None): return None
        sword.Prefixes = prefixes

        surfaceCand = "".join(sword.Prefixes) + sword.Root.replace("_", "") + "".join(
            sword.Suffixes)

        # OTHER ROOTS (this section returns other alternative root candidates outside the morpheme segmentation given from left to right.)
        # 1. Parenthesis blocks (these determine other roots in a linear sequence)
        exprForOtherRoots = morphoLex
        exprForOtherRoots = StringHelper.RemoveLastCharIf(exprForOtherRoots,
                                                          '}')  # We are not interested in parentheses that encompass the entire word. I don't know why MorphoLex put these.
        exprForOtherRoots = StringHelper.RemoveFirstCharIf(exprForOtherRoots, '{')
        exprForOtherRoots = StringHelper.RemoveLastCharIf(exprForOtherRoots, ')')
        exprForOtherRoots = StringHelper.RemoveFirstCharIf(exprForOtherRoots, '(')
        existence: int = exprForOtherRoots.count("(")
        for orid in range(0, existence):
            otherRootBlock = StringHelper.FindFirstBlockInBetween(exprForOtherRoots, "(", ")")
            if (otherRootBlock is None): continue
            rootcand = otherRootBlock.replace("{" + otherRootBlock + "}", "").replace("<", "").replace("(", "").replace(
                ")", "")
            if (rootcand != sword.Root.replace("_",
                                               "") and "_" + rootcand not in sword.OtherRoots and rootcand != surfaceCand):
                if (rootcand not in sword.Suffixes):  # MorphoLex sometimes puts the suffix in parentheses. So if you added it as a suffix, don't add it as an other root. For example: "{(voc)>abulary>}>ian>{(ism)}
                    sword.OtherRoots.append("_" + rootcand)
            exprForOtherRoots = exprForOtherRoots.replace("(" + rootcand + ")", "")

        # 2. Curly blocks {} (these determine other roots non-linearly)
        exprForAlterRoots = morphoLex.replace("(", "").replace(")", "")  # We are not very interested in parentheses here.
        existence: int = exprForAlterRoots.count("{")
        for arid in range(0, existence):
            alterRootBlock = StringHelper.FindFirstBlockInBetween(exprForAlterRoots, "{", "}")
            if (alterRootBlock is None): continue
            alterRoot = alterRootBlock.replace("(", "").replace(")", "").replace("<", "").replace(">", "")  # Also remove PrefixMorpheme prefixes.
            if (alterRoot != sword.Root.replace("_",
                                                "") and "_" + alterRoot not in sword.OtherRoots and alterRoot != surfaceCand):
                sword.AlternativeRoots.append(
                    "_" + alterRoot)  # Root, OtherRoot, or AlterRoot all must have _ at the beginning.
            exprForAlterRoots = exprForAlterRoots.replace("{" + alterRoot + "}", "")
        return sword

    @staticmethod
    def LoadFromText(path: str, loadMetadatas: bool = False, caseSensitive: bool = True):
        """Allows loading from our custom text file instead of the original one"""
        ds: MorphoLexSegmentedDataset = MorphoLexSegmentedDataset(path, autoLoad=False, caseSensitive=caseSensitive)
        with open(path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                segs = line.split("\t")
                skey = segs[0] if caseSensitive else segs[0].lower()
                ds.Segmentations[skey] = Preprocessors.NormalizeWhitespaces(segs[1])

        # Metadatas
        if (loadMetadatas):
            logp("Loading metadatas too...", True)
            extension: str = path.split(".")[1]

            # prefix
            prefixesPath = path.replace("." + extension, "-MetaPrefixes." + extension)
            with open(prefixesPath, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    w = Preprocessors.NormalizeWhitespaces(line)
                    ds.MetaPrefixes.add(w)
            # suffix
            suffixesPath = path.replace("." + extension, "-MetaSuffixes." + extension)
            with open(suffixesPath, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    w = Preprocessors.NormalizeWhitespaces(line)
                    ds.MetaSuffixes.add(w)
            # root
            rootPath = path.replace("." + extension, "-Roots." + extension)
            with open(rootPath, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    w = Preprocessors.NormalizeWhitespaces(line)
                    ds.Roots.add(w)
        logp("Dataset loaded from flat text(s).", True)
        return ds

    def _Load(self):
        """Loads from the original excel file. Loading is slow because the excel file contains many sheets and columns."""
        # Load
        import pandas as pd
        logp("Excel will be loaded...", anyMode=True)
        self._DFSeg = DataFrame()
        if (not self.LoadMetadataOnly):
            for i in range(1, 31):  # 31       # All sheets containing data. Distributed according to their distributions.
                logp("sheet#: " + str(i), True)
                dftemp = pd.read_excel(self.DSFilePath, sheet_name=i, header=0, usecols="B,C,F")
                if (i == 1):
                    self._DFSeg = dftemp
                else:
                    self._DFSeg = self._DFSeg.append(dftemp)

            # Index
            self.Segmentations = {}
            for index, row in self._DFSeg.iterrows():
                w = row.Word if self.CaseSensitive else row.Word.lower()
                self.Segmentations[w] = row.MorphoLexSegm

        # Metadatas
        dfTemp = DataFrame()
        # prefixes
        logp("Loading metadatas...", True)
        dftemp = pd.read_excel(self.DSFilePath, sheet_name=31, header=0, usecols="A")
        for index, row in dftemp.iterrows():
            metaPrefix = self._FormatToUpperMetaMorpheme(row.morpheme)
            self.MetaPrefixes.add(metaPrefix)
        # suffixes
        dftemp = pd.read_excel(self.DSFilePath, sheet_name=32, header=0, usecols="A")
        for index, row in dftemp.iterrows():
            metaSuffix = self._FormatToUpperMetaMorpheme(row.morpheme)
            self.MetaSuffixes.add(metaSuffix)
        # roots
        dftemp = pd.read_excel(self.DSFilePath, sheet_name=33, header=0, usecols="A")
        for index, row in dftemp.iterrows():
            root = str(row.morpheme).replace("(", "").replace(")", "")
            self.Roots.add(root)

        logp("Excel loaded.", anyMode=True)
        return self


class MorphoLexSegmentedDatasetTest(TestCase):

    def test_ParseToSegmentedWord_OneFromAll_Return(self):
        sword: SegmentedWord = MorphoLexSegmentedDataset.ParseToSegmentedWord("{<de<(script)>ion>}")
        self.assertEqual(sword.Root, "_script")
        self.assertEqual(1, sword.SuffixCount())
        self.assertEqual(1, len(sword.Prefixes))

    def test_ParseToSegmentedWord_NotSupportedChars_ReturnNull(self):
        sword: SegmentedWord = MorphoLexSegmentedDataset.ParseToSegmentedWord(
            "{d'etat}")  #There's an entry {d'etat} in the original dataset. The apostrophe is sanitized, but since it doesn't have parentheses, it's invalid.

        self.assertIsNone(sword)

    def test_ParseToSegmentedWord_FullAffixesAndMultiMorphemeBase_ReturnBaseAsRoot(self):
        sword: SegmentedWord = MorphoLexSegmentedDataset.ParseToSegmentedWord("<de<{(nation)}>al>>ize>>ion>")
        self.assertEqual(sword.Root, "_nation")
        self.assertEqual(3, sword.SuffixCount())
        self.assertEqual("de", sword.Prefixes[0])
        self.assertEqual(0, len(sword.OtherRoots))

    def test_ParseToSegmentedWord_AffixOnBase_ReturnBaseWithAffixAsRoot(self):
        sword: SegmentedWord = MorphoLexSegmentedDataset.ParseToSegmentedWord("{<in<(stitute)}>ion>>al>>ize>")
        self.assertEqual(sword.Root, "_stitute")
        self.assertEqual(3, sword.SuffixCount())
        self.assertEqual("in", sword.Prefixes[0])
        self.assertEqual("_institute", sword.AlternativeRoots[0])

    def test_ParseToSegmentedWord_MultipleBases_ReturnBasesAsASingleRootAndOthers(self):  # The ones in parentheses are other roots, and the ones in curly braces can be alternatives.
        sword: SegmentedWord = MorphoLexSegmentedDataset.ParseToSegmentedWord("{(air)}{(craft)}{(men)}")
        self.assertEqual(sword.Root, "_air")
        self.assertEqual(2, len(sword.OtherRoots))
        self.assertEqual("_craft", sword.OtherRoots[0])
        self.assertEqual("_men", sword.OtherRoots[1])
        # They should not be counted as suffixes. OtherRoots are already supported in linear mode.
        self.assertEqual(0, sword.Suffixes.__len__())  # Previous comment: It is entirely normal for the same "craft" morpheme to appear both as a suffix and as an OtherRoot. It is counted as a suffix because it is a morpheme within the left-to-right expression. It is counted as an OtherRoot because MorphoLex marks the morpheme as a root by surrounding it with ().
        self.assertEqual(0, sword.AlternativeRoots.__len__())  # Since they are all linear other roots, curly braces should not yield extra alternative roots.


    def test_FormatToUpperMetaMorpheme_Prefix_Format(self):
        ds = MorphoLexSegmentedDataset("dummypath", False)
        actual = ds._FormatToUpperMetaMorpheme("<auto<")
        self.assertEqual("AUTO", actual)

    def test_FormatToUpperMetaMorpheme_Suffix_Format(self):
        ds = MorphoLexSegmentedDataset("dummypath", False)
        actual = ds._FormatToUpperMetaMorpheme("<ist<")
        self.assertEqual("IST", actual)

    def test_ParseToSegmentedWord_TriplePrefixes_ParseRootAndPrefixes(self):
        sword: SegmentedWord = MorphoLexSegmentedDataset.ParseToSegmentedWord("<un<<re<{<co<(struct)}")  # 3-1-0
        self.assertEqual(3, len(sword.Prefixes))
        self.assertEqual("un", sword.Prefixes[0])
        self.assertEqual("re", sword.Prefixes[1])
        self.assertEqual("co", sword.Prefixes[2])
        self.assertEqual("_struct", sword.Root)
        self.assertEqual("_costruct", sword.AlternativeRoots[0])

    def test_ParseToSegmentedWord_ALL30PLUSSCENARIOS(self):
        cases: List[str, str, str, str, str] = []  # expr,root,otherroot1,otherroot2,otherroot3,alterroot1
        cases.append(["{(algorithm)}", "_algorithm", None, None, None, None])  # 0-1-0
        cases.append(["{(animal)}", "_animal", None, None, None, None])  # 0-1-0
        cases.append(["{(algorithm)}>ic>", "_algorithm", None, None, None, None])  # 0-1-1
        cases.append(["{(algebra)}>ic>>al>", "_algebra", None, None, None, None])  # 0-1-2
        cases.append(["{(allegor)>ic>}>al>>ly>", "_allegor", None, None, None, "_allegoric"])  # 0-1-3
        cases.append(["{(sense)}>ate>>ion>>al>>ist>", "_sense", None, None, None, None])  # 0-1-4
        cases.append(["{(wood)}(men)", "_wood", "_men", None, None, None])  # 0-2-0
        cases.append(["{(violon)(cello)>ist>}", "_violon", "_cello", None, None, "_violoncelloist"])  # 0-2-1
        cases.append(["{(wrong)}{(head)}>ness>", "_wrong", "_head", None, None, None])  # 0-2-1_2
        cases.append(["{(voc)>abulary>}>ian>{(ism)}", "_voc", None, None, None,"_vocabulary"])
        cases.append(["(petro){(chem)>ic>>al>}", "_petro", "_chem", None, None, "_chemical"])  # 0-2-2_2
        cases.append(["{(typo)}(graph)>ic>>al>>ly>", "_typo", "_graph", None, None, None])  # 0-2-3
        cases.append(["(tele){(photo)}{(graph)}", "_tele", "_photo", "_graph", None, None])  # 0-3-0
        cases.append(["(tele){(photo)(graph)>y>}", "_tele", "_photo", "_graph", None, "_photography"])  # 0-3-1
        cases.append(["(psycho){(pharma)(log)>ic>}>al>", "_psycho", "_pharma", "_log", None, "_pharmalogic"])  # 0-3-2
        cases.append(["<up<{(date)}", "_date", None, None, None, None])  # 1-1-0
        cases.append(["<un<{(conscious)}>ness>", "_conscious", None, None, None, None])  # 1-1-1
        cases.append(["<un<{(ceremony)}>ious>>ness>", "_ceremony", None, None, None, None])  # 1-1-2
        cases.append(["<un<{(profess)>ion>}>al>>ly>", "_profess", None, None, None, "_profession"])  # 1-1-3
        cases.append(["{<in<(stitute)}>ion>>al>>ize>>ion>", "_stitute", None, None, None, "_institute"])  # 1-1-4
        cases.append(["{<re<(pair)}{(men)}", "_pair", "_men", None, None, "_repair"])  # 1-2-0
        cases.append(["{(<re<(plic)>ate>)}", "_plic", None, None, None, None])  # 1-2-1
        cases.append(["<micro<{(bio)(log)>ic>}>al>", "_bio", "_log", None, None,"_biologic"])  # 1-2-2
        cases.append(["<auto<{(bio)(graph)>ic>}>al>>ly>", "_bio", "_graph", None, None, "_biographic"])  # 1-2-3
        cases.append(["(electro){<en<(cephalo)(gram)}", "_electro", "_cephalo", "_gram", None, "_encephalogram"])  # 1-3-0
        cases.append(["<un<{<pre<(judic)}", "_judic", None, None, None, "_prejudic"])  # 2-1-0 - Double Prefix.
        cases.append(["<un<{<re<(strict)}>ly>", "_strict", None, None, None, "_restrict"])  # 2-1-1
        cases.append(["<im<{<a<(propri)>ate>}>ly>", "_propri", None, None, None,"_apropriate"])  # 2-1-2
        cases.append(["<un<{<ex<(cept)}>ion>>able>>y>", "_cept", None, None, None, "_except"])  # 2-1-3
        cases.append(["<un<{<a<(know)(ledge)}", "_know", "_ledge", None, None, "_aknowledge"])  # 2-2-0
        cases.append(["<un<<re<{<co<(struct)}", "_struct", None, None, None, "_costruct"])  # 3-1-0
        #
        cases.append(["(myco){(bacteri)>a>}", "_myco", "_bacteri", None, None, "_bacteria"])  # MYCOBACTERIA

        # OtherRoot vs AlternativeRoots
        cases.append(["<un<<re<{<co<(struct)}", "_struct", None, None, None,
                      "_costruct"])  # Curly ones are aRoot, straight ones are otherRoot !? !?

        # special scenarios
        cases.append(["{<in<(_here)}>ant>", "_here", None, None, None,
                      "_inhere"])  # buggy instance: https://github.com/hugomailhot/MorphoLex-en/issues/4

        for case in cases:
            sword = MorphoLexSegmentedDataset.ParseToSegmentedWord(case[0])
            actualRoot = sword.Root

            actualOtherRoot1 = sword.OtherRoots[0] if len(sword.OtherRoots) > 0 else None
            otherRootPassed1 = True if actualOtherRoot1 is None else actualOtherRoot1 == case[2]

            actualOtherRoot2 = sword.OtherRoots[1] if len(sword.OtherRoots) > 1 else None
            otherRootPassed2 = True if actualOtherRoot2 is None else actualOtherRoot2 == case[3]

            actualOtherRoot3 = sword.OtherRoots[2] if len(sword.OtherRoots) > 2 else None
            otherRootPassed3 = True if actualOtherRoot3 is None else actualOtherRoot3 == case[4]

            # alternate root
            actualAlterRoot1 = sword.AlternativeRoots[0] if len(sword.AlternativeRoots) > 0 else None
            alterRootPassed1 = True if actualAlterRoot1 is None else actualAlterRoot1 == case[5]

            # recap
            passed = (case[1] == actualRoot) and (
                        otherRootPassed1 and otherRootPassed2 and otherRootPassed3 and alterRootPassed1)
            msg: str = "passed: " + str(case) if passed else "failed: " + str(case)
            print(msg)
            self.assertTrue(passed, msg)
        print("passed " + str(len(cases)) + " test cases!")


if __name__ == "__main__":
    unittest.main()
    # exit()

    # Excel to Flat Text
    # path:str = Resources.GetOthersPath("MorphoLEX_en.xlsx")
    # morphoLex:MorphoLexSegmentedDataset = MorphoLexSegmentedDataset(path,autoLoad=True,loadMetadataOnly=False)
    # morphoLex.Persist(Resources.GetOthersPath("MorphoLEXTest.txt"))     # Convert to flat

    # Read from flat text.
    # txtpath:str = Resources.GetOthersPath("MorphoLEX2.txt")
    # morphoLex:MorphoLexSegmentedDataset = MorphoLexSegmentedDataset.LoadFromText(txtpath,loadMetadatas=True)
    # affixSet = morphoLex.MetasToAffixSet()
    # AffixSetLoader().Persist(affixSet,"MorphoLEX")
    # print("MorphoLex text has " + str(len(morphoLex.Segmentations)) + " entries.")