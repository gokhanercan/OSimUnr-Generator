import random, string
import re
from functools import reduce
from typing import Optional
from unittest import TestCase

#References:
# https://docs.python.org/3/library/stdtypes.html#str.isalnum

def FindFirstBlockInBetweenOrDefault(value: str, firstBlock: str, endingBlock: str, default:str="") -> str:
    """
    Returns the first string block between the given blocks, or the given default value if not found.
    :param value:
    :param firstBlock:
    :param endingBlock:
    :param default:
    :return:
    """
    block = FindFirstBlockInBetween(value,firstBlock,endingBlock)
    if(block is None): return default
    return block

def FindFirstBlockInBetween(value: str, firstBlock: str, endingBlock: str) -> Optional[str]:
    """
    Returns the first block found between the given blocks.
    :param value:
    :param firstBlock:
    :param endingBlock:
    :return: Returns None if not found.
    """
    try:
        firstLeftIndex:int = value.index(firstBlock) + len(firstBlock)-1
        firstEndingIndex:int = value.index(endingBlock,firstLeftIndex+1)
        if (firstEndingIndex >= 0 and firstEndingIndex >= 0):
            return value[firstLeftIndex+1:firstEndingIndex]
    except ValueError:
        return None

def FindIntAfterStringOrDefault(value: str, firstBlock: str, default:int=None) -> int:
    pattern = firstBlock + "([+-]?[0-9]\d*|0)"
    r = re.search(pattern, value)
    if (r is None): return default
    return int(r.group(1))

def RemoveLastChar(value:str):
    return value[:-1]

def RemoveLastCharIf(value:str, chr)->str:
    """
    Removes the last character if it matches the given character.
    :param value:
    :param chr:
    :return:
    """
    if (value[len(value)-1] == chr): return value[:-1]
    return value

def RemoveFirstCharIf(value:str, chr)->str:
    """
    Removes the first character if it matches the given character.
    :param value:
    :param chr:
    :return:
    """
    if (value[0] == chr): return value[1:]
    return value

_HasAnyNumberCompiled = None
def HasAnyNumber(value:str)->bool:
    """
    Checks if there is at least one digit in the text.
    :param value:
    :return:
    """
    global _HasAnyNumberCompiled
    if(_HasAnyNumberCompiled is None): _HasAnyNumberCompiled = re.compile(r'\d')
    return bool(_HasAnyNumberCompiled.search(value))

BOOLEANS_TRUE = frozenset(('y', 'yes', 'on', '1', 'true', 't','var','evet', 1, 1.0, True))
BOOLEANS_FALSE = frozenset(('n', 'no', 'off', '0', 'false', 'f','yok','hayır', 0, 0.0, False))
BOOLEANS = BOOLEANS_TRUE.union(BOOLEANS_FALSE)

"modified from: https://raw.githubusercontent.com/ansible/ansible/2bd6b1415b9131c3a7cb13724f5d31bb0d33846b/lib/ansible/module_utils/parsing/convert_bool.py"
def ToBool(value, strict=True):
    if isinstance(value, bool):
        return value

    normalized_value = value
    if isinstance(value, str):
        normalized_value = str(value).lower().strip()

    if normalized_value in BOOLEANS_TRUE:
        return True
    elif normalized_value in BOOLEANS_FALSE or not strict:
        return False

    raise TypeError("The value '%s' is not a valid boolean.  Valid booleans include: %s" % (str(value), ', '.join(repr(i) for i in BOOLEANS)))

def BoolToStr(value:bool)->str:
    return "1" if value else "0"

def IsNullOrEmpty(str)->bool:
    """
    Instead of this Helper, you can check the string with not.
    :param str:
    :return:
    """
    #https://stackoverflow.com/questions/9573244/most-elegant-way-to-check-if-the-string-is-empty-in-python
    return not str

def GenerateRandomStr(length:int = 8, lowerCase = False):
    letters = string.ascii_lowercase if lowerCase else string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

