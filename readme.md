# OSimUnr-Generator
## INTRODUCTION
This repository provides tools used to automatically generate new instances of **[OSimUnr dataset](https://github.com/gokhanercan/OSimUnr)** ([see the paper of the study](#cite)), which contains *orthographically similar but semantically unrelated* (OSimUnr) word-pairs.

Here are some word-pair examples from the [dataset repository](https://github.com/gokhanercan/OSimUnr):

| English                  | Turkish                   |
| :------------------------- | --------------------------- |
| processor - professor    | tencere - pencere         |
| adventure - denture      | tesbih - teşbih          |
| souffle - shuffle        | kiracılık - biracılık |
| fridge - fringe          | enişte - erişte         |
| internet - intercept     | kampanya - şampanya      |
| lockdown - lookdown      | avanta - lavanta          |
| undergrad - underground  | piyangocu - piyanocu      |
| margin - margarin        | bakara - makara           |
| shrine - shrink          | istifa - istifra          |
| dictionary - reactionary | kıyafet - kıyamet       |

The dataset construction pipeline leverages various morphological resources and orthographic algorithms such as python-string-similarity, NLTK, WordNet, and MorphoLex. These tools approximate orthographic similarity and semantic relatedness based on the assumptions explained in the paper.

This repository uses English as the default language, but the codebase is designed to be extensible to support additional languages. This repository does not include corpus, modeling, or evaluation components, as the focus is on the dataset generation.

## Core Components

- **Genuine OSimUnr Methods**: Includes methods from the study, such as the dataset generation pipeline, relatedness classifier, shallow affixation, semantic blacklisting, and root detectors.
- **Handles Pairing of Words**: Manages the associations and pairing of words.
- **General Utility Functions**: Comprises Logger, Progress, String manipulation, and other utilities.
- **General NLP Functions**: Covers essential NLP functionalities like Dataset, Language, POS (Part of Speech), Tokenizer, and Preprocessor.
- **Subword Level Representations**: Features components like Ngram, Root, SegmentedWord, and Affixes for detailed linguistic analysis.
- **Orthographic Similarity Tools**: Tools to compute various edit distances and overlapping coefficients for assessing text similarity.
- **MorphoLex Shallow Parser**: A specialized parser for morphological analysis.
- **WordNet Wrapper**: Used as a relatedness approximation tool; includes Word-pool, Semantic graph, and root detector.
- **Supports Building Your Own Language-Specific Pipeline**: Encourages the development of customized language pipelines, as detailed in `PipelineProviderBase`.

## Compatibility

The code has been tested on the following environments:

- **Python 3,6, 3.8**, Windows, Ubuntu. See Github Actions for tests running on Ubuntu.

### Important Note

- **NLTK Version**: To ensure reproducibility in the English language processing pipeline, please use the exact 3.4.5 version of NLTK. This version is compatible with Python versions 2.7 through 3.8.
- **Python 3.8+**: Not supported due to NLTK compatibility issues. If you do not require the exact WordNet implementation, feel free to fork and test in higher Python versions. In theory, it should work.

## INSTALLATION

1. Clone the repository to a folder:
2. Install required dependencies in the root of the project:

   ```bash
   pip install pip-tools
   ```

   ```bash
   pip install -r requirements.txt
   ```
3. Run the [`setup.py`](setup.py) script to download WordNet data in your local:

   ```bash
   python setup.py
   ```
4. (Optional) Add project path to PythonPath to enable importing modules from any location:

   ```bash
   $env:PYTHONPATH = "YourClonePath"
   ```

## How to Run

### Generate an English Dataset using defaults

1. Navigate to the root directory of the cloned source-code.
2. Configure the pipeline for your study if you want to. The default is the English pipeline described in the paper.
3. Start the pipeline by running:

   ```bash
   python src\Run.py
   ```
4. You should see an output similar to the one given in the Output section below:
5. The generated dataset files should be located in the '../Resources/Studies/MyStudy/eng' directory relative to your source code.

   For example, for the final Q3 dataset for English, check out the file named *'S3a-OrthographicallySimilarButUnrelatedsQ3-nedit-{RandomDatasetID}.csv'*. The overall naming pattern is as follows:
   ```S{StageNumber}-SubDatasetNameQ{SimilarityLevel}-{OrthographicAlg}-{RandomDatasetID}.csv ```

   This is very similar to the naming conventions of the [released OSimUnr dataset.](https://github.com/gokhanercan/OSimUnr)

**Output:**
```bash
C:\Users\gokhan\AppData\Local\Programs\Python\Python36\python.exe L:\Projects\OSimUnr-Generator\src\Run.py 
20:43:10: Building common context for the study...
20:43:10: Common context executed!
<src.Core.OSimUnrPipeline.EnglishPipeline.EnglishPipeline object at 0x00000149A9C66F60>
20:43:10: Resources root: L:\Projects\OSimUnr-Generator\Resources
20:43:10: Starting dataset generation..
Debugger is not attached. _Debug=False
20:43:15: Starting Stage2...
20:43:15: oSimAlg: nedit
20:43:15: iter-a: 12/125000 (0.01%)
20:43:15: Remaining: 0:00:03.251675
...
..
20:43:19: iter-w: 124740/125000 (99.79%)
20:43:19: Remaining: 0:00:00.009201
totalSpace: 124750
20:43:19: Saving dataset or dataset snapshot named: S2-OrthographicallySimilarsQ3-nedit ...
20:43:19: Saved snapshot: L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S2-OrthographicallySimilarsQ3-nedit-ZTXQX.csv(411)
20:43:19: Saving dataset or dataset snapshot named: S2-OrthographicallySimilarsQ4-nedit ...
20:43:19: Saved snapshot: L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S2-OrthographicallySimilarsQ4-nedit-ZTXQX.csv(2)
20:43:19: S3: Starting Stage3 Relatedness Filtering...
20:43:19: WordNetSim Type: <src.Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapper object at 0x00000149AEEE0630>
20:43:19: S3: Calculating WordNet relatedness values for WordPairs...
20:43:19: S3: Loading
20:43:19: Loading wordpair dataset into memory...L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S2-OrthographicallySimilarsQ4-nedit-ZTXQX.csv
20:43:19: Loaded wordpairs from path: L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S2-OrthographicallySimilarsQ4-nedit-ZTXQX.csv (2 items)
20:43:19: Loading wordpair dataset into memory...L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S2-OrthographicallySimilarsQ3-nedit-ZTXQX.csv
20:43:19: Loaded wordpairs from path: L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S2-OrthographicallySimilarsQ3-nedit-ZTXQX.csv (411 items)
20:43:19: Setting WordNet similarities for L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S2-OrthographicallySimilarsQ4-nedit-ZTXQX.csv ...
20:43:19: WordSimilarityNormalizerWrapper.Eagerly normalizing 2 wordpairs ...
20:43:19: wordpair: 0/2 (0.0%)

20:43:25: WordSimilarityNormalizerWrapperNormalization completed!
20:43:25: Saving dataset or dataset snapshot named: S3-OrthographicallySimilarsWithWNQ4-nedit ...
20:43:25: Saved snapshot: L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S3-OrthographicallySimilarsWithWNQ4-nedit-ZTXQX.csv(2)
20:43:25: Setting WordNet similarities for L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S2-OrthographicallySimilarsQ3-nedit-ZTXQX.csv ...
20:43:25: WordSimilarityNormalizerWrapper.Eagerly normalizing 411 wordpairs ...
20:43:25: wordpair: 0/411 (0.0%)
20:43:25: wordpair: 4/411 (0.97%)
...
..
20:43:25: wordpair: 408/411 (99.27%)
20:43:25: Remaining: 0:00:00.000803
20:43:25: WordSimilarityNormalizerWrapperNormalization completed!
20:43:25: Saving dataset or dataset snapshot named: S3-OrthographicallySimilarsWithWNQ3-nedit ...
20:43:25: Saved snapshot: L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S3-OrthographicallySimilarsWithWNQ3-nedit-ZTXQX.csv(411)
20:43:25: Loading wordpair dataset into memory...L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S3-OrthographicallySimilarsWithWNQ3-nedit-ZTXQX.csv
20:43:25: Loaded wordpairs from path: L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S3-OrthographicallySimilarsWithWNQ3-nedit-ZTXQX.csv (411 items)
20:43:25: Initializing root detection dependencies...
20:43:25: Loading metadatas too...
20:43:25: Dataset loaded from flat text(s).
20:43:25: Loading metadatas too...
20:43:25: Dataset loaded from flat text(s).
20:43:25: Initializing definition-based filtering dependencies...
20:43:25: detectUnrelateds...
20:43:25: S3a Relatedness Filtering is about to begin for L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S3-OrthographicallySimilarsWithWNQ4-nedit-ZTXQX.csv ...
20:43:25: wp: 0/2 (0.0%)
20:43:25: Saving dataset or dataset snapshot named: S3a-OrthographicallySimilarAndSharingRootsQ4-nedit ...
20:43:25: Saved snapshot: L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S3a-OrthographicallySimilarAndSharingRootsQ4-nedit-ZTXQX.csv(2)
20:43:25: Relatedness filtering ended.
20:43:25: detectUnrelateds...
20:43:25: S3a Relatedness Filtering is about to begin for L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S3-OrthographicallySimilarsWithWNQ3-nedit-ZTXQX.csv ...
20:43:25: wp: 0/411 (0.0%)
20:43:25: wp: 4/411 (0.97%)
20:43:25: Remaining: 0:00:00.006840
20:43:25: wp: 8/411 (1.95%)
...
..
20:43:25: Remaining: 0:00:00.000055
20:43:25: wp: 408/411 (99.27%)
20:43:25: Remaining: 0:00:00.000023
20:43:25: Saving dataset or dataset snapshot named: S3a-OrthographicallySimilarButUnrelatedsQ3-nedit ...
20:43:25: Saved snapshot: L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S3a-OrthographicallySimilarButUnrelatedsQ3-nedit-ZTXQX.csv(8)
20:43:25: Saving dataset or dataset snapshot named: S3a-OrthographicallySimilarAndSharingRootsQ3-nedit ...
20:43:25: Saved snapshot: L:\Projects\OSimUnr-Generator\Resources\Studies\MyStudy\eng\S3a-OrthographicallySimilarAndSharingRootsQ3-nedit-ZTXQX.csv(403)
20:43:25: Relatedness filtering ended.
20:43:25: MyStudy S3a process completed.
20:43:25: Process completed for MyStudy
20:43:25: Dataset generation completed.

Process finished with exit code 0
```

## CUSTOMIZATION

You can customize and extend the pipeline based on your needs as follows:

### Set the Initial Parameters and Algorithms

In the [`Run.py`](src/Run.py) file, you can set various parameters:

```python
GenerateDataset(wordPosFilters=[POSTypes.NOUN],minOrthographicSimQ3=0.50, minOrthographicSimQ4=0.75,maxRelatedness=0.25,limitWordCands=500)
```

### Parameters
> **wordPosFilters**: Defines the part-of-speech (POS) tags that the word-pool should use. Default is [POSTypes.NOUN](/src/Core/Morphology/POSTypes.py).

> **minOrthographicSimQ3**: Defines the lower limit of the Q3 orthographic space. The upper limit is *minOrthographicSimQ4*. Default is 0.50.

> **minOrthographicSimQ4**: Defines the lower limit of the Q4 orthographic space. The upper limit is 1 by default. Default is 0.75.

> **maxRelatedness**: Sets the threshold that defines the maximum level of 'unrelatedness' of word pairs on a scale of 0 to 1. Default is 0.25.

> **limitWordCands**: Limits the size of the word-pool. If set, it limits the word-pool by randomly picking words form the [`IWordSource`](src/Core/IWordSource.py). Default is None. This is useful for local pre-experimentation. Keep in mind that word pairing is quadratic, and dataset generation may take weeks to complete.

Please use parameters *resume*, *resumeStage3and4*, *wordpoolPath*, *wordpairsPath*, *s1Only* if you want to use the Save/Restore/Resume stages of the pipeline functionality. It is very useful for very long-running generations that take days.


### Change Providers and Settings

The [`Generator.py`](src/Core/Generator.py) implementation utilizes an abstract provider model called [`PipelineProviderBase`](/src/Core/OSimUnrPipeline/PipelineProviderBase.py) to create concrete resources, data entries, and implementations.
The default provider is set as [`EnglishPipelineProvider`](/src/Core/OSimUnrPipeline/EnglishPipeline.py), configured as follows:
```python
englishPipeline: PipelineProviderBase = EnglishPipeline(LinguisticContext.BuildEnglishContext(), EditDistance())
```

If you wish to modify the orthographic similarity, for instance, please provide any Python implementation of [`IWordSimilarity`](/src/Core/WordSim/IWordSimilarity.py) and inject it into the provider.
Below is a list of factory methods expected from a concrete provider, organized into three groups:

**A. Morphological Resources**
```python
> CreateRootDetector()
> CreateFastRootDetector()
> CreateMorphoLex()
> CreateTokenizer()
```

**B. Semantic Resources**
```python
> CreateWordNet()
> CreateWordSource()
> CreateWordSimilarityAlgorithm()
```

**C. Semantic Definitions:** Manually defined list of WordNet concept mappings.
```python
> CreateBlacklistedConceptsFilterer()
> CreateConceptPairFilterer()
> CreateDefinitionBasedRelatednessClassifier()
> CreateDerivationallyRelatedClassifier()
```

If you check out [`EnglishPipeline.py`](/src/Core/OSimUnrPipeline/EnglishPipeline.py), you'll see a list of manual definitions and mappings introduced to reduce the false positive rates in the final dataset. 

As an example, here is the list of blacklisted concepts (synset names) from English WordNet used in `CreateBlacklistedConceptsFilterer`:

```bash
- ill_health.n.01
- disorder.n.01
- pathologic_process.n.01
- plant_part.n.01
- biological_group.n.01
- medical_procedure.n.01
- animal.n.01
- microorganism.n.01
- plant.n.02
- chemical.n.01
- drug.n.01
- body_substance.n.01
- vasoconstrictor.n.01
- symptom.n.01
```


### Adding a New Language
To add a new language, along with the morphological and semantic provider types required for your language, you need to modify the [`LinguisticContext`](src/Core/Languages/LinguisticContext.py) type specifically for your language code. If the grammar ([`IGrammar`](src/Core/Languages/Grammars/IGrammar.py)) of the language is generic enough, considering aspects such as the alphabet, casing, and accents, you may reuse the [`InvariantGrammar`](src/Core/Languages/Grammars/InvariantGrammar.py) instance. However, if the language has distinct characteristics, please refer to our Turkish implementation [`TRGrammar`](src/Core/Languages/Grammars/TRGrammar.py) as a model.

Below is the list of languages supported by WordNet version 3.4.5, which includes 29 languages:
```bash
['eng', 'als', 'arb', 'bul', 'cat', 'cmn', 'dan', 'ell', 'eus', 'fas', 'fin', 'fra', 'glg', 'heb', 'hrv', 'ind', 'ita', 'jpn', 'nld', 'nno', 'nob', 'pol', 'por', 'qcn', 'slv', 'spa', 'swe', 'tha', 'zsm']
```

You can retrieve this list by running the following code:

```bash
from src.Core.WordNet.NLTKWordNetWrapper import QueryLanguages
QueryLanguages()
```
Note that Turkish is not included in this list. For generating [OSimUnr](https://github.com/gokhanercan/OSimUnr), we utilized our study group's open-source [Java WordNet library](https://github.com/olcaytaner/TurkishWordNet), which adheres to the same [`IWordNet`](src/Core/WordNet/IWordNet.py) and `IWordNetMeasure` interfaces.

## DEPENDENCIES
This project relies on minimal dependencies (see [`requirements.txt`](src/Core/requirements.txt) for details). The main dependencies are:

- **NLTK**: Ensure version 3.4.5 is used. This study heavily relies on NLTK's WordNet and other resources. Changing the NLTK version may cause some semantic or morphological assumption and tests to break.
- **Pandas**: Ensure the compatible version is installed (fixed in [`requirements.txt`](src/Core/requirements.txt)).

### Notes

- **EditDistance and Overlapping Coefficients**: Some implementations are adapted from the https://github.com/gokhanercan/python-string-similarity package.
- **Cython, Java and C++ Code**: These components are excluded from this repository due to their deployment and configuration complexity.

## RUNNING TESTS

If you want to verify the installation or have made changes to the code, you can execute the unit tests as follows:

1. Execute the test suite:
   ```bash
   python test\UnitTestsRunner.py
   ```
2. Check whether the "TESTS PASSED" as shown below:

Output:

See an example of unit test output [here.](unittests.md)

## CONTRIBUTE AND SUPPORT

Feel free to open issues or pull requests to suggest improvements or report bugs. If you have read the paper and are looking for specific implementations, such as a C++ implementation of FastText models and n-gramming, resources for Turkish morphology, or Cython-optimized versions of the tools, please contact.

Before submitting a pull request, please ensure that all tests have been run and passed.

### Cite

The paper for this work is currently under peer review. Citation details will be provided here once available.
