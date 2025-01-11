class Language(object):

    def __init__(self, code:str, name:str = None) -> None:
        super().__init__()
        self.Code = code
        self.Name = name

    def __str__(self) -> str:
        return (self.Name or "") + " (" + self.Code + ")"
