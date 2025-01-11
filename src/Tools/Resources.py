import os
from pathlib import Path
from typing import Optional

from src.Tools.Logger import logp

"""
If we take the Gensim root folder as the root, it returns the folder according to the scripts running in that path.
"""
def GetRoot()->str:
    path = os.getcwd()
    return path

global _RootFolder
_RootFolder = None

def SetRootFolder(rootFolder:str):
    _RootFolder = rootFolder
def GetResourcesRoot()->str:
    global _RootFolder
    if(_RootFolder is not None):
        logp("Resources root folder is set to: " + str(_RootFolder),True)
        return str(_RootFolder)
    root:str = GetRoot()
    if(root.endswith("src") or root.endswith("test")):
         return str(Path(root).parent.joinpath("Resources"))
    else:
        return str(Path(root).joinpath("Resources"))
def GetResourcesSubFolder(subfolder:str)->str:
    return str(Path(GetResourcesRoot()).joinpath(subfolder))

def GetWordSimilarityRoot()->str:
    return str(Path(GetResourcesSubFolder("Evaluation")).joinpath("WordSimilarity"))
def GetWordSimilarityFile(filename)->str:
    return str(Path(GetWordSimilarityRoot()).joinpath(filename))

def GetStudiesRoot()->str:
    return GetResourcesSubFolder("Studies")
def GetStudyPath(studyName)->str:
    return str(Path(GetStudiesRoot()).joinpath(studyName))

def GetOthersRoot()->str:
    return GetResourcesSubFolder("Others")
def GetOthersPath(filename:str)->str:
    return str(Path(GetOthersRoot()).joinpath(filename))
