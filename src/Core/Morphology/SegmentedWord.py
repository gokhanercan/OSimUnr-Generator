import re
import copy
from typing import List, Set, Optional

from src.Core.Languages.Grammars.IGrammar import IGrammar
from src.Core.Morphology.ModelConvensions import ModelConvensions
from src.Tools import StringHelper


class SegmentedWord(object):
    """
    Holds the segmented form of a word. As 'Prefixes + Root(s) + Suffixes'
    """
    def __init__(self, root:str = "None", suffixes = None, prefixes = None):
        """
        :param root:
        :param suffixes:
        :param prefixes:
        """
        self.Root:str = root                        #single root assumption for now.        #This root is given directly with its suffix, but it shouldn't be.
        self.Suffixes = suffixes
        self.Prefixes:List[str] = prefixes      #Do not confuse this with other prefixes, this is the prefix as an affix.
        self.OtherRoots:List[str] = []          #Other roots that form a compound word in addition to the main root. This could also contain alternative roots. These roots do not break linearity.
        self.AlternativeRoots:List[str] = []    #Contains only alternative roots that break linearity.
        if(suffixes is None): self.Suffixes = []
        if(prefixes is None): self.Prefixes = []

    def IsOnRootForm(self)->bool:
        """
        It has no analyzed affix. Surface and root are the same. Even if it is a multiple root without an affix, it is considered a Root.
        :return:
        """
        return len(self.Suffixes) == 0 and len(self.Prefixes) == 0

    def GetSegments(self, linear:bool = True)->List[str]:
        """
        Returns all segments regardless of morphological definitions such as root, suffix.
        linear: If True, excludes alternatives. Default is true.
        """
        segments:List[str] = []

        for n in range(0,self.PrefixCount()):
            segments.append(self.Prefixes[n])

        #root
        segments.append(self.Root)

        #other root
        for n in range(0,self.OtherRoots.__len__()):
            segments.append(self.OtherRoots[n])

        #alt. root
        if(not linear):
            for n in range(0,self.AlternativeRoots.__len__()):
                aroot = self.AlternativeRoots[n]
                if not aroot.endswith('!'): aroot = aroot + "!"         #We always add ! at the end in alternative syntax.
                segments.append(aroot)

        for n in range(0,self.SuffixCount()):
            segments.append(self.Suffixes[n])

        return segments

    def ToMorphemes(self)->List[str]:
        """
        Returns a sequential list of all morphemes including all prefixes, roots, and suffixes.
        Assumes ``Prefixes + root + suffixes``.
        ToMorphemes does not return alternative roots. Use GetSegments(False) for that.
        :return:
        """
        morphemes = []
        for p in self.Prefixes:
            morphemes.append(p)
        morphemes.append(self.Root)
        for oroot in self.OtherRoots:
            morphemes.append(oroot)
        #AlternativeRoots are intentionally not returned
        for s in self.Suffixes:
            morphemes.append(s)
        return morphemes

    def ToMorphemesSet(self)->Set[str]:
        """
        Returns a set of unique morphemes, losing the order.
        Does not contain AlternativeRoots.
        :return:
        """
        morphemes = set()
        for p in self.Prefixes:
            morphemes.add(p)
        morphemes.add(self.Root)
        for oroot in self.OtherRoots:
            morphemes.add(oroot)
        #AlternativeRoots are intentionally not returned
        for s in self.Suffixes:
            morphemes.add(s)
        return morphemes

    def SuffixCount(self):
        if(self.Suffixes is None): return 0
        return len(self.Suffixes)

    def PrefixCount(self):
        if(self.Prefixes is None): return 0
        return len(self.Prefixes)

    def AffixCount(self):
        return self.PrefixCount() + self.SuffixCount()

    def RootCount(self):
        """
        Considers root and OtherRoots linearly. Does not consider AlternativeRoots.
        :return:
        """
        if StringHelper.IsNullOrEmpty(self.Root): return 0
        if(self.OtherRoots is None): return 1
        return self.OtherRoots.__len__()+1

    _SplitPattern = re.compile(r"[_|\-+]")

    @staticmethod
    def ParseUnitExpression(unitExpr:str):
        """
        Linear only: NonLinear not supported. Does not yet support parsing AlternativeRoots (_aroot?).
        But it supports parsing multiple roots (root + otherroots) linearly. See _air_craft_men
        :param unitExpr:
        :return:
        """
        conv = ModelConvensions()
        sword:SegmentedWord = None
        if not conv.IsExpression(unitExpr):
            if (conv.IsRoot(unitExpr)):
                sword = SegmentedWord(unitExpr)
                return sword
            return None

        #expression
        sword = SegmentedWord("")
        segments = SegmentedWord._SplitPattern.split(unitExpr)
        if(segments[0] == ""): segments = segments[1:]          #The first element can come empty if there is a prefix.

        #prefix
        prefixCount = unitExpr.count(conv.FormPrefixes.Prefix)
        if(prefixCount > 0):
            sword.Prefixes = segments[0:prefixCount]

        #root
        rootCount = unitExpr.count(conv.FormPrefixes.Root)
        if(rootCount > 0):
            roots = segments[prefixCount:prefixCount+rootCount]
            sword.Root = "_" + roots[0]       #roots are always parsed with CharPrefix.
            if(roots.__len__() >1):
                for i in range(1,rootCount):
                    sword.OtherRoots.append("_" + roots[i])

        #suffix
        suffixCount = unitExpr.count(conv.FormPrefixes.Suffix)
        if(suffixCount > 0):
            sword.Suffixes = segments[prefixCount+rootCount:prefixCount+rootCount+suffixCount]
        return sword

    @staticmethod
    def FromStrList(list:List[str]):
        """
        Converts the string segments we have into standard (root+suffixes) format without knowing their morphological counterparts like Root/Prefix/Suffix.
        Does not support Prefix, OtherRoot, and AlternativeRoot.
        :param list:
        :return:
        """
        if(len(list)) == 0: return None
        sword:SegmentedWord = SegmentedWord(list[0])
        sword.Suffixes = list[1:]
        return sword

    def BuildUnitExpression(self, linear:bool=True)->Optional[str]:
        """
        Default linear: splits the entire word into segments from left to right. Order is preserved.
        In non-linear mode, AlternativeRoots are also returned. Ex: -pre_root_otherroot+suffix syntax is used.
        :return:
        """
        conv = ModelConvensions()
        if StringHelper.IsNullOrEmpty(self.Root): return None

        expr:str = ""
        for prefix in self.Prefixes:
            expr += conv.FormPrefixes.Prefix + prefix

        #root
        rootFinal = self.Root if (self.Root.startswith(conv.FormPrefixes.Root)) else conv.FormPrefixes.Root + self.Root           #root prefix ensured version.
        if (self.IsOnRootForm() and self.RootCount()==1): return rootFinal      #If there is no Other root, no need to return the rest.
        expr += rootFinal

        #otherroots
        for oroot in self.OtherRoots:
            orootFinal = oroot if str(oroot).startswith(conv.FormPrefixes.Root) else conv.FormPrefixes.Root + oroot
            expr += orootFinal

        #alternative-roots
        if(not linear):
            for aroot in self.AlternativeRoots:
                arootFinal = aroot + "!" if str(aroot).startswith(conv.FormPrefixes.Root) else conv.FormPrefixes.Root + aroot + "!"
                expr += arootFinal

        #suffix
        for suffix in self.Suffixes:
            suffixFinal = suffix if str(suffix).startswith(conv.FormPrefixes.Suffix) else conv.FormPrefixes.Suffix + suffix
            expr += suffixFinal
        return expr

    @staticmethod
    def FromWithsToUnitExpr(withs:str):
        """
        Converts Withs expression to UnitExpression.
        Does not support Prefix, ORoot, ARoot.
        :param withs:
        :return:
        """
        unitExpr:str = "_" + withs #Since it does not support Prefix, ARoot, ORoot analyzer expressions for now. So putting _ at the beginning converts it to unit expression.
        return unitExpr

    @staticmethod
    def BuildAlternateRepresentations(unitExpr:str)->[str]:
        """
        Provides alternative representations by replacing units separated by '/' with their alternatives, resulting in as many alternatives as the square of the number of '/'.
        Used for testing for now. Contains deepcopy().
        Supports only suffixes.
        :param unitExpr:
        :return:
        """
        altCount:int = unitExpr.count("/")
        if(altCount == 0): return [unitExpr]
        osw:SegmentedWord = SegmentedWord.ParseUnitExpression(unitExpr)
        alts:[SegmentedWord] = [copy.deepcopy(osw)]

        #iterate
        sIndex:int = 0
        for suffix in osw.Suffixes:         #Suffixes supported only.
            segs = suffix.split("/")
            if(len(segs) > 1):
                altsclone = alts.copy()
                for s in range(0,len(segs)):
                    seg:str = segs[s]
                    #clone
                    for alt in altsclone:     #use copy so that not to stay in the append iterate loop forever.
                        new_sw = copy.deepcopy(alt)
                        alts.append(new_sw)
                        new_sw.Suffixes[sIndex] = seg
                        if(s==0): alts.remove(alt)    #since it is forked, remove itself (copied one) only in the first clone
            sIndex=sIndex+1

        if(alts.__len__() == 0):
            return [osw.BuildUnitExpression()]
        exprs:[str] = []
        for alt in alts:
            expr = alt.BuildUnitExpression()
            exprs.append(expr)
        return exprs

    def LowerCaseRoots(self, grammar:IGrammar):
        self.Root = grammar.ToLowerCase(self.Root)  # all lowercase assumption (Propers included)
        for orIndex, oroot in enumerate(self.OtherRoots):
            self.OtherRoots[orIndex] = grammar.ToLowerCase(oroot)
        for arIndex, aroot in enumerate(self.AlternativeRoots):
            self.AlternativeRoots[arIndex] = grammar.ToLowerCase(aroot)

    def __str__(self):
        if(not self.Root): return "N/A"
        return self.BuildUnitExpression() + " (" + str(type(self)) + ")"

    def __repr__(self):
        return self.__str__()
