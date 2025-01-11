import unittest
from textwrap import TextWrapper
from typing import Set, List
from unittest import TestCase

from pandas import DataFrame
from tabulate import tabulate

from src.Core.Morphology.MorphoLex.MorphoLexSegmentedDataset import MorphoLexSegmentedDataset
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.EnglishRootDetectionStack import EnglishRootDetectionStack
from src.Core.Morphology.RootDetection.IRootDetector import IRootDetector
from src.Core.Morphology.RootDetection.IRootDetectorStack import IRootDetectorStack
from src.Core.WordNet.NLTKWordNetWrapper import NLTKWordNetWrapper
from src.Core.WordPair import WordPair
from src.Tools import Resources, FormatHelper


class SharingRootDetector(object):
    """
    Decides whether two words share a root using IRootDetector.
    """

    def __init__(self, rootDetector:IRootDetector, useOutOfLexiconRoots:bool = False) -> None:
        """
        :param rootDetector: Supports IRootDetector or IRootDetectorStack.
        :param useOutOfLexiconRoots: This is actually an application outside the standard RootDetector. Types like EnglishRootDetectionStack can return oolRoots, used to utilize it.
        """
        super().__init__()
        self.RootDetector:IRootDetector = rootDetector
        self.UseOutOfLexiconRoots:bool = useOutOfLexiconRoots

    def IsSharingRoot(self, wp: WordPair, priorPOS:POSTypes = None) -> [bool, List[str], str]:
        """
        :param wp:
        :param priorPOS:
        :return:isSharing, SharedRoots, detectors
        """
        effRoots1:Set[str] = None
        effRoots2:Set[str] = None
        detector1=detector2 = ""

        if(isinstance(self.RootDetector,IRootDetectorStack) or str(self.RootDetector).__contains__("RootDetectionStack") or str(self.RootDetector).__contains__("RootDetectorStack") ): #Hack: I disabled type check because cython interface could not be implemented.
            #region Stack
            stack:IRootDetectorStack = self.RootDetector
            roots1,d1,oolRoots1 = stack.DetectRootsInStack(wp.Word1,priorPOS)
            roots2,d2,oolRoots2 = stack.DetectRootsInStack(wp.Word2,priorPOS)
            detector1 = d1
            detector2 = d2
            if(self.UseOutOfLexiconRoots):
                effRoots1 = roots1.union(oolRoots1)
                effRoots2 = roots2.union(oolRoots2)
            else:
                effRoots1 = roots1
                effRoots2 = roots2
            #endregion
        else:
            #with regular detector
            effRoots1 = set(self.RootDetector.DetectRoots(wp.Word1,priorPOS))
            effRoots2 = set(self.RootDetector.DetectRoots(wp.Word2,priorPOS))

        #Add Surfaces for Possible Surface<->Root Matches
        effRoots1.add(wp.Word1)
        effRoots2.add(wp.Word2)
        
        #Intersection logic
        intersection = effRoots1.intersection(effRoots2)
        if (len(intersection) > 0):
            return True, list(intersection)[0],"w1:" + detector1 + "\t w2:" + detector2  # we only return the first common element.
        return False, None, ""
        #endregion

