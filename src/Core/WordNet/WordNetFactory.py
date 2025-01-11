from src.Core.Languages.LinguisticContext import LinguisticContext
from src.Core.WordNet.NLTKWordNetWrapper import NLTKWordNetWrapper


class WordNetFactory:
    
    def __init__(self,ctx:LinguisticContext) -> None:
        super().__init__()
        self.Context:LinguisticContext = ctx

    def CreateWordNet(self):
        if(self.Context.Language.Code == "eng"):
            return NLTKWordNetWrapper()
        elif(self.Context.Language.Code == "tr"):
            # trwn = TurkishWordNetServiceProxy()  #Disabled in the open source version. This is a Java wrapper.
            raise NotImplemented("Turkish provider is not implemented.")
        else:
            raise NotImplemented("lang not supported: " + self.Context.Language.Code)