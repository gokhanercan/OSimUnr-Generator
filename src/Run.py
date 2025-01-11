import os
import sys

from src.Core import Generator
from src.Core.Generator import GenerateDataset, SetContext

from src.Core.Languages.LinguisticContext import LinguisticContext
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.OSimUnrPipeline.EnglishPipeline import EnglishPipeline
from src.Core.OSimUnrPipeline.PipelineProviderBase import PipelineProviderBase
from src.Core.Orthographic.NormalizedStringSimilarity.EditDistance import EditDistance
from src.Core.WordNet.NLTKWordNetWrapper import QueryLanguages

from src.Tools import Resources
from src.Tools.Logger import logp

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    englishPipeline: PipelineProviderBase = EnglishPipeline(LinguisticContext.BuildEnglishContext(), EditDistance())
    Generator.Provider =  englishPipeline
    print(englishPipeline)
    # exit()

    #Start the dataset generation with default values for English language using EditDistance ('edit') as orthographic similarity measure.
    # Resources.SetRootFolder("c:\Set your custom root resources folder here")  # Optional: Will be calculated automatically if not set.
    logp(f"Resources root: {Resources.GetResourcesRoot()}", True)
    logp("Starting dataset generation..",True)

    GenerateDataset(wordPosFilters=[POSTypes.NOUN],
                    minOrthographicSimQ3=0.50, minOrthographicSimQ4=0.75,
                    limitWordCands=500, maxRelatedness=0.25
                    )
    logp("Dataset generation completed.",True)

    #QueryLanguages()