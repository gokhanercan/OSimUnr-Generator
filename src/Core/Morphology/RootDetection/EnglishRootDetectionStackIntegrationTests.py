import unittest
from typing import Optional, List, Tuple, Dict, Set
from unittest import TestCase
from pandas import DataFrame
from tabulate import tabulate

from src.Core.Morphology.MorphoLex.MorphoLexSegmentedDataset import MorphoLexSegmentedDataset
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.EnglishRootDetectionStack import EnglishRootDetectionStack
from src.Core.Morphology.RootDetection.IRootDetectorStack import IRootDetectorStack
from src.Core.WordNet.NLTKWordNetWrapper import NLTKWordNetWrapper
from src.Tools import Resources, FormatHelper


class EnglishRootDetectionStackIntegrationTests(TestCase):

    def setUp(self):
        txtpath:str = Resources.GetOthersPath("MorphoLEX2.txt")
        morpholex:MorphoLexSegmentedDataset = MorphoLexSegmentedDataset.LoadFromText(txtpath,loadMetadatas=True,caseSensitive=False)
        inflectional = NLTKWordNetWrapper(wordSimPOSFilters=[POSTypes.NOUN])
        self.Stack:IRootDetectorStack = EnglishRootDetectionStack(inflectional,morpholex,yieldOutOfLexiconRoots=True)

    def test_DetectRootsInStack_CompoundWordMissingInDerivationalLexicon_DetectConstitiuentsAsRoots(self):
        cases = {}
        cases["psychosurgery"] = ["psycho","surgery"]
        cases["biochemist"] = ["bio","chemist","chem"] #requires _MinConstituentSize=3
        cases["bio"] = [None]
        cases["aeromechanics"] = ["aero","mechanic"]
        cases["psychophysics"] = ["psycho","physic"]
        cases["antilope"] = ["lope",None]     #the returned root should not be a prefix/suffix! I'm trying to test that 'anti' is not returned.
        cases["sentimentalisation"] = ["senti",None]
        cases["vitalisation"] = ["vital",None]
        cases["mylodontidae"] = ["mylodon",None]

        df = DataFrame()
        i = 1
        anyFail = False
        for k,val in cases.items():
            roots,reason,oolroots = self.Stack.DetectRootsInStack(k)     #two words both occur in the lexicon, but input does not exist in DerLexicon(morpholex)

            if(roots.__len__() >= 2):
                for r in roots:         #Since we now recursively parse constituents, we return more than 2 root candidates.
                    passed:bool = (r in val) or (r in val)        #The order of constituents does not matter.
                    if(passed): break
            else:
                if(None in val):        #Tests containing None, meaning we expect not to find a root.
                    passed = True       #If it couldn't split the word into two roots, the test should pass.
                else:
                    passed = False      #We are not testing negative scenarios yet.

            df.at[i,"Passed"] = "OK" if passed else "X"
            df.at[i,"Compound"] = k
            df.at[i,"Exp.Constitiuents"] = str(val)
            df.at[i,"Act.Constitiuents"] = str(roots)
            if not passed: anyFail = True
            i = i +1
        print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=FormatHelper._ThreeDigitFormat))
        if(anyFail): self.fail("some test(s) failed!")
        else:  self.assertTrue("All " + str(i) + " passed!")

    def test_DetectRootsInStack_RootScenarios(self):
        cases = {}  #surface,any matching root
        cases["animal"] = ["animal"]        #return surface itself if it is explicitly defined in morpholex. If MorphoLex does not return the match with itself, it unnecessarily falls into shallow suffixing.
        cases["gokhanercan"] = []       #There is no such root, it should return an empty list.
        cases["bohemianism"] = ["bohemia"]       #MorphoL root 'bohemia',  #boehme is the name of a person. It should be boehme+ian. It's not! ML has boheme but not boehme. This is an issue that can never be solved without a lexicon. A semantic relationship is needed between bohemia and boehme.
        cases["byzantine"] = ["byzant"]
        cases["byzantium"] = ["byzant"]
        cases["cabinetry"] = ["cabinet"]
        cases["candelabra"] = ["candela"]       #Added +BRA
        cases["candelabrum"] = ["candela"]      #Added +BRUM.
        cases["decriminalisation"] = ["crimin"]
        cases["graphic"] = ["graph"]
        cases["graphia"] = ["graph"]        #1L suffix test

        df = DataFrame()
        i = 1
        anyFail = False
        for k,expecteds in cases.items():
            roots,reason,oolroots = self.Stack.DetectRootsInStack(k)

            passed:bool = None
            if(expecteds.__len__() == 0):        #expected None cannot be returned!
                passed = roots.__len__() == 0      #If an empty list is expected, it passes with an empty list.
            else:
                passed = expecteds[0] in roots

            df.at[i,"Passed"] = "OK" if passed else "X"
            df.at[i,"Surface"] = k
            df.at[i,"Exp.Roots"] = str(expecteds)
            df.at[i,"Act.Roots"] = str(roots)
            if(reason): df.at[i,"Reason"] = reason
            if not passed : anyFail = True
            i = i +1

        print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=FormatHelper._ThreeDigitFormat))       #print first
        if(not anyFail): self.assertTrue("All " + str(i) + " passed!")
        else: self.fail("Some failed!")


if __name__ == "__main__":
    unittest.main()
    exit(0)

    #Stack Config.
    txtpath:str = Resources.GetOthersPath("MorphoLEX2.txt")
    morpholex:MorphoLexSegmentedDataset = MorphoLexSegmentedDataset.MorphoLexSegmentedDataset.LoadFromText(txtpath,loadMetadatas=True,caseSensitive=False)
    inflectional = NLTKWordNetWrapper(wordSimPOSFilters=[POSTypes.NOUN])
    stack:IRootDetectorStack = EnglishRootDetectionStack(inflectional,morpholex,yieldOutOfLexiconRoots=True)

    #test cases
    cases:Dict[str,Tuple[str,bool]]={}
    cases["cornet"] = "corn",None

    df = DataFrame()
    i:int=1
    for key,val in cases.items():
        surface = key
        expectedRoot = val[0]
        roots,reason,oolroots = stack.DetectRootsInStack(surface)

        passed = False
        if (expectedRoot in roots):
            passed = True
        else:
            passed = False

        df.at[i,"Passed"] = passed
        df.at[i,"Surface"] = surface
        df.at[i,"Expected Root"] = expectedRoot
        df.at[i,"Actual Roots"] = str(roots)
        df.at[i,"Reason"] = reason
        df.at[i,"OOLRoots"] = str(oolroots)
        i=i+1

    print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=FormatHelper._ThreeDigitFormat))