# coding=utf-8
from typing import Optional, List, Tuple, Dict, Set

from src.Core.Morphology.MorphoLex.MorphoLexSegmentedDataset import MorphoLexSegmentedDataset
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.IRootDetector import IRootDetector
from src.Core.Morphology.RootDetection.IRootDetectorStack import IRootDetectorStack


class EnglishRootDetectionStack(IRootDetectorStack):
    """
    A hybrid root detector utilizing all linguistic and trained prior knowledge at hand.
    """
    def __init__(self, wordnetWrapper, morpholex: MorphoLexSegmentedDataset, lexiconPosFilter: POSTypes = None, yieldOutOfLexiconRoots: bool = False) -> None:
        """
        :param wordnetWrapper:
        :param morpholex:
        :param lexiconPosFilter:
        :param yieldOutOfLexiconRoots: Roots generated as a result of Shallow Affixation are returned as secondary OOLRoots.
        Even if they are not in any lexicon, a root like 'anesthesi' can be returned due to 'anesthesiology.' Disabled by default.
        """
        IRootDetector.__init__(self)
        self.WordNet = wordnetWrapper
        self.MorphoLex: MorphoLexSegmentedDataset = morpholex
        self.LexiconPosFilter = lexiconPosFilter
        self._Lexicon: Set[str] = None
        self._MinConstituentSize = 3  # Minimum length for constituents forming a compound. For example, the word 'bio' can form a compound like 'biochemist.'
        self._MinEmergingLexemeSize = 5  # In OOLexicon cases, dynamically generated lexicon defaults to a minimum of this many characters.
        self.YieldOutOfLexiconRoots: bool = yieldOutOfLexiconRoots

    def _GetLexicon(self):
        if self._Lexicon is None:
            morphlexRootsLexicon: Set[str] = self.MorphoLex.Roots  # MorphoLex surfaces can also be added.
            morpholexSurfacesLexicon: Set[str] = set(self.MorphoLex.Segmentations.keys())
            wordnetLexicon = self.WordNet.GetWords(self.LexiconPosFilter)
            finalLexicon: Set[str] = morphlexRootsLexicon.union(morpholexSurfacesLexicon, wordnetLexicon)
            self._Lexicon = finalLexicon
        return self._Lexicon

    def DetectRootsInStack(self, surface: str, priorPOS1: POSTypes = None) -> Tuple[Set[str], str, Set[str]]:
        """
        IDEAS:
        1) Mofressor roots larger than a certain length can be used.
        2) After eliminating inflections from Morphy, derivational forms can be considered.
        3) By systematically removing prefixes and suffixes, we can check if we find the root.
        :param surface:
        :param priorPOS:
        :return:
        """
        finalRoots: Set[str] = set()
        detector: str = ""
        oolRoots: Set[str] = set()

        # 1. DerivationDataset
        roots = set(self.MorphoLex.DetectRoots(surface))  # Even if MorphoLex returns a result, we still check below. If the input itself is returned, we trust it. Leaving it below may incorrectly parse 'animal' as 'anim+al'!
        if roots:
            finalRoots = roots  # Even if we find the root, we try checking alternative roots. MorphoLex could be wrong.
            detector = "MorphoLex"
            f, d, ool = self._ShallowDetect(surface, priorPOS1)
            # Return by adding. Intentionally not returning OOLs because MorphoLex might have valid insights!
            finalRoots = finalRoots | f  # Adding shallow findings to ML findings.
            detector += "+" + d
        else:
            f, d, ool = self._ShallowDetect(surface, priorPOS1)
            finalRoots = f
            detector = d
            oolRoots = ool

        if not finalRoots:
            finalRoots = set()
        return finalRoots, detector, oolRoots

    def _ShallowDetect(self, surface: str, priorPOS1: POSTypes = None):
        """
        A stack for detecting roots using superficial methods (not deep, no morphological rules applied).
        Does not include MorphoLex.
        :param surface:
        :param priorPOS1:
        :return:
        """
        finalRoots: Set[str] = set()
        detector: str = ""
        oolRoots: Set[str] = set()

        # 2. OneLayerInflectionFirst
        roots = set(self.WordNet.DetectRoots(surface))  # Uses Morphy to return low-success roots based solely on inflections.
        if surface in roots:
            roots.remove(surface)  # Exclude the surface itself.
        for root in roots:
            roots = set(self.MorphoLex.DetectRoots(root))
            finalRoots = roots
            detector = "Morphy"
            return finalRoots, detector, oolRoots

        # 3. OneLevelPrefixRemoval
        lexicon = self._GetLexicon()
        for prefix in self.MorphoLex.MetaPrefixes:
            pre = prefix.lower()
            if not surface.startswith(pre):
                continue
            mutated: str = surface[len(pre):]
            if len(mutated) < self._MinConstituentSize:
                continue
            if mutated in lexicon:
                finalRoots.add(mutated)
                roots = set(self.MorphoLex.DetectRoots(mutated))  # Extract roots of the new surface again.
                finalRoots = finalRoots.union(roots)
                detector += "+1LPrefix"
            elif self.YieldOutOfLexiconRoots and len(mutated) >= self._MinEmergingLexemeSize:  # Could using this for prefixes cause harm?
                oolRoots.add(mutated)

        # 4. OneLevelSuffixRemoval
        for suffix in self.MorphoLex.MetaSuffixes:
            suf = suffix.lower()
            if not surface.endswith(suf):
                continue
            mutated: str = surface[:len(surface) - len(suf)]
            if len(mutated) < self._MinConstituentSize:
                continue
            if mutated in lexicon:
                finalRoots.add(mutated)
                roots = set(self.MorphoLex.DetectRoots(mutated))
                finalRoots = finalRoots.union(roots)
                detector += "+1LSuffix"
            elif self.YieldOutOfLexiconRoots and len(mutated) >= self._MinEmergingLexemeSize:  # Should suffix length limit be enforced as a last resort?
                oolRoots.add(mutated)

        # 5. SimpleAutoCompounding
        constituent_cands = set()
        for w in lexicon:
            w = w.lower()
            if len(w) < self._MinConstituentSize:
                continue  # assumption!
            if w == surface:
                continue
            if surface.endswith(w) or surface.startswith(w):
                wAffix: str = w.upper()
                if wAffix not in self.MorphoLex.MetaPrefixes and wAffix not in self.MorphoLex.MetaSuffixes:
                    constituent_cands.add(w)

        # Compose possible compounds
        constituents: Set[str] = set()
        for c1 in constituent_cands:  # Can be optimized slightly!
            for c2 in constituent_cands:
                compound = c1 + c2
                if compound == surface:  # We built the surface from roots
                    constituents.add(c1)
                    constituents.add(c2)
        if constituents:
            detector += "+1LCompounding"
            finalRoots.update(constituents)

            # Parse Constituents Recursively
            for c in constituents:  # Increases complexity! Example: "physic psychophysics"
                croots, cdetectors, coolRoots = self.DetectRootsInStack(c, None)
                for croot in croots:
                    if croot not in finalRoots and len(croot) >= self._MinConstituentSize:
                        finalRoots.add(croot)
                        detector += f" -rec[{cdetectors}]"

        if not finalRoots:
            finalRoots = set()
        return finalRoots, detector, oolRoots
