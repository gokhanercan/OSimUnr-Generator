from typing import List

from src.Core.Languages.LinguisticContext import LinguisticContext
from src.Core.Morphology.POSTypes import POSTypes
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
from src.Core.WordNet.WordPairDefinitionSourceFilter import WordPairDefinitionSourceFilter
from src.Core.WordSim.IWordSimilarity import IWordSimilarity
from src.Tools.Logger import logp




class TurkishPipeline(PipelineProviderBase):

    def __init__(self, ctx: LinguisticContext, osimAlgorithm:IWordSimilarity):
        super().__init__(ctx, osimAlgorithm)

    def CreateWordNet(self):
        raise NotImplementedError("Turkish WordNet is not included sur to deployment complexity.")

    def CreateWordSource(self):
        raise NotImplementedError("Turkish WordNet is not included sur to deployment complexity.")

    def CreateTokenizer(self):
        return TokenizerCacher(NLTKWhitespaceTokenizer())

    def CreateWordSimilarityAlgorithm(self):
        sim = WordNetSimilarityAlgorithms.WUP
        logp("Algorithm '" + str(sim) + "' has been determined for Sim/Rel approx. for Turkish.")
        return sim

    def CreateWordNetForSimilarity(self,wnSimAlg: WordNetSimilarityAlgorithms,
                                   l2s: Lemma2SynsetMatching = Lemma2SynsetMatching.HighestScoreOfCombinations,
                                   wordSimPOSFilters: List[POSTypes] = None):
        raise NotImplemented("TurkishWordNet is not implemented in this version.")

    def CreateWordNetSimAlgorithm(self) -> WordNetSimilarityAlgorithms:
        sim = WordNetSimilarityAlgorithms.WUP
        logp("Algorithm '" + str(sim) + "' has been determined for Sim/Rel approx. for English.")
        return sim

    #region Filterings
    def CreateBlacklistedConceptsFilterer(self, pos):
        bconcepts = ["organizma.n.02=TUR10-0590380", "mahluk.n.01=TUR10-0518540", "bitki.n.01=TUR10-0109420",
                     "patolojik durum.n.01=TUR10-1238570",
                     "kimyasal madde.n.01=TUR10-1240650", "vücut maddesi.n.01=TUR10-1217450"]
        # wn: IWordNet = GetOrCreateWORDNET_TR()
        filterer: BlacklistedConceptsWordNetRelatednessFilterer = BlacklistedConceptsWordNetRelatednessFilterer(wn,                                                                                         pos)
        return filterer

    def CreateConceptPairFilterer(self, pos):
        # region RelatedConcepts
        rc = []
        rc.append(("takson.n.01=TUR10-1223940",
                   "bitki.n.01=TUR10-0109420"))  # süsengiller [takson.n.01=TUR10-1223940]                      | sütleğengiller [bitki.n.01=TUR10-0109420]
        rc.append(("takson.n.01=TUR10-1223940",
                   "organizma.n.02=TUR10-0590380"))  # | 1518 | protoctista [takson.n.01=TUR10-1223940]                | protoktist [canlı.n.03=TUR10-0132550]
        rc.append(("mahluk.n.01=TUR10-0518540",
                   "sınıf.n.05=TUR10-0687130"))  # daha soyutları da verilebiliyor ama zorlamıyorum.
        rc.append(("hayvan sesi.n.01=TUR10-1222280", "mahluk.n.01=TUR10-0518540"))
        rc.append(("primat.n.01=TUR10-1208410", "insangiller.n.01=TUR10-1208440"))
        rc.append(("meyve-sebze.n.01=TUR10-1222970", "mahluk.n.01=TUR10-0518540"))

        rc.append(("tıp dalı.n.01=TUR10-1219730", "bilim.n.01=TUR10-0103020"))
        rc.append(("toplumsal grup.n.01=TUR10-1223790",
                   "alemdar.n.02=TUR10-0026380"))  # metropol [örgüt.n.01=TUR10-0770410]                          | metropolit [şahıs.n.02=TUR10-0721020]
        rc.append(("işadamı.n.01=TUR10-1231380",
                   "meslek.n.01=TUR10-0538220"))  # lastikçi [şahıs.n.02=TUR10-0721020]                          | plastikçilik [psikolojik özellik.n.01=TUR10-1246180]         | KEEP
        rc.append(("çalışan.n.01=TUR10-0985770", "iş.n.02=TUR10-0383950"))
        rc.append(("ekonomik süreç.n.01=TUR10-1236540",
                   "sahip olunan şey.n.01=TUR10-1195790"))  # |  866 | istihkak [psikolojik özellik.n.01=TUR10-1246180]       | istihlak [süreç.n.01=TUR10-0716680]                    | KEEP                                 |
        rc.append(("çalışan.n.01=TUR10-0985770",
                   "görev.n.03=TUR10-0264770"))  # | 1405 | muhasip [şahıs.n.02=TUR10-0721020]                     | muhtesip [varlık.n.02=TUR10-0814560]                   | KEEP                                 |

        rc.append(("yerli.n.04=TUR10-0851000",
                   "ekip.n.02=TUR10-0238540"))  # nationality hatasını çözüyor. kazakistanlı [örgüt.n.01=TUR10-0770410]                      | pakistanlı [canlı.n.03=TUR10-0132550]
        rc.append(("yerli.n.04=TUR10-0851000", "bölge.n.01=TUR10-0444290"))  #
        rc.append(("yerli.n.04=TUR10-0851000", "dil.n.02=TUR10-0512360"))  #
        rc.append(("bölge.n.01=TUR10-0444290", "dil.n.02=TUR10-0512360"))
        rc.append(("belde.n.02=TUR10-0090350", "belediye.n.01=TUR10-0090390"))
        rc.append(("idari birim.n.02=TUR10-1225490", "belde.n.02=TUR10-0090350"))
        rc.append(("ulam.n.01=TUR10-0467660",
                   "akran.n.01=TUR10-0116380"))  # dildaş [varlık.n.02=TUR10-0814560]                     | dindaş [şahıs.n.02=TUR10-0721020]
        rc.append(("idari bölge.n.01=TUR10-1225740", "şehir.n.01=TUR10-0441470"))

        rc.append(("veri işleme.n.01=TUR10-1236440", "problem çözme.n.01=TUR10-1218950"))
        rc.append(("buluş.n.02=TUR10-0123850",
                   "zihinsel işleme.n.01=TUR10-1246200"))  # ihtira [nesne.n.01=TUR10-0729480]                            | ihtiraz [psikolojik özellik.n.01=TUR10-1246180]
        rc.append(("ölçüm.n.02=TUR10-0601010", "ölçüm aleti.n.01=TUR10-1213780"))
        rc.append(("ölçümleme.n.01=TUR10-0601030", "ölçüm aleti.n.01=TUR10-1213780"))
        rc.append(("navigatör.n.01=TUR10-1186030", "navigasyon.n.01=TUR10-1186040"))

        rc.append(("malzeme.n.01=TUR10-0522720", "kayaç.n.01=TUR10-0431870"))
        rc.append(("molekül.n.01=TUR10-0549590", "fizyolojik durum.n.01=TUR10-1238470"))

        rc.append(("savunucu.n.01=TUR10-0669750",
                   "yüksek bilişsel süreç.n.01=TUR10-1246360"))  # ideoloji:  devrimcilik [canlı.n.03=TUR10-0132550]                       | evrimcilik [psikolojik özellik.n.01=TUR10-1246180]
        rc.append(("inanç.n.01=TUR10-0372440", "din.n.01=TUR10-0211370"))
        rc.append(("savunucu.n.01=TUR10-0669750", "yönelim.n.03=TUR10-0860760"))
        rc.append(("zihinsel birikim.n.01=TUR10-1218960", "münevver.n.01=TUR10-0562610"))

        rc.append(("değişim.n.01=TUR10-0188350", "doğal fenomen.n.01=TUR10-1246350"))
        rc.append(("mekanik olgu.n.01=TUR10-1233290", "yer değişikliği.n.01=TUR10-1197130"))

        rc.append(("müzik.n.02=TUR10-0567430", "müzik aleti.n.01=TUR10-1214020"))

        rc.append(("patolojik durum.n.01=TUR10-1238570",
                   "organ.n.01=TUR10-0805830"))  # menisk [organ.n.01=TUR10-0805830]                            | menisküs
        rc.append(("tedavi.n.01=TUR10-0755730", "patolojik durum.n.01=TUR10-1238570"))
        rc.append(("bozukluk.n.01=TUR10-0118140", "patolojik durum.n.01=TUR10-1238570"))
        rc.append(("bozukluk.n.01=TUR10-0118140", "tedavi.n.01=TUR10-0755730"))
        rc.append(("cerrahi müdahale.n.01=TUR10-0589000", "patolojik durum.n.01=TUR10-1238570"))
        rc.append(("cerrahi müdahale.n.01=TUR10-0589000", "organ.n.01=TUR10-0805830"))
        rc.append(("fizyolojik durum.n.01=TUR10-1238470",
                   "mineral.n.01=TUR10-0546710"))  # |  476 | dermatit [fizyolojik durum.n.01=TUR10-1238470]         | hematit [madde.n.01=TUR10-0516010]
        rc.append(("fizyolojik durum.n.01=TUR10-1238470", "biyolojik süreç.n.01=TUR10-1236690"))
        # endregion

        wn: IWordNet = self.CreateWordNet()
        filterer = ConceptWiseWordNetRelatednessFilterer(wn, rc, pos)
        return filterer

    def CreateDefinitionBasedRelatednessClassifier(self, posFilter, rootDetector, fastRootDetector):
        minRootlength: int = 4  # OSimUnr study uses 4. It is a good value for English.
        typeDepthRatio = 0.4  # OSimUnr study uses 0.4. It is a good value for English.
        tokenizer: ITokenizer = TokenizerCacher(NLTKWhitespaceTokenizer())

        wn: IWordNet = self.CreateWordNet()
        definitionClassifier = DefinitionBasedRelatednessClassifier(
            WordPairDefinitionSourceFilter(wn, self.Context, POSTypes.NOUN, rootDetector, fastRootDetector,
                                           "varlık.n.02=TUR10-0814560"),
            tokenizer, minRootLength=minRootlength, typeDepthRatio=typeDepthRatio
        )
        # D5
        definitionClassifier.SkipMutualMeaningfulAffixes = False
        definitionClassifier.MeaningfulSuffixes = ("oloji", "grafi", "metri", "metre")
        definitionClassifier.MeaningfulPrefixes = ("elektr", "nükleo", "karbo")
        return definitionClassifier

    def CreateDerivationallyRelatedClassifier(self):
        return WordNetDerivationallyRelatedBinaryClassifier(self.CreateWordNet())
    #endregion
