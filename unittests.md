```
C:\Users\gokhan\AppData\Local\Programs\Python\Python36\python.exe
L:\Projects\OSimUnr-Generator\test\UnitTestsRunner.py 
Current Directory: L:\Projects\OSimUnr-Generator\test
Source Directory:  L:\Projects\OSimUnr-Generator\src

SkipIntegrations: True
FailFast: False

13:29:25: Building common context for the study...
13:29:25: Common context executed!
13:29:25: Building common context for the study...
13:29:25: Common context executed!


Debugger is not attached. _Debug=False
test_IsNormalized_0_10_Normalized (Core.Dataset.DiscreteScale.DiscreteScaleTest) ... ok
test_IsNormalized_BothInf_False (Core.Dataset.DiscreteScale.DiscreteScaleTest) ... ok
test_IsNormalized_Min0MaxInf_False (Core.Dataset.DiscreteScale.DiscreteScaleTest) ... ok
test_IsNormalized_MinInfMax10_False (Core.Dataset.DiscreteScale.DiscreteScaleTest) ... ok
test_str_Normalized (Core.Dataset.DiscreteScale.DiscreteScaleTest) ... ok
test_str_NotNormalized (Core.Dataset.DiscreteScale.DiscreteScaleTest) ... ok
test_str_NotNormalizedMaxInf (Core.Dataset.DiscreteScale.DiscreteScaleTest) ... ok
test_ParseMetaHeader_Empty_ReturnEmptyHeaders (Core.Dataset.MetadataParser.MetadataParserTest) ... ok
test_ParseMetaHeader_MultipleAttrWithBlanks_Parse (Core.Dataset.MetadataParser.MetadataParserTest) ... ok
test_ParseMetaHeader_SingleAttr_Parse (Core.Dataset.MetadataParser.MetadataParserTest) ... ok
test_GetNextCharInAlphabet_y_ReturnZ (Core.Languages.Grammars.IGrammar.TestIGrammar) ... ok
test_GetPreviousCharInAlphabet_A_ReturnNone (Core.Languages.Grammars.IGrammar.TestIGrammar) ... ok
test_GetPreviousCharInAlphabet_Z_ReturnY (Core.Languages.Grammars.IGrammar.TestIGrammar) ... ok
test_GetPreviousCharInAlphabet_b_ReturnA (Core.Languages.Grammars.IGrammar.TestIGrammar) ... ok
test_CapitalILetter_ToLowerCase (Core.Languages.Grammars.TRGrammar.TestTRGrammar) ... ok
test_GetAccents_GetDefaults (Core.Languages.Grammars.TRGrammar.TestTRGrammar) ... ok
test_HasAccents_Accent_False (Core.Languages.Grammars.TRGrammar.TestTRGrammar) ... ok
test_HasAccents_Accent_True (Core.Languages.Grammars.TRGrammar.TestTRGrammar) ... ok
test_LowerILetter_ToUpperCase (Core.Languages.Grammars.TRGrammar.TestTRGrammar) ... ok
test_ReduceAccents_AccentedWord_ReduceToLatin (Core.Languages.Grammars.TRGrammar.TestTRGrammar) ... ok
test_ReduceAccents_NonAccentedWord_DoNothing (Core.Languages.Grammars.TRGrammar.TestTRGrammar) ... ok
test_DefaultConv_FindUnitForm (Core.Morphology.ModelConvensions.ModelConvensionsTest) ... ok
test_DefaultConv_IsExpression (Core.Morphology.ModelConvensions.ModelConvensionsTest) ... ok
test_FormQueries (Core.Morphology.ModelConvensions.ModelConvensionsTest) ... ok
test_IsExpression_Invalid_ReturnFalse (Core.Morphology.ModelConvensions.ModelConvensionsTest) ... ok
test_IsRoot_Invalid_ReturnFalse (Core.Morphology.ModelConvensions.ModelConvensionsTest) ... ok
test_RootCount_WithOthers_Count (Core.Morphology.ModelConvensions.ModelConvensionsTest) ... ok
test_ALL_ENGLISH_MORPHOLOGICAL_ANALYSIS_SCENARIOS_intergration (Core.Morphology.MorphoLex.MorphoLexEnglishMorphologicalSegmentor.MorphoLexEnglishMorphologicalSegmentorIntegrationTest) ... 13:29:25: Loading metadatas too...
13:29:25: Dataset loaded from flat text(s).
13:29:26: Loading extra lexicon from IWordSource: <class 'src.Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapper'> ...
+----+-----------------+--------------------+--------------------+
|    | Word            | Expected           | Actual             |
|----+-----------------+--------------------+--------------------|
|  1 | revisioning     | -re_vise+ion       | -re_vise+ion       |
|  2 | description     | -de_script+ion     | -de_script+ion     |
|  3 | flies           | _fly               | _fly               |
|  4 | script          | _script            | _script            |
|  5 | broadcast       | _broad_cast        | _broad_cast        |
|  6 | scripting       | _script            | _script            |
|  7 | rebroadcast     | -re_broad_cast     | -re_broad_cast     |
|  8 | cinematographer | _cinema+tograph+er | _cinema+tograph+er |
|  9 | worthwhileness  | _worth_while+ness  | _worth_while+ness  |
| 10 | sustaining      | -sus_tain          | -sus_tain          |
+----+-----------------+--------------------+--------------------+
passed: ['{(algorithm)}', '_algorithm', None, None, None, None]
passed: ['{(animal)}', '_animal', None, None, None, None]
passed: ['{(algorithm)}>ic>', '_algorithm', None, None, None, None]
passed: ['{(algebra)}>ic>>al>', '_algebra', None, None, None, None]
passed: ['{(allegor)>ic>}>al>>ly>', '_allegor', None, None, None, '_allegoric']
passed: ['{(sense)}>ate>>ion>>al>>ist>', '_sense', None, None, None, None]
passed: ['{(wood)}(men)', '_wood', '_men', None, None, None]
passed: ['{(violon)(cello)>ist>}', '_violon', '_cello', None, None, '_violoncelloist']
passed: ['{(wrong)}{(head)}>ness>', '_wrong', '_head', None, None, None]
passed: ['{(voc)>abulary>}>ian>{(ism)}', '_voc', None, None, None, '_vocabulary']
passed: ['(petro){(chem)>ic>>al>}', '_petro', '_chem', None, None, '_chemical']
passed: ['{(typo)}(graph)>ic>>al>>ly>', '_typo', '_graph', None, None, None]
passed: ['(tele){(photo)}{(graph)}', '_tele', '_photo', '_graph', None, None]
passed: ['(tele){(photo)(graph)>y>}', '_tele', '_photo', '_graph', None, '_photography']
passed: ['(psycho){(pharma)(log)>ic>}>al>', '_psycho', '_pharma', '_log', None, '_pharmalogic']
passed: ['<up<{(date)}', '_date', None, None, None, None]
passed: ['<un<{(conscious)}>ness>', '_conscious', None, None, None, None]
passed: ['<un<{(ceremony)}>ious>>ness>', '_ceremony', None, None, None, None]
passed: ['<un<{(profess)>ion>}>al>>ly>', '_profess', None, None, None, '_profession']
passed: ['{<in<(stitute)}>ion>>al>>ize>>ion>', '_stitute', None, None, None, '_institute']
passed: ['{<re<(pair)}{(men)}', '_pair', '_men', None, None, '_repair']
passed: ['{(<re<(plic)>ate>)}', '_plic', None, None, None, None]
passed: ['<micro<{(bio)(log)>ic>}>al>', '_bio', '_log', None, None, '_biologic']
passed: ['<auto<{(bio)(graph)>ic>}>al>>ly>', '_bio', '_graph', None, None, '_biographic']
passed: ['(electro){<en<(cephalo)(gram)}', '_electro', '_cephalo', '_gram', None, '_encephalogram']
passed: ['<un<{<pre<(judic)}', '_judic', None, None, None, '_prejudic']
passed: ['<un<{<re<(strict)}>ly>', '_strict', None, None, None, '_restrict']
passed: ['<im<{<a<(propri)>ate>}>ly>', '_propri', None, None, None, '_apropriate']
passed: ['<un<{<ex<(cept)}>ion>>able>>y>', '_cept', None, None, None, '_except']
passed: ['<un<{<a<(know)(ledge)}', '_know', '_ledge', None, None, '_aknowledge']
passed: ['<un<<re<{<co<(struct)}', '_struct', None, None, None, '_costruct']
passed: ['(myco){(bacteri)>a>}', '_myco', '_bacteri', None, None, '_bacteria']
passed: ['<un<<re<{<co<(struct)}', '_struct', None, None, None, '_costruct']
passed: ['{<in<(_here)}>ant>', '_here', None, None, None, '_inhere']
passed 34 test cases!
ok
test_ApplySimpleSuffixations_HasNoSegmentationAfterPrefixationButInLexicon (Core.Morphology.MorphoLex.MorphoLexEnglishMorphologicalSegmentor.MorphoLexEnglishMorphologicalSegmentorIntegrationTest) ... ok
test_ApplySimpleSuffixations_HasNoSegmentationAfterSuffixationButInLexicon (Core.Morphology.MorphoLex.MorphoLexEnglishMorphologicalSegmentor.MorphoLexEnglishMorphologicalSegmentorIntegrationTest) ... ok
test_ApplySimpleSuffixations_HasSegmentationAfterPrefixation (Core.Morphology.MorphoLex.MorphoLexEnglishMorphologicalSegmentor.MorphoLexEnglishMorphologicalSegmentorIntegrationTest) ... ok
test_ApplySimpleSuffixations_HasSegmentationAfterSuffixation (Core.Morphology.MorphoLex.MorphoLexEnglishMorphologicalSegmentor.MorphoLexEnglishMorphologicalSegmentorIntegrationTest) ... ok
test_FormatToUpperMetaMorpheme_Prefix_Format (Core.Morphology.MorphoLex.MorphoLexSegmentedDataset.MorphoLexSegmentedDatasetTest) ... ok
test_FormatToUpperMetaMorpheme_Suffix_Format (Core.Morphology.MorphoLex.MorphoLexSegmentedDataset.MorphoLexSegmentedDatasetTest) ... ok
test_ParseToSegmentedWord_ALL30PLUSSCENARIOS (Core.Morphology.MorphoLex.MorphoLexSegmentedDataset.MorphoLexSegmentedDatasetTest) ... ok
test_ParseToSegmentedWord_AffixOnBase_ReturnBaseWithAffixAsRoot (Core.Morphology.MorphoLex.MorphoLexSegmentedDataset.MorphoLexSegmentedDatasetTest) ... ok
test_ParseToSegmentedWord_FullAffixesAndMultiMorphemeBase_ReturnBaseAsRoot (Core.Morphology.MorphoLex.MorphoLexSegmentedDataset.MorphoLexSegmentedDatasetTest) ... ok
test_ParseToSegmentedWord_MultipleBases_ReturnBasesAsASingleRootAndOthers (Core.Morphology.MorphoLex.MorphoLexSegmentedDataset.MorphoLexSegmentedDatasetTest) ... ok
test_ParseToSegmentedWord_NotSupportedChars_ReturnNull (Core.Morphology.MorphoLex.MorphoLexSegmentedDataset.MorphoLexSegmentedDatasetTest) ... ok
test_ParseToSegmentedWord_OneFromAll_Return (Core.Morphology.MorphoLex.MorphoLexSegmentedDataset.MorphoLexSegmentedDatasetTest) ... ok
test_ParseToSegmentedWord_TriplePrefixes_ParseRootAndPrefixes (Core.Morphology.MorphoLex.MorphoLexSegmentedDataset.MorphoLexSegmentedDatasetTest) ... ok
test_DetectRootsInStack_CompoundWordMissingInDerivationalLexicon_DetectConstitiuentsAsRoots (Core.Morphology.RootDetection.EnglishRootDetectionStackIntegrationTests.EnglishRootDetectionStackIntegrationTests) ... 13:29:27: Loading metadatas too...
13:29:27: Dataset loaded from flat text(s).
ok
+----+----------+--------------------+----------------------------+-------------------------------------------+
|    | Passed   | Compound           | Exp.Constitiuents          | Act.Constitiuents                         |
|----+----------+--------------------+----------------------------+-------------------------------------------|
|  1 | OK       | psychosurgery      | ['psycho', 'surgery']      | {'surg', 'surge', 'surgery', 'psycho'}    |
|  2 | OK       | biochemist         | ['bio', 'chemist', 'chem'] | {'chemist', 'che', 'chem', 'bio', 'mist'} |
|  3 | OK       | bio                | [None]                     | set()                                     |
|  4 | OK       | aeromechanics      | ['aero', 'mechanic']       | {'aero', 'mechan', 'mechanics'}           |
|  5 | OK       | psychophysics      | ['psycho', 'physic']       | {'phys', 'physics', 'psycho'}             |
|  6 | OK       | antilope           | ['lope', None]             | {'lope'}                                  |
|  7 | OK       | sentimentalisation | ['senti', None]            | {'sentimental', 'senti'}                  |
|  8 | OK       | vitalisation       | ['vital', None]            | {'vital'}                                 |
|  9 | OK       | mylodontidae       | ['mylodon', None]          | {'mylodon', 'mylodontid'}                 |
+----+----------+--------------------+----------------------------+-------------------------------------------+
test_DetectRootsInStack_RootScenarios (Core.Morphology.RootDetection.EnglishRootDetectionStackIntegrationTests.EnglishRootDetectionStackIntegrationTests) ... 13:29:28: Loading metadatas too...
13:29:28: Dataset loaded from flat text(s).
ok
test_EN_IsSharingRoot_SharedRootScenarios (Core.Morphology.RootDetection.SharingRootDetector.SharingRootDetectorIntegrationTest) ... +----+----------+-------------------+-------------+-----------------------------------+---------------------+
|    | Passed   | Surface           | Exp.Roots   | Act.Roots                         | Reason              |
|----+----------+-------------------+-------------+-----------------------------------+---------------------|
|  1 | OK       | animal            | ['animal']  | {'anim', 'animal'}                | MorphoLex++1LSuffix |
|  2 | OK       | gokhanercan       | []          | set()                             | nan                 |
|  3 | OK       | bohemianism       | ['bohemia'] | {'bohemian', 'bohemia', 'boehme'} | +1LSuffix+1LSuffix  |
|  4 | OK       | byzantine         | ['byzant']  | {'byzant', 'byzantine'}           | MorphoLex++1LSuffix |
|  5 | OK       | byzantium         | ['byzant']  | {'byzantium', 'byzant'}           | MorphoLex++1LSuffix |
|  6 | OK       | cabinetry         | ['cabinet'] | {'cabinet'}                       | +1LSuffix           |
|  7 | OK       | candelabra        | ['candela'] | {'candela', 'candelabra'}         | MorphoLex++1LSuffix |
|  8 | OK       | candelabrum       | ['candela'] | {'candela'}                       | +1LSuffix           |
|  9 | OK       | decriminalisation | ['crimin']  | {'criminalisation', 'crimin'}     | MorphoLex++1LPrefix |
| 10 | OK       | graphic           | ['graph']   | {'graph'}                         | MorphoLex++1LSuffix |
| 11 | OK       | graphia           | ['graph']   | {'graph'}                         | +1LSuffix           |
+----+----------+-------------------+-------------+-----------------------------------+---------------------+
13:29:28: Loading metadatas too...
13:29:28: Dataset loaded from flat text(s).
+----+----------+--------------------+----------------------+----------------+------------+----------+------------------------------------------------------------------------+------------------------------------------------------------------------+------------------------------------------------------------------------+
|    | Passed   | Word1              | Word2                | SharedRoot     | Expected   | Actual   | Reason                                                                 | Roots1 + detector + OOLRoots                                           | Roots2 + detector + OOLRoots                                           |
|----+----------+--------------------+----------------------+----------------+------------+----------+------------------------------------------------------------------------+------------------------------------------------------------------------+------------------------------------------------------------------------|
|  1 | OK       | academic           | academicianship      | academ         | True       | True     | w1:MorphoLex++1LSuffix   w2:MorphoLex++1LSuffix+1LCompounding          | ({'academ'}, 'MorphoLex++1LSuffix', set())                             | ({'academician', 'hip', 'academicians', 'academ'},                     |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | 'MorphoLex++1LSuffix+1LCompounding', set())                            |
|  2 | OK       | cardiologist       | cardiology           | cardio         | True       | True     | w1:+1LSuffix     w2:+1LSuffix                                          | ({'cardio'}, '+1LSuffix', {'cardi', 'cardiologis', 'cardiolog'})       | ({'cardio'}, '+1LSuffix', {'cardi', 'cardiol', 'cardiolog'})           |
|  3 | OK       | romanticisation    | romanticist          | romantic       | True       | True     | w1:+1LSuffix     w2:MorphoLex++1LSuffix                                | ({'romantic'}, '+1LSuffix', {'romanticisati', 'romanticisatio',        | ({'romantic'}, 'MorphoLex++1LSuffix', set())                           |
|    |          |                    |                      |                |            |          |                                                                        | 'romanticisat'})                                                       |                                                                        |
|  4 | OK       | angiologist        | angiology            | angio          | True       | True     | w1:+1LSuffix     w2:+1LSuffix                                          | ({'angio'}, '+1LSuffix', {'angiologis', 'ngiologist', 'angiolog'})     | ({'angio'}, '+1LSuffix', {'ngiology', 'angiol', 'angiolog'})           |
|  5 | OK       | animal             | animalisation        | animal         | True       | True     | w1:MorphoLex++1LSuffix   w2:+1LSuffix                                  | ({'anim', 'animal'}, 'MorphoLex++1LSuffix', set())                     | ({'animal'}, '+1LSuffix', {'animalisati', 'animalisatio',              |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | 'nimalisation', 'animalisat'})                                         |
|  6 | OK       | biochemist         | biochemistry         | bio            | True       | True     | w1:+1LCompounding -rec[MorphoLex++1LSuffix+1LCompounding]              | ({'chemist', 'che', 'chem', 'bio', 'mist'}, '+1LCompounding            | ({'chemist', 'chem', 'bio', 'biochemist', 'chemistry'},                |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix+1LCompounding]                                | 'MorphoLex++1LSuffix+1LCompounding -rec[MorphoLex++1LSuffix]           |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix]', set())                                     |
|    |          |                    |                      |                |            |          | w2:MorphoLex++1LSuffix+1LCompounding -rec[MorphoLex++1LSuffix]         | -rec[MorphoLex++1LSuffix+1LCompounding]', {'biochemis', 'ochemist',    |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix]                                              | 'biochem'})                                                            |                                                                        |
|  7 | OK       | biophysicist       | biophysics           | bio            | True       | True     | w1:+1LCompounding -rec[MorphoLex++1LSuffix] -rec[MorphoLex++1LSuffix]  | ({'bio', 'phys', 'physicist', 'physic'}, '+1LCompounding               | ({'bio', 'phys', 'physics'}, '+1LCompounding                           |
|    |          |                    |                      |                |            |          | w2:+1LCompounding -rec[MorphoLex++1LSuffix]                            | -rec[MorphoLex++1LSuffix] -rec[MorphoLex++1LSuffix]', {'biophysic',    | -rec[MorphoLex++1LSuffix]', {'biophy', 'biophys', 'ophysics'})         |
|    |          |                    |                      |                |            |          |                                                                        | 'ophysicist', 'biophysicis'})                                          |                                                                        |
|  8 | OK       | biofeedback        | feedback             | feedback       | True       | True     | w1:+1LCompounding -rec[MorphoLex++1LSuffix] -rec[MorphoLex++1LSuffix]  | ({'bio', 'feed', 'back', 'feedback'}, '+1LCompounding                  | ({'feed', 'back'}, 'MorphoLex++1LSuffix', set())                       |
|    |          |                    |                      |                |            |          | w2:MorphoLex++1LSuffix                                                 | -rec[MorphoLex++1LSuffix] -rec[MorphoLex++1LSuffix]', {'ofeedback',    |                                                                        |
|    |          |                    |                      |                |            |          |                                                                        | 'biofeed'})                                                            |                                                                        |
|  9 | OK       | aeromechanics      | mechanic             | mechan         | True       | True     | w1:+1LCompounding -rec[MorphoLex++1LSuffix]                            | ({'aero', 'mechan', 'mechanics'}, '+1LCompounding                      | ({'mechan'}, 'MorphoLex++1LSuffix', set())                             |
|    |          |                    |                      |                |            |          | w2:MorphoLex++1LSuffix                                                 | -rec[MorphoLex++1LSuffix]', {'eromechanics', 'aeromechan'})            |                                                                        |
| 10 | OK       | psychophysics      | physic               | phys           | True       | True     | w1:+1LCompounding -rec[MorphoLex++1LSuffix]                            | ({'phys', 'physics', 'psycho'}, '+1LCompounding                        | ({'phys'}, 'MorphoLex++1LSuffix', set())                               |
|    |          |                    |                      |                |            |          | w2:MorphoLex++1LSuffix                                                 | -rec[MorphoLex++1LSuffix]', {'psychophy', 'psychophys'})               |                                                                        |
| 11 | OK       | buddhism           | buddhist             | buddha         | True       | True     | w1:MorphoLex+    w2:MorphoLex+                                         | ({'buddha'}, 'MorphoLex+', set())                                      | ({'buddha'}, 'MorphoLex+', set())                                      |
| 12 | OK       | boehme             | bohemianism          | boehme         | True       | True     | w1:+1LSuffix     w2:+1LSuffix+1LSuffix                                 | ({'boehm'}, '+1LSuffix', set())                                        | ({'bohemian', 'bohemia', 'boehme'}, '+1LSuffix+1LSuffix', {'bohem'})   |
| 13 | OK       | arthrogram         | arthrography         | arthro         | True       | True     | w1:+1LCompounding        w2:+1LSuffix                                  | ({'gram', 'arthro'}, '+1LCompounding', {'rthrogram'})                  | ({'arthro'}, '+1LSuffix', {'arthrograph', 'rthrography'})              |
| 14 | OK       | verbena            | verbenaceae          | verbena        | True       | True     | w1:MorphoLex+    w2:+1LSuffix                                          | ({'verbena'}, 'MorphoLex+', set())                                     | ({'verbena'}, '+1LSuffix', {'verben', 'verbenacea', 'verbenace'})      |
| 15 | OK       | valerian           | valerianaceae        | valerian       | True       | True     | w1:      w2:+1LSuffix+1LSuffix                                         | (set(), '', {'valeria', 'valer', 'valeri'})                            | ({'valerian', 'valeriana'}, '+1LSuffix+1LSuffix', {'valerianacea',     |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | 'valerianace'})                                                        |
| 16 | OK       | ureter             | ureterocele          | ureter         | True       | True     | w1:      w2:+1LSuffix                                                  | (set(), '', {'reter', 'urete'})                                        | ({'ureter'}, '+1LSuffix', {'ureteroce', 'reterocele', 'ureterocel'})   |
| 17 | OK       | omphalocele        | omphalos             | omphal         | True       | True     | w1:      w2:                                                           | (set(), '', {'omphalocel', 'omphaloce', 'omphal', 'mphalocele'})       | (set(), '', {'omphal', 'mphalos'})                                     |
| 18 | OK       | sentimentalisation | sentimentalist       | sentimental    | True       | True     | w1:+1LSuffix     w2:MorphoLex++1LSuffix                                | ({'sentimental', 'senti'}, '+1LSuffix', {'sentimentalisatio',          | ({'sentimental', 'senti'}, 'MorphoLex++1LSuffix', set())               |
|    |          |                    |                      |                |            |          |                                                                        | 'sentimentalisat', 'sentimentalisati', 'ntimentalisation'})            |                                                                        |
| 19 | OK       | sigmoidoscope      | sigmoidoscopy        | sigmoidoscop   | True       | True     | w1:+1LSuffix     w2:+1LSuffix                                          | ({'sigmoid'}, '+1LSuffix', {'sigmoidoscop'})                           | ({'sigmoid'}, '+1LSuffix', {'sigmoidoscop', 'sigmoidos'})              |
| 20 | OK       | sigmoidectomy      | sigmoidoscopy        | sigmoid        | True       | True     | w1:+1LSuffix     w2:+1LSuffix                                          | ({'sigmoid'}, '+1LSuffix', {'sigmoidectom'})                           | ({'sigmoid'}, '+1LSuffix', {'sigmoidoscop', 'sigmoidos'})              |
| 21 | OK       | keynes             | keynesianism         | keynes         | True       | True     | w1:      w2:+1LSuffix+1LSuffix                                         | (set(), '', set())                                                     | ({'keynes', 'keynesian'}, '+1LSuffix+1LSuffix', {'keynesia'})          |
| 22 | OK       | archeologist       | archeology           | arche          | True       | True     | w1:+1LSuffix     w2:+1LSuffix                                          | ({'arche'}, '+1LSuffix', {'archeolog', 'archeologis', 'rcheologist',   | ({'arche'}, '+1LSuffix', {'archeolog', 'rcheology', 'archeol',         |
|    |          |                    |                      |                |            |          |                                                                        | 'archeo'})                                                             | 'archeo'})                                                             |
| 23 | OK       | arboriculture      | arboriculturist      | arboricultur   | True       | True     | w1:      w2:                                                           | (set(), '', {'arboricult', 'rboriculture', 'arboricultur'})            | (set(), '', {'arboriculturis', 'rboriculturist', 'arboricultur'})      |
| 24 | OK       | arthrogram         | arthrography         | arthro         | True       | True     | w1:+1LCompounding        w2:+1LSuffix                                  | ({'gram', 'arthro'}, '+1LCompounding', {'rthrogram'})                  | ({'arthro'}, '+1LSuffix', {'arthrograph', 'rthrography'})              |
| 25 | OK       | trauma             | traumatology         | trauma         | True       | True     | w1:MorphoLex+    w2:+1LSuffix                                          | ({'trauma'}, 'MorphoLex+', set())                                      | ({'trauma'}, '+1LSuffix', {'traumat', 'traumatolog', 'traumato',       |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | 'traumatol'})                                                          |
| 26 | OK       | tracheid           | tracheitis           | trache         | True       | True     | w1:      w2:                                                           | (set(), '', {'trache'})                                                | (set(), '', {'tracheit', 'trache'})                                    |
| 27 | OK       | sclerite           | scleritis            | scler          | True       | True     | w1:      w2:                                                           | (set(), '', {'scler', 'sclerit'})                                      | (set(), '', {'scler', 'sclerit'})                                      |
| 28 | OK       | schistosome        | schistosomiasis      | schistosom     | True       | True     | w1:      w2:                                                           | (set(), '', {'schistosom', 'schisto'})                                 | (set(), '', {'schistosomia', 'schistosom', 'schistosomias'})           |
| 29 | OK       | zigadene           | zigadenus            | zigaden        | True       | True     | w1:      w2:                                                           | (set(), '', {'zigaden'})                                               | (set(), '', {'zigaden'})                                               |
| 30 | OK       | amygdala           | amygdaloid           | amygdal        | True       | True     | w1:      w2:                                                           | (set(), '', {'amygdal', 'mygdala'})                                    | (set(), '', {'amygdal', 'amygdalo', 'mygdaloid'})                      |
| 31 | OK       | aclant             | saclant              |                | False      | False    |                                                                        | (set(), '', {'aclan', 'clant'})                                        | (set(), '', {'saclan'})                                                |
| 32 | OK       | immunofluorescence | autofluorescence     | fluor          | True       | True     | w1:+1LCompounding -rec[MorphoLex+] -rec[+1LSuffix]                     | ({'immun', 'fluorescence', 'immuno', 'fluor'}, '+1LCompounding         | ({'auto', 'fluor', 'fluorescence'}, 'MorphoLex++1LPrefix', set())      |
|    |          |                    |                      |                |            |          | w2:MorphoLex++1LPrefix                                                 | -rec[MorphoLex+] -rec[+1LSuffix]', {'munofluorescence',                |                                                                        |
|    |          |                    |                      |                |            |          |                                                                        | 'immunofluorescenc', 'immunofluoresc'})                                |                                                                        |
| 33 | OK       | anglican           | anglia               | anglo          | True       | True     | w1:MorphoLex+    w2:MorphoLex+                                         | ({'anglo'}, 'MorphoLex+', set())                                       | ({'anglo'}, 'MorphoLex+', set())                                       |
| 34 | OK       | onomasticon        | onomastics           | onomast        | True       | True     | w1:+1LSuffix+1LCompounding -rec[+1LCompounding                         | ({'onomast', 'mast', 'icon', 'mas', 'ono', 'onomastic'},               | ({'onomast'}, '+1LSuffix', {'onomas', 'nomastics', 'omastics'})        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix]] -rec[+1LCompounding                         | '+1LSuffix+1LCompounding -rec[+1LCompounding                           |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix]] -rec[+1LCompounding                         | -rec[MorphoLex++1LSuffix]] -rec[+1LCompounding                         |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix]]  w2:+1LSuffix                               | -rec[MorphoLex++1LSuffix]] -rec[+1LCompounding                         |                                                                        |
|    |          |                    |                      |                |            |          |                                                                        | -rec[MorphoLex++1LSuffix]]', {'nomasticon', 'onomastico',              |                                                                        |
|    |          |                    |                      |                |            |          |                                                                        | 'omasticon'})                                                          |                                                                        |
| 35 | OK       | presidio           | presidium            | presidi        | True       | True     | w1:      w2:                                                           | (set(), '', {'sidio', 'presidi'})                                      | (set(), '', {'presidi', 'sidium', 'presid'})                           |
| 36 | OK       | arthroscope        | arthroscopy          | arthroscop     | True       | True     | w1:+1LCompounding        w2:                                           | ({'scope', 'arthro'}, '+1LCompounding', {'arthr', 'rthroscope',        | (set(), '', {'rthroscopy', 'arthros', 'arthroscop', 'arthr'})          |
|    |          |                    |                      |                |            |          |                                                                        | 'arthroscop'})                                                         |                                                                        |
| 37 | OK       | blennioid          | blennioidea          | blennio        | True       | True     | w1:      w2:                                                           | (set(), '', {'blenni', 'blennio'})                                     | (set(), '', {'blennioide', 'blennio'})                                 |
| 38 | OK       | anesthesia         | anesthesiology       | anesthesi      | True       | True     | w1:      w2:                                                           | (set(), '', {'nesthesia', 'anesthes', 'anesthesi'})                    | (set(), '', {'nesthesiology', 'anesthesio', 'anesthesi',               |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | 'anesthesiolog', 'anesthesiol'})                                       |
| 39 | OK       | anesthesiologist   | anesthesiology       | anesthesiolog  | True       | True     | w1:      w2:                                                           | (set(), '', {'anesthesio', 'anesthesi', 'anesthesiologis',             | (set(), '', {'nesthesiology', 'anesthesio', 'anesthesi',               |
|    |          |                    |                      |                |            |          |                                                                        | 'anesthesiolog', 'nesthesiologist'})                                   | 'anesthesiolog', 'anesthesiol'})                                       |
| 40 | OK       | acanthopterygian   | acanthopterygii      | acanthopterygi | True       | True     | w1:      w2:                                                           | (set(), '', {'acanthopterygi', 'acanthopteryg', 'acanthopterygia',     | (set(), '', {'acanthopterygi', 'canthopterygii'})                      |
|    |          |                    |                      |                |            |          |                                                                        | 'canthopterygian'})                                                    |                                                                        |
| 41 | OK       | autogenics         | autogeny             | autogen        | True       | True     | w1:      w2:+1LSuffix                                                  | (set(), '', {'genics', 'utogenics', 'autogen'})                        | ({'auto'}, '+1LSuffix', {'utogeny', 'autogen'})                        |
| 42 | OK       | haematologist      | haematology          | hema           | True       | True     | w1:MorphoLex+    w2:MorphoLex+                                         | ({'hema', 'log'}, 'MorphoLex+', set())                                 | ({'hema', 'log'}, 'MorphoLex+', set())                                 |
| 43 | OK       | haemoglobin        | haemoglobinemia      | haemo          | True       | True     | w1:MorphoLex++1LCompounding -rec[+1LSuffix] -rec[+1LSuffix]            | ({'haemo', 'globin', 'haem', 'glob'}, 'MorphoLex++1LCompounding        | ({'haemo', 'haemoglobin', 'globin'}, '+1LSuffix', {'haemoglobinemi',   |
|    |          |                    |                      |                |            |          | w2:+1LSuffix                                                           | -rec[+1LSuffix] -rec[+1LSuffix]', set())                               | 'haemoglobinem', 'haemoglobine'})                                      |
| 44 | OK       | acanthocyte        | acanthocytosis       | acantho        | True       | True     | w1:+1LSuffix     w2:+1LSuffix                                          | ({'acantho'}, '+1LSuffix', {'acanthocyt', 'canthocyte'})               | ({'acantho'}, '+1LSuffix', {'acanthocytos', 'canthocytosis',           |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | 'acanthocyto'})                                                        |
| 45 | OK       | thrombocyte        | thrombocytopenia     | thrombo        | True       | True     | w1:      w2:                                                           | (set(), '', {'thrombo', 'thrombocyt'})                                 | (set(), '', {'thrombo', 'thrombocytopeni', 'thrombocytopen'})          |
| 46 | OK       | megapodiidae       | megapode             | megapod        | True       | True     | w1:      w2:                                                           | (set(), '', {'megapodiid', 'podiidae', 'megapod', 'megapodiida',       | (set(), '', {'megap', 'megapod'})                                      |
|    |          |                    |                      |                |            |          |                                                                        | 'megapodi'})                                                           |                                                                        |
| 47 | OK       | megathere          | megatheriidae        | megather       | True       | True     | w1:+1LPrefix     w2:+1LSuffix                                          | ({'there'}, '+1LPrefix', {'megather'})                                 | ({'megatheriid'}, '+1LSuffix', {'megatheri', 'theriidae',              |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | 'megatheriida', 'megather'})                                           |
| 48 | OK       | mycoplasma         | mycoplasmataceae     | mycoplasma     | True       | True     | w1:+1LCompounding -rec[MorphoLex++1LSuffix]      w2:+1LSuffix          | ({'plasm', 'plasma', 'myco'}, '+1LCompounding                          | ({'mycoplasma'}, '+1LSuffix', {'mycoplasmatacea', 'mycoplasmata',      |
|    |          |                    |                      |                |            |          |                                                                        | -rec[MorphoLex++1LSuffix]', {'mycoplasm'})                             | 'mycoplasmat', 'mycoplasmatace'})                                      |
| 49 | OK       | mylodon            | mylodontidae         | mylodon        | True       | True     | w1:      w2:+1LSuffix+1LSuffix                                         | (set(), '', {'mylodo', 'mylod'})                                       | ({'mylodon', 'mylodontid'}, '+1LSuffix+1LSuffix', {'mylodontida',      |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | 'mylodont'})                                                           |
| 50 | OK       | aerophilately      | aerophile            | aero           | True       | True     | w1:+1LCompounding -rec[MorphoLex++1LCompounding                        | ({'aero', 'late', 'phi', 'ely', 'lat', 'philately', 'lately'},         | ({'aero'}, '+1LSuffix', {'erophile', 'aeroph', 'aerophi', 'aerophil'}) |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | '+1LCompounding -rec[MorphoLex++1LCompounding                          |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix+1LCompounding]                                |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]] -rec[MorphoLex++1LCompounding | -rec[MorphoLex++1LSuffix+1LCompounding]                                |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix+1LCompounding]] -rec[MorphoLex++1LCompounding |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix+1LCompounding]                                |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]] -rec[MorphoLex++1LCompounding | -rec[MorphoLex++1LSuffix+1LCompounding]                                |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix+1LCompounding]] -rec[MorphoLex++1LCompounding |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix+1LCompounding]                                |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]] -rec[MorphoLex++1LCompounding | -rec[MorphoLex++1LSuffix+1LCompounding]                                |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix+1LCompounding]] -rec[MorphoLex++1LCompounding |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix+1LCompounding]                                |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]] -rec[MorphoLex++1LCompounding | -rec[MorphoLex++1LSuffix+1LCompounding]                                |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix+1LCompounding]] -rec[MorphoLex++1LCompounding |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]                                | -rec[MorphoLex++1LSuffix+1LCompounding]                                |                                                                        |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LCompounding]]     w2:+1LSuffix              | -rec[MorphoLex++1LSuffix+1LCompounding]                                |                                                                        |
|    |          |                    |                      |                |            |          |                                                                        | -rec[MorphoLex++1LSuffix+1LCompounding]]', {'aerophilate',             |                                                                        |
|    |          |                    |                      |                |            |          |                                                                        | 'aerophilatel', 'erophilately'})                                       |                                                                        |
| 51 | OK       | aesthete           | aesthetic            | thet           | True       | True     | w1:MorphoLex++1LPrefix   w2:MorphoLex++1LPrefix+1LPrefix               | ({'esthete', 'thet'}, 'MorphoLex++1LPrefix', set())                    | ({'esthetic', 'thet', 'thetic'}, 'MorphoLex++1LPrefix+1LPrefix',       |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | set())                                                                 |
| 52 | OK       | amygdala           | amygdalotomy         | amygdal        | True       | True     | w1:      w2:                                                           | (set(), '', {'amygdal', 'mygdala'})                                    | (set(), '', {'mygdalotomy', 'amygdalotom', 'amygdal'})                 |
| 53 | OK       | anesthesia         | anesthesiologist     | anesthesi      | True       | True     | w1:      w2:                                                           | (set(), '', {'nesthesia', 'anesthes', 'anesthesi'})                    | (set(), '', {'anesthesio', 'anesthesi', 'anesthesiologis',             |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | 'anesthesiolog', 'nesthesiologist'})                                   |
| 54 | OK       | biochemistry       | immunohistochemistry | chem           | True       | True     | w1:MorphoLex++1LSuffix+1LCompounding -rec[MorphoLex++1LSuffix]         | ({'chemist', 'chem', 'bio', 'biochemist', 'chemistry'},                | ({'immun', 'histo', 'chem'}, 'MorphoLex+', set())                      |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix]         w2:MorphoLex+                        | 'MorphoLex++1LSuffix+1LCompounding -rec[MorphoLex++1LSuffix]           |                                                                        |
|    |          |                    |                      |                |            |          |                                                                        | -rec[MorphoLex++1LSuffix]', set())                                     |                                                                        |
| 55 | OK       | birdnest           | birdnesting          | bird           | True       | True     | w1:MorphoLex++1LCompounding      w2:Morphy                             | ({'bird', 'nest'}, 'MorphoLex++1LCompounding', set())                  | ({'bird', 'nest'}, 'Morphy', set())                                    |
| 56 | OK       | bishopry           | bishopric            | bishop         | True       | True     | w1:+1LSuffix     w2:MorphoLex+                                         | ({'bishop'}, '+1LSuffix', {'bishopr', 'shopry'})                       | ({'bishop'}, 'MorphoLex+', set())                                      |
| 57 | OK       | bowdleriser        | bowdlerism           | bowdler        | True       | True     | w1:+1LSuffix+1LSuffix    w2:+1LSuffix                                  | ({'bowdler', 'bowdlerise'}, '+1LSuffix+1LSuffix', {'bowdleris'})       | ({'bowdler'}, '+1LSuffix', set())                                      |
| 58 | OK       | byzant             | byzantinism          | byzant         | True       | True     | w1:      w2:+1LSuffix                                                  | (set(), '', {'byzan'})                                                 | ({'byzant'}, '+1LSuffix', {'byzantin', 'zantinism', 'byzanti'})        |
| 59 | OK       | byzant             | byzantium            | byzant         | True       | True     | w1:      w2:MorphoLex++1LSuffix                                        | (set(), '', {'byzan'})                                                 | ({'byzantium', 'byzant'}, 'MorphoLex++1LSuffix', set())                |
| 60 | OK       | consuetude         | consuetudinal        | consuetude     | True       | True     | w1:MorphoLex+    w2:MorphoLex+                                         | ({'consuetude'}, 'MorphoLex+', set())                                  | ({'consuetude'}, 'MorphoLex+', set())                                  |
| 61 | OK       | consuetude         | consuetudinary       | consuetude     | True       | True     | w1:MorphoLex+    w2:MorphoLex+                                         | ({'consuetude'}, 'MorphoLex+', set())                                  | ({'consuetude'}, 'MorphoLex+', set())                                  |
| 62 | OK       | criminal           | criminalization      | criminal       | True       | True     | w1:MorphoLex++1LSuffix   w2:MorphoLex++1LSuffix                        | ({'crimin'}, 'MorphoLex++1LSuffix', set())                             | ({'criminal', 'crimin'}, 'MorphoLex++1LSuffix', set())                 |
| 63 | OK       | criminal           | decriminalisation    | crimin         | True       | True     | w1:MorphoLex++1LSuffix   w2:MorphoLex++1LPrefix                        | ({'crimin'}, 'MorphoLex++1LSuffix', set())                             | ({'criminalisation', 'crimin'}, 'MorphoLex++1LPrefix', set())          |
| 64 | OK       | cytogeny           | cytogenetics         | cyto           | True       | True     | w1:+1LSuffix     w2:+1LCompounding -rec[MorphoLex++1LSuffix+1LSuffix]  | ({'cyto'}, '+1LSuffix', {'cytogen'})                                   | ({'gene', 'cyto', 'genetics', 'genet', 'gen'}, '+1LCompounding         |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix+1LSuffix] -rec[MorphoLex++1LSuffix+1LSuffix]  |                                                                        | -rec[MorphoLex++1LSuffix+1LSuffix] -rec[MorphoLex++1LSuffix+1LSuffix]  |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | -rec[MorphoLex++1LSuffix+1LSuffix]', {'cytogene', 'cytogenet'})        |
| 65 | OK       | harlotry           | harlot               | harlot         | True       | True     | w1:+1LSuffix     w2:MorphoLex++1LCompounding                           | ({'harlot'}, '+1LSuffix', {'harlotr'})                                 | ({'lot', 'harlot', 'har'}, 'MorphoLex++1LCompounding', set())          |
| 66 | OK       | mammogram          | mammography          | mammo          | True       | True     | w1:+1LCompounding        w2:+1LSuffix                                  | ({'gram', 'mammo'}, '+1LCompounding', set())                           | ({'mammo'}, '+1LSuffix', {'mammograph'})                               |
| 67 | OK       | rollerblading      | rollerblader         | rollerblade    | True       | True     | w1:MorphoLex+Morphy      w2:MorphoLex++1LSuffix                        | ({'rollerblade'}, 'MorphoLex+Morphy', set())                           | ({'rollerblade'}, 'MorphoLex++1LSuffix', set())                        |
| 68 | OK       | thermal            | thermalgesia         | thermo         | True       | True     | w1:MorphoLex++1LSuffix   w2:+1LCompounding -rec[MorphoLex++1LSuffix]   | ({'thermo', 'therm'}, 'MorphoLex++1LSuffix', set())                    | ({'gesia', 'thermo', 'thermal', 'therm'}, '+1LCompounding              |
|    |          |                    |                      |                |            |          | -rec[MorphoLex++1LSuffix]                                              |                                                                        | -rec[MorphoLex++1LSuffix] -rec[MorphoLex++1LSuffix]', {'thermalges',   |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | 'thermalgesi'})                                                        |
| 69 | OK       | cyberwar           | cyberart             | cyber          | True       | True     | w1:+1LCompounding        w2:+1LCompounding                             | ({'cyber', 'war'}, '+1LCompounding', {'cyberwa', 'cyberw'})            | ({'cyber', 'art'}, '+1LCompounding', {'cyberar'})                      |
| 70 | OK       | hematology         | haematology          | hema           | True       | True     | w1:MorphoLex++1LSuffix   w2:MorphoLex+                                 | ({'hema', 'log'}, 'MorphoLex++1LSuffix', set())                        | ({'hema', 'log'}, 'MorphoLex+', set())                                 |
| 71 | OK       | haematologist      | hematology           | hema           | True       | True     | w1:MorphoLex+    w2:MorphoLex++1LSuffix                                | ({'hema', 'log'}, 'MorphoLex+', set())                                 | ({'hema', 'log'}, 'MorphoLex++1LSuffix', set())                        |
| 72 | OK       | encyclopedism      | encyclopaedism       | cycle          | True       | True     | w1:MorphoLex+    w2:MorphoLex+                                         | ({'ped', 'cycle'}, 'MorphoLex+', set())                                | ({'ped', 'cycle'}, 'MorphoLex+', set())                                |
| 73 | OK       | cyclopedia         | cyclopaedia          | cycle          | True       | True     | w1:MorphoLex+    w2:MorphoLex+                                         | ({'ped', 'cycle'}, 'MorphoLex+', set())                                | ({'ped', 'cycle'}, 'MorphoLex+', set())                                |
| 74 | OK       | cyclopedia         | encyclopaedism       | cycle          | True       | True     | w1:MorphoLex+    w2:MorphoLex+                                         | ({'ped', 'cycle'}, 'MorphoLex+', set())                                | ({'ped', 'cycle'}, 'MorphoLex+', set())                                |
| 75 | OK       | vitalisation       | sentimentalisation   |                | False      | False    |                                                                        | ({'vital'}, '+1LSuffix', {'vitalisati', 'vitalisatio', 'vitalisat'})   | ({'sentimental', 'senti'}, '+1LSuffix', {'sentimentalisatio',          |
|    |          |                    |                      |                |            |          |                                                                        |                                                                        | 'sentimentalisat', 'sentimentalisati', 'ntimentalisation'})            |
+----+----------+--------------------+----------------------+----------------+------------+----------+------------------------------------------------------------------------+------------------------------------------------------------------------+------------------------------------------------------------------------+
All 76 passed!
ok
test_ALL_INFLECTIONS (Core.Morphology.Stemmers.MorphyInflectionalEnglishStemmer.MorphyInflectionalEnglishStemmerTest) ... ok
test_AnyMeasure_MeasureOverlapImpl_NoGrams_0 (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_AnyMeasure_WordSimilarity_WithNgramAsExtractor_DistinctGrams_Half (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_AnyMeasure_WordSimilarity_WithNgramExtractor_NoGramsToGenerate_0 (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_Dice_MeasureOverlapImpl_HalfMatch_05 (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_Dice_MeasureOverlapImpl_HalfMatch_066 (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_Dice_MeasureOverlapImpl_NoOverlaps_0 (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_Dice_MeasureOverlapImpl_SameWords_1 (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_Jaccard_MeasureOverlapImpl_NoOverlaps_0 (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_Jaccard_MeasureOverlapImpl_SameWords_1 (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_Overlap_MeasureOverlapImpl_HalfMatch_05 (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_Overlap_MeasureOverlapImpl_NoOverlaps_0 (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_Overlap_MeasureOverlapImpl_SameWords_1 (Core.Orthographic.OverlappingMeasuresTests.OverlappingMeasuresTests) ... ok
test_ContainsPunctuation_Hypens_ReturnTrue (Core.Preprocessing.Preprocessors.PreprocessorsTest) ... ok
test_ContainsPunctuation_PlainText_ReturnFalse (Core.Preprocessing.Preprocessors.PreprocessorsTest) ... ok
test_RemovePunctuation_Hypens_Remove (Core.Preprocessing.Preprocessors.PreprocessorsTest) ... ok
test_ToFiltered_UnderThresholdWords_Remove (Core.Preprocessing.WordsFilterer.WordsFiltererTest) ... ok
test_ToFiltered_WordsWithPuncts_RemoveWordsWithPunts (Core.Preprocessing.WordsFilterer.WordsFiltererTest) ... ok
test_ExtractGrams_2Gram_2GramWithRecurringGrams (Core.Segmentation.Ngram.NgramSegmentorTest) ... ok
test_ExtractOrderedGrams_2Gram_2GramWithRecurringGrams (Core.Segmentation.Ngram.NgramSegmentorTest) ... ok
test_ExtractRecurringGrams_2Gram_2GramWithRecurringGrams (Core.Segmentation.Ngram.NgramSegmentorTest) ... ok
test_SegmentImpl_2Gram_2GramWithRecurringGrams_PreserveRecurringsAsASegmentor (Core.Segmentation.Ngram.NgramSegmentorTest) ... ok
test_Iterate_FullMorphologyWithRecurringMorphemes_PreserveRecurringOrdering (Core.Segmentation.SegmentorBase.SegmentorBaseTest) ... ok
test_ParseConfigValue_FullWithMultipleParams_Parse (Core.Segmentation.SegmentorBase.SegmentorBaseTest) ... ok
test_ParseConfigValue_NoParams_Parse (Core.Segmentation.SegmentorBase.SegmentorBaseTest) ... ok
test_Tokenize_CaseDifference_TokenizeCaseSensitive (Core.Segmentation.Tokenizers.NLTKWhitespaceTokenizer.NLTKWhitespaceTokenizerTest) ... ok
test_Tokenize_DoubleWhiteSpace_TokenizeTrimmed (Core.Segmentation.Tokenizers.NLTKWhitespaceTokenizer.NLTKWhitespaceTokenizerTest) ... ok
test_CacheWrapping_TwoTimes (Core.Segmentation.Tokenizers.TokenizerCacher.NLTKWhitespaceTokenizerTest) ... ok
test_WordpairsInTwoDifferentBlacklistedConcepts_ReturnRelated (Core.WordNet.Classifiers.BlacklistedConceptsWordNetRelatednessFilterer.BlacklistedConceptsWordNetRelatednessFiltererTest) ... +----+-----------+------------+----------+
|    | Word      | Expected   | Actual   |
|----+-----------+------------+----------|
|  1 | cats      | cat        | cat      |
|  2 | denied    | deny       | deny     |
|  3 | churches  | church     | church   |
|  4 | built     | build      | build    |
|  5 | scripting | script     | script   |
|  6 | walking   | walk       | walk     |
|  7 | building  | build      | build    |
+----+-----------+------------+----------+
ok
test_OnlyOneMatchingUnrelatedInstances_ReturnNone (Core.WordNet.Classifiers.ConceptWiseWordNetRelatednessFilterer.ConceptWiseWordNetRelatednessFiltererTest) ... ok
test_TwoIndirectInstancesInReverse_ReturnRelated (Core.WordNet.Classifiers.ConceptWiseWordNetRelatednessFilterer.ConceptWiseWordNetRelatednessFiltererTest) ... ok
test_TwoIndirectInstances_ReturnRelated (Core.WordNet.Classifiers.ConceptWiseWordNetRelatednessFilterer.ConceptWiseWordNetRelatednessFiltererTest) ... ok
test_str (Core.WordNet.IWordTaxonomy.TaxonomyTypeTest) ... ok
test_DetectRoot_NoPOSArgAndNoMatching_ReturnEmptyList (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_DetectRoot_StemmerCases (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_DetectRoot_WithPOSArgumentButExpectedNoMatchingForPOS_ReturnEmpty (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_DetectRoot_WithPOSArgument_ReturnRoot (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_DetectRoot_WithoutAnyPOSArgument_ReturnFirstMatchingOrNone (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_GetParents_InstanceSynset_ReturnParent (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_GetParents_SynsetWithParent_Return (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_GetRelateds_MemberOrMeronym_ReturnAsRelated (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_GetTypeCodesOfHierarchy_InstanceWord_ReturnTypeRelationsViaCombiningRelationsTypes (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_GetTypeCodesOfHierarchy_LemmaWithMultipleSenses_ReturnCombined (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_GetTypeCodesOfHierarchy_LemmaWithSynonmyLemmasInItsSense_ReturnSynonymsToo (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_GetTypeCodesOfHierarchy_SynsetWithNoHypernymTypeHierachy_ReturnEmptyList (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_GetTypeCodesOfHierarchy_WordWithBothHypernymAndInstanceRelations_ReturnCombined (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_IsInType_WithPosValidNames_Return (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_Is_ThingIsTypeCases (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
+----+-----------+----------------+---------------+----------+
|    | Surface   | ExpectedRoot   | ActualRoots   | Passed   |
|----+-----------+----------------+---------------+----------|
|  1 | tables    | table          | table         | OK       |
+----+-----------+----------------+---------------+----------+
All 2 ThingIsType test cases passed.
+----+-------------------------------+---------------------------------+------------+----------+----------+
|    | Thing                         | Type                            | Expected   | Actual   | Passed   |
|----+-------------------------------+---------------------------------+------------+----------+----------|
|  1 | Synset('dog.n.01')            | Synset('animal.n.01')           | True       | True     | OK       |
|  2 | Synset('animal.n.01')         | Synset('entity.n.01')           | True       | True     | OK       |
|  3 | Synset('cancer.n.01')         | Synset('illness.n.01')          | True       | True     | OK       |
|  4 | Synset('animal.n.01')         | Synset('illness.n.01')          | False      | False    | OK       |
|  5 | Synset('ambystomid.n.01')     | Synset('living_thing.n.01')     | True       | True     | OK       |
|  6 | Synset('ambystomatidae.n.01') | Synset('biological_group.n.01') | True       | True     | OK       |
|  7 | Synset('table.n.01')          | Synset('animal.n.01')           | False      | False    | OK       |
+----+-------------------------------+---------------------------------+------------+----------+----------+
All 8 ThingIsType test cases passed.
13:29:49: WordSimilarityNormalizerWrapper.Eagerly normalizing 2 wordpairs ...
13:29:49: wordpair: 0/2 (0.0%)
13:29:49: WordSimilarityNormalizerWrapperNormalization completed!
13:29:49: WordSimilarityNormalizerWrapper.Eagerly normalizing 2 wordpairs ...
13:29:49: wordpair: 0/2 (0.0%)
13:29:49: WordSimilarityNormalizerWrapperNormalization completed!



--------TEST RESULTS (Tests)--------------

->TESTS PASSED (Tests)
<unittest.runner.TextTestResult run=138 errors=0 failures=0>

Skipping integration tests (Tests)

test_ToTaxonomyType (Core.WordNet.NLTKWordNetWrapper.NLTKWordNetWrapperIntegrationTest) ... ok
test_AreReferencingEachOtherInDefinitions_DefinitionsReferEachOtherWordsNearPuncts_RemovePunctsAndReturnMatched (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_AreReferencingEachOtherInDefinitions_DefinitionsReferEachOther_ReturnMatched (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_AreReferencingEachOtherInDefinitions_DefinitionsReferWordsConstituteOfSynonyms_ExplodeSynonymsAndMatch (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_ContainsKeywordInTypeHierarchy_MultiSenseAndNoReferenceButEntity_ReturnFalse (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_ContainsKeywordInTypeHierarchy_NoWordLengthFilteringForRawMatches_True (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_ContainsKeywordInTypeHierarchy_OneDefReferencingOthersTypeInHierarchy_ReturnTrue (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_ContainsKeywordInTypeHierarchy_OneDefReferencingOthersTypeInViaPhraseHierarchy_MatchViaFullPhraseMatch (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_ContainsKeywordInTypeHierarchy_OneDefReferencingOthersTypeInViaPhraseHierarchy_MatchViaMatchingPhraseSegment (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_ContainsKeywordInTypeHierarchy_OneDefReferencingOthersTypeViaPhrasePrepositionHierarchy_IgnoreShortSegmentsInPhrases (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_ContainsKeywordInTypeHierarchy_OneDefReferencingSynonymOfATypeInHierarchy_ReturnTrue (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_ContainsKeywordInTypeHierarchy_OneRootInDefReferencingOthersTypeInHierarchy_ReturnTrue (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_ExtractTwoSegmentPhrases_HasPhrases_Extact (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_ExtractTwoSegmentPhrases_SingleWord_ReturnEmpty (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_TrimTypesByDepthRatio_HierWithNoEntity_NoEffectiveTypes (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_TrimTypesByDepthRatio_SingleWithHalfDepth_ReturnFirstHalf (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_TrimTypesByDepthRatio_TwoSensesWithFullDepth (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test__DecomposePhrasesOfSets_ENTypeCodes_SplitUnderscores (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test__DecomposePhrasesOfSets_TRTypeCodes_SplitUnderscores (Core.WordNet.WordPairDefinitionSourceFilter.WordPairDefinitionSourceFilterTest) ... ok
test_TwoSymetticalyWordPairs_ReturnSameHashes (Core.WordPair.WordPairTest) ... ok
test_GeneratePossibleWordPairs_RegularSet_AvoidSymetricalDuplicates (Core.WordPairSynthesizer.WordPairSynthesizerTest) ... ok
test_ApplyScaling_DiffScale_Scale (Core.WordSim.IWordSimilarity.IWordSimilarityTest) ... ok
test_ApplyScaling_MinIsNotZero (Core.WordSim.IWordSimilarity.IWordSimilarityTest) ... ok
test_ApplyScaling_SameScales_ReturnSame (Core.WordSim.IWordSimilarity.IWordSimilarityTest) ... ok
test_MergeDatasets_MergeTwoWithDifferentScales_NoDuplicates (Core.WordSim.WordSimDataset.WordSimDatasetTest) ... ok
test_CtorWrapAndToNewWordPairs_UnnormalizedMetric_Normalize (Core.WordSim.WordSimilarityNormalizerWrapper.WordSimilarityNormalizerWrapperTest) ... ok
test_CtorWrap_NormalizedMetric_ScaleOnly (Core.WordSim.WordSimilarityNormalizerWrapper.WordSimilarityNormalizerWrapperTest) ... ok
test_Humanize_NotSmallNumber_WithReportActualNumber_DoReportActual (Tools.FormatHelper.FormatHelperTest) ... ok
test_Humanize_SmallNumber_WithReportActualNumber_DoNotReportActual (Tools.FormatHelper.FormatHelperTest) ... ok
test_Humanize_WithReportActualNumber (Tools.FormatHelper.FormatHelperTest) ... ok
test_Coelesce_ChooseFirstStr (Tools.StringHelper.StringHelperTest) ... ok
test_Coelesce_PassEmpties (Tools.StringHelper.StringHelperTest) ... ok
test_Coelesce_PassNones (Tools.StringHelper.StringHelperTest) ... ok
test_FindFirstBlockInBetweenOrDefault_NoMatching_ReturnTheDefault (Tools.StringHelper.StringHelperTest) ... ok
test_FindFirstBlockInBetweenOrDefault_SingleBlock_Return (Tools.StringHelper.StringHelperTest) ... ok
test_FindFirstBlockInBetween_MultipleBlocks_ReturnFirstBlock (Tools.StringHelper.StringHelperTest) ... ok
test_FindFirstBlockInBetween_NoMatching_ReturnNone (Tools.StringHelper.StringHelperTest) ... ok
test_FindFirstBlockInBetween_SameBlockFromBegiggingAndEnding_LookFor2ndMatchForEndingBlock (Tools.StringHelper.StringHelperTest) ... ok
test_FindFirstBlockInBetween_SingleBlockAndBeginningBlockIsBiggerThanOneChar_ReturnFirstBlock (Tools.StringHelper.StringHelperTest) ... ok
test_FindFirstBlockInBetween_SingleBlockAndEndingBlockAreBiggerThanOneChar_ReturnFirstBlock (Tools.StringHelper.StringHelperTest) ... ok
test_HasAnyNumber_DoesNotHaveNumber_ReturnFalse (Tools.StringHelper.StringHelperTest) ... ok
test_HasAnyNumber_HasNumber_ReturnTrue (Tools.StringHelper.StringHelperTest) ... ok
test_RemoveFirstCharIf_AnotherChar_Remove (Tools.StringHelper.StringHelperTest) ... ok
test_RemoveFirstCharIf_SameChar_Remove (Tools.StringHelper.StringHelperTest) ... ok
test_RemoveLastCharIf_AnotherChar_Remove (Tools.StringHelper.StringHelperTest) ... ok
test_RemoveLastCharIf_SameChar_Remove (Tools.StringHelper.StringHelperTest) ... ok

----------------------------------------------------------------------
Ran 138 tests in 23.656s

OK

Process finished with exit code 0

```