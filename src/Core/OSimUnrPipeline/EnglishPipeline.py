from typing import List

from src.Core.Languages.LinguisticContext import LinguisticContext
from src.Core.Morphology.MorphoLex.MorphoLexSegmentedDataset import MorphoLexSegmentedDataset
from src.Core.Morphology.POSTypes import POSTypes
from src.Core.Morphology.RootDetection.IRootDetectorStack import IRootDetectorStack
from src.Core.Morphology.RootDetection.RootDetectorCacher import RootDetectorCacher
from src.Core.Morphology.RootDetection.RootDetectorStackCacher import RootDetectorStackCacher
from src.Core.OSimUnrPipeline.PipelineProviderBase import PipelineProviderBase
from src.Core.Orthographic.NormalizedStringSimilarity.EditDistance import EditDistance
from src.Core.Segmentation.Tokenizers.ITokenizer import ITokenizer
from src.Core.Segmentation.Tokenizers.NLTKWhitespaceTokenizer import NLTKWhitespaceTokenizer
from src.Core.Segmentation.Tokenizers.TokenizerCacher import TokenizerCacher
from src.Core.WordNet.Classifiers.BlacklistedConceptsWordNetRelatednessFilterer import \
    BlacklistedConceptsWordNetRelatednessFilterer
from src.Core.WordNet.Classifiers.ConceptWiseWordNetRelatednessFilterer import ConceptWiseWordNetRelatednessFilterer
from src.Core.WordNet.Classifiers.DefinitionBasedRelatednessClassifier import DefinitionBasedRelatednessClassifier
from src.Core.WordNet.Classifiers.WordNetDerivationallyRelatedBinaryClassifier import \
    WordNetDerivationallyRelatedBinaryClassifier
from src.Core.WordNet.IWordNet import IWordNet, WordNetSimilarityAlgorithms, Lemma2SynsetMatching
from src.Core.WordNet.NLTKWordNetWrapper import NLTKWordNetWrapper
from src.Core.WordNet.WordPairDefinitionSourceFilter import WordPairDefinitionSourceFilter
from src.Core.WordSim.IWordSimilarity import IWordSimilarity
from src.Tools import Resources
from src.Tools.Logger import logp


