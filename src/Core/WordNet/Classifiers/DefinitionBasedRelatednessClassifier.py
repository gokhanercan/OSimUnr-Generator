from typing import Optional, Set

from src.Core.Segmentation.Tokenizers.ITokenizer import ITokenizer
from src.Core.Task.IWordRelatednessBinaryClassifier import IWordRelatednessBinaryClassifier
from src.Core.WordNet.WordPairDefinitionSourceFilter import WordPairDefinitionSourceFilter
from src.Core.WordPair import WordPair


class DefinitionBasedRelatednessClassifier(IWordRelatednessBinaryClassifier):
    """
    Performs definition-based relatedness approximation by accepting the match assumptions of WordPairDefinitionSourceFilter.
    """

    def __init__(self, filter:WordPairDefinitionSourceFilter,  tokenizer:ITokenizer, minRootLength:int=3, typeDepthRatio:float = 0.4) -> None:
        """
        :param filter:
        :param keywords:
        :param tokenizer:
        :param minRootLength:
        :param typeDepthRatio: This ratio indicates what percentage of concrete types in a sense's tree will be considered in the relatedness matching.
        """
        super().__init__()
        self.Filter = filter

        #D3 and D4
        self.Tokenizer = tokenizer
        self.SkipReferencing = False
        self.SkipKeywordInTypeHierarchy = False
        self.MinRootLength = minRootLength
        self.TypeDepthRatio:float = typeDepthRatio

        #D5
        self.SkipMutualMeaningfulAffixes = False
        #defaults: Not giving defaults here to avoid DRY violation. Values should be set by the agent.
        self.MeaningfulPrefixes = ()        #These values are normally expected to be provided externally, but we initialize them as a Tuple here at least to have them in the attribute schema.
        self.MeaningfulSuffixes = ()

    def IsRelated(self, word1: str, word2: str) -> Optional[bool]:
        wp = WordPair(word1,word2)

        #2
        if(not self.SkipKeywordInTypeHierarchy):
            try:
                match3,shared = self.Filter.ContainsKeywordInTypeHierarchy(wp,self.Tokenizer,self.MinRootLength,self.TypeDepthRatio)
                if(match3): return True, ("3A3:KwdInHier " + (str(shared) or "N/A"))
            except Exception as ex:
                print("3A3:Process stopped due to ERROR!" + str(wp))
                raise ex

        #3 - Performance Hazard (run last.) #Extremely slow. 99% of the slowness comes from here.
        if(not self.SkipReferencing):
            try:
                match2,shared = self.Filter.AreReferencingEachOtherInDefinitions(wp,self.Tokenizer,minRootLength=self.MinRootLength)
                if(match2): return True, ("3A4:Referencing "+ (str(shared) or "N/A") +"'")
            except Exception as ex:

                print(ex)
                print("3A4:Process stopped due to ERROR!" + str(wp))
                exit(0)

        #4 - MutualMeaningfullAffixes (Affixes like logy, graphy, which appear as affixes but are of FRG origin, are prevented from being simultaneously present in the word pair through orthographic control as they constantly produce the same meaning in compound words.)
        if(not self.SkipMutualMeaningfulAffixes):
            try:
                #Suffixes
                if word1.endswith(self.MeaningfulSuffixes) and word2.endswith(self.MeaningfulSuffixes):
                    return True, "3C3:MutualMeaningful-Suffix"

                #Prefixes
                if word1.startswith(self.MeaningfulPrefixes) and word2.startswith(self.MeaningfulPrefixes):
                    return True, "3C3:MutualMeaningful-Prefix"
            except Exception as ex:
                print(ex)
                print("3C3: Process stopped due to ERROR!" + str(wp))
                exit(0)

        return False,None