class SharingRootDetectorIntegrationTest(TestCase):     #Integration path.

    def setUp(self, outOfLexiconRootsAllowed:bool = True):      #I run the tests allowing OOLs
        #English
        txtpath:str = Resources.GetOthersPath("MorphoLEX2.txt")
        morpholex:MorphoLexSegmentedDataset = MorphoLexSegmentedDataset.LoadFromText(txtpath,loadMetadatas=True,caseSensitive=False)
        inflectional = NLTKWordNetWrapper(wordSimPOSFilters=[POSTypes.NOUN])
        self.Stack:IRootDetectorStack = EnglishRootDetectionStack(inflectional,morpholex,yieldOutOfLexiconRoots=outOfLexiconRootsAllowed)
        self.Target = SharingRootDetector(self.Stack,useOutOfLexiconRoots=outOfLexiconRootsAllowed)

    def test_EN_IsSharingRoot_SharedRootScenarios(self):
        cases = []

        # region Successful cases
        cases.append(["academic","academicianship",True])
        cases.append(["cardiologist","cardiology",True])        #Not in MorphoLex.
        cases.append(["romanticisation","romanticist",True])        #ISATION added.
        cases.append(["angiologist","angiology",True])      #No 'angio' root. Without root, suffixes do not work. There is no 'angio' in WN. There are many surfaces. Not in MorphoLex. If I add 'Angio' root, it works.
        cases.append(["animal","animalisation",True])
        cases.append(["biochemist","biochemistry",True])        #barely passes the 3-word compound limit.
        cases.append(["biophysicist","biophysics",True])
        cases.append(["biofeedback","feedback",True])
        cases.append(["aeromechanics","mechanic",True])
        cases.append(["psychophysics","physic",True])
        cases.append(["buddhism","buddhist",True])      #I corrected the wrong decomposition of morpholex in my version!
        cases.append(["boehme","bohemianism",True])      #NSIM added but didn't work. boehme is a person's name and should semantically match the concept! Therefore, I corrected the decomposition of bohemian: {(boheme)>ia>}>n>       #The separation of boheme root and boehme roots is problematic. They should actually be synonyms. There should be 2 decompositions for these words.
        cases.append(["arthrogram","arthrography",True])        #added root. +GRAPHY added.
        cases.append(["verbena","verbenaceae",True])        #CEAE added.
        cases.append(["valerian","valerianaceae",True])     #ACEAE added.
        cases.append(["ureter","ureterocele",True])         #+OCELE
        cases.append(["omphalocele","omphalos",True])       #OS suffix already exists, + OCELE makes it ok.
        cases.append(["sentimentalisation","sentimentalist",True])
        cases.append(["sigmoidoscope","sigmoidoscopy",True])
        cases.append(["sigmoidectomy","sigmoidoscopy",True])    #+OSCOPE #OSCOPY saved it.
        cases.append(["keynes","keynesianism",True])            #2 levels would solve it. + ianism solved it.
        cases.append(["archeologist","archeology",True])
        cases.append(["arboriculture","arboriculturist",True])     #shallow suffixes solve it half by chance.
        cases.append(["arthrogram","arthrography",True])
        cases.append(["trauma","traumatology",True])            #TOLOGY added.
        cases.append(["tracheid","tracheitis",True])
        cases.append(["sclerite","scleritis",True])
        cases.append(["schistosome","schistosomiasis",True])        #+IASIS
        cases.append(["zigadene","zigadenus",True])
        cases.append(["amygdala","amygdaloid",True])      #OID solved it.
        cases.append(["aclant","saclant",False])         #two proper names, no derivational relationship. Therefore, no SharedRoot but they refer to each other in their definitions! The largest stack should catch this wp.
        cases.append(["immunofluorescence","autofluorescence",True])        #added immuno root.
        cases.append(["anglican","anglia",True])       #added expr in ML: 'anglia' root: anglo
        cases.append(["onomasticon","onomastics",True])     #added as root in ML.
        #endregion

        #region Fixed OutOfLexiconCases
        cases.append(["presidio","presidium",True])     #since the root 'preside' was entered, it was not finding the missing presidi root. OOLRoots ensured it returns presidi.
        cases.append(["arthroscope","arthroscopy",True])       #no root.
        cases.append(["blennioid","blennioidea",True])      #no blennio in lexicon, blennioid and blennioidea exist. Our algorithm does not solve this. Solved. 'blennio' common dynamic root.
        cases.append(["anesthesia","anesthesiology",True])        #ISATION added.     #no anesthesi root. OLOGY dynamically created anesthesi.
        cases.append(["anesthesiologist","anesthesiology",True])    #same as above case.
        cases.append(["acanthopterygian","acanthopterygii",True])       #a type of fish, a fish. IAN solved it.
        cases.append(["autogenics","autogeny",True])       #dynamically found autogen root.
        cases.append(["haematologist","haematology",True])
        cases.append(["haemoglobin","haemoglobinemia",True])
        cases.append(["acanthocyte","acanthocytosis",True])     #+cytosis
        cases.append(["thrombocyte","thrombocytopenia",True])     #+cytopenia
        cases.append(["megapodiidae","megapode",True])      #bird.
        cases.append(["megathere","megatheriidae",True])      #extinct sloth
        cases.append(["mycoplasma","mycoplasmataceae",True])   #bacteria
        cases.append(["mylodon","mylodontidae",True])   #extinct animal, bear, iguanodontidae also exists.
        cases.append(["aerophilately","aerophile",True])        #related to aviation, solved with +PHILE suffix.
        cases.append(["aesthete","aesthetic",True])        #same root, one is a person, the other is a philosophy.   #ML incorrect, solved with ML2.
        cases.append(["amygdala","amygdalotomy",True])     #same root. a turned into o. solved with +OTOMY. A suffix was already separated.
        cases.append(["anesthesia","anesthesiologist",True])        #same root. added +OLOGIST.
        cases.append(["biochemistry","immunohistochemistry",True])       #nothing in lexicon. added to lexicon: 'immunohistochemistry	(immun){(histo)(chemistry)}'
        cases.append(["birdnest","birdnesting",True])                   #added to ML: birdnest	{(bird)}{(nest)}        compound word has no place. very difficult without adding root, nest cannot be added.
        cases.append(["bishopry","bishopric",True])                     #corrected in ML: bishopric	{(bishop)}>ic>      added +RY.
        cases.append(["bowdleriser","bowdlerism",True])                 #added +IZE allomorph ISE and ISER. existed in ML as bowdlerizer but not as bowdleriser.
        cases.append(["byzant","byzantinism",True])
        cases.append(["byzant","byzantium",True])                       #added byzant root.
        cases.append(["consuetude","consuetudinal",True])       #no word in ML. only comes from WN. added 3 entries.
        cases.append(["consuetude","consuetudinary",True])       #'
        cases.append(["criminal","criminalization",True])       #added +IZATION suffix. ISATION already existed. Allomorph not supported.
        cases.append(["criminal","decriminalisation",True])       #added 4 expr to ML. very difficult to solve without a recursive analyzer.
        cases.append(["cytogeny","cytogenetics",True])
        cases.append(["harlotry","harlot",True])
        cases.append(["mammogram","mammography",True])          #mammo
        cases.append(["rollerblading","rollerblader",True])          #no root. compounding creates rollerblade but sound drop ends it. added 2 expr.
        cases.append(["thermal","thermalgesia",True])        #added gesia root to use compounding.
        cases.append(["cyberwar","cyberart",True])          #added cyber root.
        cases.append(["hematology","haematology",True])     #added 3 surfaces.
        cases.append(["haematologist","hematology",True])     #
        cases.append(["encyclopedism","encyclopaedism",True])     #added surfaces.
        cases.append(["cyclopedia","cyclopaedia",True])
        cases.append(["cyclopedia","encyclopaedism",True])
        #endregion

        #region Negative Cases
        cases.append(["vitalisation","sentimentalisation",False])
        #endregion

        df = DataFrame()
        anyFail = False
        textWrapper = TextWrapper(width=70)

        #EN Cases
        enCount,enAnyFail = self._ExecuteCases(cases,df,textWrapper)

        trAnyFail = False
        trCount = 0
        #endregion

        #Results
        print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=FormatHelper._ThreeDigitFormat))
        anyFail = enAnyFail or trAnyFail
        if(not anyFail):
            msg = "All " + str(enCount+trCount) + " passed!"
            print(msg)
            self.assertTrue(msg)
        else:
            self.fail("some are failed!")

    def _ExecuteCases(self, cases, df, textWrapper)->[int,bool]:
        i:int = 1
        anyFail = False
        for case in cases:
            wp = WordPair(case[0], case[1])
            shared,sharedRoot,reason = self.Target.IsSharingRoot(wp)
            passed:bool = (shared == case[2])
            df.at[i,"Passed"] = "OK" if passed else "X"
            df.at[i,"Word1"] = case[0]
            df.at[i,"Word2"] = case[1]
            df.at[i,"SharedRoot"] = sharedRoot if passed else ""
            df.at[i,"Expected"] = case[2]
            df.at[i,"Actual"] = shared
            df.at[i,"Reason"] = "\n".join(textWrapper.wrap(reason)) if passed else ""
            df.at[i,"Roots1 + detector + OOLRoots"] = "\n".join(textWrapper.wrap(str(self.Stack.DetectRootsInStack(case[0],None))))        #Here we call again from outside for tracing.
            df.at[i,"Roots2 + detector + OOLRoots"] = "\n".join(textWrapper.wrap(str(self.Stack.DetectRootsInStack(case[1],None))))        #Here we call again from outside for tracing.
            if not passed: anyFail = True
            i = i +1
        return i,anyFail

if __name__ == "__main__":
    unittest.main()