class EnglishPipeline(PipelineProviderBase):

    def __init__(self, ctx: LinguisticContext, osimAlgorithm:IWordSimilarity):
        super().__init__(ctx, osimAlgorithm)

    def CreateWordNet(self):
        return NLTKWordNetWrapper()     #TODO: pass lang.

    def CreateWordSource(self):
        return NLTKWordNetWrapper()

    def CreateRootDetector(self):
        morpholex: MorphoLexSegmentedDataset = self._CreateMorphoLex()
        inflectional = self.CreateWordNet()
        from src.Core.Morphology.RootDetection.EnglishRootDetectionStack import EnglishRootDetectionStack
        stack: IRootDetectorStack = EnglishRootDetectionStack(inflectional, morpholex, lexiconPosFilter=None,
                                                              yieldOutOfLexiconRoots=True)  # We do not limit lexicon POS because it may have been derived from different POS.
        return RootDetectorStackCacher(stack)  # Note: StackCacher is not the same as Cacher! Stacks must be cached inside StackCacher.
        # return RootDetectorCacher(stack)
        # return stack  # No cache usage

    def CreateFastRootDetector(self):
        # stack: EnglishRootDetectionStack = CreateRootDetector()  # This is slow, but the cached root detector is used by multiple tasks: SharingRootDetector, DefinitionBased, etc.
        morpholex: MorphoLexSegmentedDataset = self._CreateMorphoLex()
        return RootDetectorCacher(morpholex)

    def _CreateMorphoLex(self) -> MorphoLexSegmentedDataset:
        txtpath: str = Resources.GetOthersPath("MorphoLEX2.txt")
        morpholex: MorphoLexSegmentedDataset = MorphoLexSegmentedDataset.LoadFromText(txtpath, loadMetadatas=True,                                                         caseSensitive=False)
        return morpholex

    def CreateTokenizer(self)->ITokenizer:
        tokenizer: ITokenizer = TokenizerCacher(NLTKWhitespaceTokenizer())
        return tokenizer

    def CreateWordSimilarityAlgorithm(self):
        sim = WordNetSimilarityAlgorithms.LCH
        logp("Algorithm '" + str(sim) + "' has been determined for Sim/Rel approx. for English.")
        return sim

    def CreateWordNetForSimilarity(self,wnSimAlg: WordNetSimilarityAlgorithms,
                                   l2s: Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations,
                                   wordSimPOSFilters: List[POSTypes] = None):
        return NLTKWordNetWrapper(algorithm=wnSimAlg, l2s=l2s, wordSimPOSFilters=wordSimPOSFilters)  # For now, we are producing a separate instance due to ctor params. It can be connected to WORDNET_EN.

    def CreateWordNetSimAlgorithm(self) -> WordNetSimilarityAlgorithms:
        sim = WordNetSimilarityAlgorithms.LCH
        logp("Algorithm '" + str(sim) + "' has been determined for Sim/Rel approx. for English.")
        return sim

    #region Filterings

    def CreateBlacklistedConceptsFilterer(self,pos):
        wn:IWordNet = self.CreateWordNet()
        bconcepts = ["ill_health.n.01", "disorder.n.01",
                     "pathologic_process.n.01",
                     "plant_part.n.01", "biological_group.n.01", "medical_procedure.n.01",
                     "animal.n.01", "microorganism.n.01", "plant.n.02",
                     "chemical.n.01", "drug.n.01", "body_substance.n.01", "vasoconstrictor.n.01",
                     # Food is also a substance.
                     "symptom.n.01"]  # Order is important! General -> specific.
        filterer: BlacklistedConceptsWordNetRelatednessFilterer = BlacklistedConceptsWordNetRelatednessFilterer(wn, bconcepts,pos)
        return filterer

    def CreateConceptPairFilterer(self, pos):
        # region RelatedConcepts
        rc = []
        rc.append(("religious_person.n.01",
                   "religion.n.01"))  # (both are very close; they score 1.5/10 with WUP.) e.g., wahhabi - wahhabism
        rc.append(("religious_person.n.01",
                   "theology.n.02"))  # | 1387 | jesuit [religious_person.n.01] | jesuitry [cognition.n.01]
        rc.append(("religion.n.01", "theology.n.02"))

        rc.append(("doctrine.n.01",
                   "general.n.01"))  # General and its ideology - caesar [living_thing.n.01] | caesaropapism [cognition.n.01]
        rc.append(
            ("body_part.n.01", "physical_condition.n.01"))  # adenohypophysis adenosis 6 - a disease of a body part
        rc.append(("cognitive_state.n.01", "cognition.n.01"))  # aesthesia chromesthesia 5
        rc.append(("nervous_disorder.n.01",
                   "cognition.n.01"))  # 208 | astereognosis [disorder.n.01] | gnosis [cognition.n.01]
        rc.append(("psychological_state.n.01",
                   "psychological_feature.n.01"))  # aesthesia chromesthesia 5 - cognition's subtype. While unnecessary in some cases, it's good for abstract matches! Note: psychological_feature is too low-level.

        rc.append(("sense.n.03", "paralysis.n.01"))  # akinesia kinesthesia 7 - slightly specific.
        rc.append(("organic_process.n.01",
                   "physical_condition.n.01"))  # agenesia [organic_process.n.01] akinesia [ill_health.n.01]
        rc.append(("reaction.n.03",
                   "sensitivity.n.01"))  # | 1399 | kinaesthesis [cognition.n.01] | kinesis [organic_process.n.01]
        rc.append(("anesthesia.n.01", "somesthesia.n.02"))  # acroanaesthesia kinaesthesia 5 (TOO SPECIFIC!)
        rc.append(("mechanics.n.01",
                   "proprioception.n.01"))  # | 1401 | kinesthetics [cognition.n.01] | kinetics [cognition.n.01]

        # Medicine
        rc.append(("plastic_surgery.n.01",
                   "plastic.n.01"))  # abdominoplasty [medical_procedure.n.01] | aminoplast [entity.n.01]
        rc.append(("body_part.n.01", "medical_procedure.n.01"))  # amygdala amygdalotomy 0.2
        rc.append(("body_part.n.01",
                   "diagnostic_procedure.n.01"))  # arteriography artery 8 - imaging techniques (like x-rays) have a health base. It's odd that it derives from psychological_feature, but that's the case.
        rc.append(("medical_procedure.n.01", "diagnostic_procedure.n.01"))
        rc.append(("health_professional.n.01",
                   "physical_condition.n.01"))  # Disease and its doctor -> anesthesia [entity.n.01] | anesthesiologist [entity.n.01]
        rc.append(("extravasation.n.03",
                   "physical_condition.n.01"))  # extravasation.n.03 might also fit under organic_process.
        rc.append(
            ("substance.n.07", "physical_condition.n.01"))  # nephroptosia [ill_health.n.01] | nephrotoxin [entity.n.01]
        rc.append(("medical_instrument.n.01", "diagnostic_procedure.n.01"))
        rc.append(("radiogram.n.02", "diagnostic_procedure.n.01"))
        rc.append(("medical_science.n.01", "treatment.n.01"))
        rc.append(("medical_science.n.01", "health_professional.n.01"))
        rc.append(("medical_science.n.01", "medical_procedure.n.01"))
        rc.append(("living_thing.n.01", "medical_procedure.n.01"))
        rc.append(("treatment.n.01", "dissolution.n.01"))

        rc.append(("body_part.n.01", "living_thing.n.01"))  # artiodactyl [animal.n.01] | dactyl [body_part.n.01]
        rc.append(("body_part.n.01",
                   "biological_group.n.01"))  # branchia [body_part.n.01] | branchiostegidae [biological_group.n.01]

        rc.append(("language.n.01", "country.n.01"))  # No specific example, but it might come up.
        rc.append(
            ("inhabitant.n.01", "language.n.01"))  # | 242 | bangla [language.n.01] | bangladeshi [living_thing.n.01]
        rc.append(("natural_language.n.01",
                   "geographical_area.n.01"))  # | 40 | hindostani [language.n.01] | hindustan [entity.n.01]

        # Animal
        rc.append(("animal.n.01", "animal_material.n.01"))  # | 1407 | lambkin [animal.n.01] | lambskin [entity.n.01]
        rc.append(("assay.n.04", "natural_science.n.01"))  # immunohistochemistry chemistry
        rc.append(
            ("zoolatry.n.01", "animal.n.01"))  # ichthyolatry [psychological_feature.n.01] | ichthyosaur [animal.n.01]
        rc.append(("zoolatry.n.01",
                   "biology.n.01"))  # | 1 | ichthyolatry [psychological_feature.n.01] | ichthyology [cognition.n.01]

        rc.append(("ill_health.n.01",
                   "organism.n.01"))  # Organisms causing disease - 298 | blastoma [ill_health.n.01] | blastomycete [living_thing.n.01]
        rc.append(("ill_health.n.01",
                   "cell.n.01"))  # Including all living beings causing diseases without generalizing to living_thing.
        rc.append(("ill_health.n.01", "cell.n.02"))  # Refers to the other "cell."
        rc.append(("discharge.n.03", "microorganism.n.01"))

        rc.append(("measure.n.02", "appraisal.n.01"))  # centilitre - centile
        rc.append(("unit_of_measurement.n.01", "measuring_instrument.n.01"))
        rc.append(
            ("fungus.n.01", "biological_group.n.01"))  # Initially living_thing, but it includes humans, so too broad.
        rc.append(("pathologic_process.n.01", "infestation.n.01"))  # | KEEP
        rc.append(("worm.n.01", "infestation.n.01"))  # | KEEP
        rc.append(("physics.n.01", "celestial_body.n.01"))
        rc.append(("legislation.n.02", "bad_person.n.01"))
        rc.append(("biology.n.01", "organic_process.n.01"))
        rc.append(("pathologic_process.n.01", "medical_instrument.n.01"))  # | KEEP
        rc.append(("symptom.n.01", "medical_instrument.n.01"))  # | KEEP
        rc.append(("infestation.n.01", "body_part.n.01"))  # | KEEP
        rc.append(("symptom.n.01", "body_part.n.01"))
        rc.append(("organic_process.n.01", "symptom.n.01"))
        rc.append(("dissolution.n.01", "occlusion.n.01"))

        rc.append(("electrical_device.n.01", "diagnostic_procedure.n.01"))
        rc.append(("sonograph.n.01", "radiography.n.02"))
        rc.append(("sonograph.n.01", "imaging.n.02"))
        rc.append(("graph.n.01", "photograph.n.01"))
        rc.append(("science.n.01", "scientist.n.01"))

        rc.append(("particle.n.02", "conduction.n.01"))
        # endregion

        wn: IWordNet = self.CreateWordNet()
        filterer = ConceptWiseWordNetRelatednessFilterer(wn, rc, pos)
        return filterer

    def CreateDefinitionBasedRelatednessClassifier(self, posFilter, rootDetector, fastRootDetector):
        minRootlength: int = 4  # OSimUnr study uses 4. It is a good value for English.
        typeDepthRatio = 0.4    # OSimUnr study uses 0.4. It is a good value for English.
        tokenizer: ITokenizer = TokenizerCacher(NLTKWhitespaceTokenizer())

        wn: IWordNet = self.CreateWordNet()
        definitionClassifier = DefinitionBasedRelatednessClassifier(
            WordPairDefinitionSourceFilter(wn, self.Context, POSTypes.NOUN, rootDetector, fastRootDetector, "entity.n.01"),
            tokenizer, minRootLength=minRootlength, typeDepthRatio=typeDepthRatio
        )  # Minimum root length is 4; matches words like drug-skin.
        # D5
        definitionClassifier.SkipMutualMeaningfulAffixes = False
        definitionClassifier.MeanindgfulPrefixes = ("hyper")  # Not prefixes: gastro, cyber, counter, electro, neuro.
        definitionClassifier.MeaningfulSuffixes = (
        "logy", "graphy", "culture", "pathy", "osis", "genesis", "phile", "phobia", "philia", "idae", "ogist", "otomy",
        "scopy", "geny")
        return definitionClassifier

    def CreateDerivationallyRelatedClassifier(self):
        return WordNetDerivationallyRelatedBinaryClassifier(self.CreateWordNet())

    #endregion