def Coelesce(*arg):
    """
    Modified to pass empty strings too
    ref: https://stackoverflow.com/questions/4978738/is-there-a-python-equivalent-of-the-c-sharp-null-coalescing-operator
    :param str:
    :param arg:
    :return:
    """
    return reduce(lambda x, y: x if not IsNullOrEmpty(x) else y, arg)

class StringHelperTest(TestCase):

    def test_FindFirstBlockInBetweenOrDefault_SingleBlock_Return(self):
        self.assertEqual("(whisper)",FindFirstBlockInBetweenOrDefault("{(whisper)}>er>","{","}"))

    def test_FindFirstBlockInBetweenOrDefault_NoMatching_ReturnTheDefault(self):
        self.assertEqual("default",FindFirstBlockInBetweenOrDefault("last-middle-first","first","last","default"))

    def test_FindFirstBlockInBetween_SingleBlockAndEndingBlockAreBiggerThanOneChar_ReturnFirstBlock(self):
        self.assertEqual("middle",FindFirstBlockInBetween("f-middle-ending","f-","-ending"))

    def test_FindFirstBlockInBetween_SingleBlockAndBeginningBlockIsBiggerThanOneChar_ReturnFirstBlock(self):
        self.assertEqual("3+6+se",FindFirstBlockInBetween("Exp2001-FastText-win100-dim100-ns5-hs0-del0-mean1-iter5-root0-inf0-seg-ngr[3+6+se]__PolyglotWikiEN13YuzBinLCNP.vec","ngr[","]"))

    def test_FindFirstBlockInBetween_MultipleBlocks_ReturnFirstBlock(self):
        self.assertEqual("gokhan",FindFirstBlockInBetween("(gokhan)(ercan)","(",")"))

    def test_FindFirstBlockInBetween_NoMatching_ReturnNone(self):
        self.assertIsNone(FindFirstBlockInBetween("(gokhan)(ercan)",".","-"))

    def test_FindFirstBlockInBetween_SameBlockFromBegiggingAndEnding_LookFor2ndMatchForEndingBlock(self):
        self.assertEqual("gokhan",FindFirstBlockInBetween("<gokhan<ercan","<","<"))

    def test_RemoveLastCharIf_SameChar_Remove(self):
        self.assertEqual("gokhan",RemoveLastCharIf("gokhan+",'+'))

    def test_RemoveLastCharIf_AnotherChar_Remove(self):
        self.assertEqual("gokhan-",RemoveLastCharIf("gokhan-",'+'))

    def test_RemoveFirstCharIf_SameChar_Remove(self):
        self.assertEqual("gokhan",RemoveFirstCharIf("_gokhan",'_'))

    def test_RemoveFirstCharIf_AnotherChar_Remove(self):
        self.assertEqual("+gokhan",RemoveFirstCharIf("+gokhan",'_'))

    def test_HasAnyNumber_HasNumber_ReturnTrue(self):
        self.assertEqual(True,HasAnyNumber("DASDASDA1"))
        self.assertEqual(True,HasAnyNumber("1dasdasdasdas"))
        self.assertEqual(True,HasAnyNumber("3434234343"))
        self.assertEqual(True,HasAnyNumber("1"))

    def test_HasAnyNumber_DoesNotHaveNumber_ReturnFalse(self):
        self.assertEqual(False,HasAnyNumber("GÖKHANÖŞİĞÜ"))
        self.assertEqual(False,HasAnyNumber("gokhan"))
        self.assertEqual(False,HasAnyNumber( "-*,ü;.%&/(%" ))
        self.assertEqual(False,HasAnyNumber( "bir one" ))

    def test_Coelesce_PassNones(self):
        self.assertEqual("Null",Coelesce(None,"Null",None))
    def test_Coelesce_ChooseFirstStr(self):
        self.assertEqual("Str1",Coelesce("Str1","Str2"))
    def test_Coelesce_PassEmpties(self):
        self.assertEqual("Str2",Coelesce("","","Str2","Str3","","None"))     #this cases is implemented customl

