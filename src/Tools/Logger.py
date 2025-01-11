import sys
from datetime import datetime

#anyMode logs in every mode regardless of Debug/Release mode.
from typing import Optional

from src.Tools import FormatHelper


def logp(msg:str, anyMode:bool = False):
    """
    Abbreviation of LogProgress
    :param msg:
    :param anyMode: If True, logs in every mode.
    :return:
    """
    if(not anyMode and not IsInDebug()): return
    _printWithTime(msg)

def logl(msg:str, label:str = "", anyMode:bool = False):
    """
    LogLabel: Information printed to the console in every mode for tracing. Disabled in debug mode.
    :param msg:
    :param label:
    :param anyMode:
    :return:
    """

    if(not anyMode and not IsInDebug()): return
    if(label is not ""): label = label + ": "
    _printWithTime(label + msg)

def log(any, anyMode:bool = False):
    """
    Standard log request.
    :param any:
    :param anyMode:
    :return:
    """
    if(not anyMode and not IsInDebug()): return
    _printWithTime(str(any))

_VerboseMode:bool = False       #Verbose mode.
def logv(any):
    """
    Logging in verbose mode. This means the developer using this does not want to inflate the log too much in every case.
    This mode only works in debug mode.
    :param any:
    :return:
    """
    if(not IsInDebug()): return
    global _VerboseMode
    if(not _VerboseMode): return
    _printWithTime(str(any))

def printArray(arr, arrayName, anyMode:bool = False):
    if(not anyMode and not IsInDebug()): return
    print("\n " + "array" +": " + arrayName)
    print(arr)
    print(arr.shape)


def logpif(iter:int, iterstr:str = "iter", expectedIter:int = 100, progressBatchSize:int = 10, anyMode=True, humanize:bool=True)->Optional[float]:
    """
    Logs the progress according to the given progressBatchSize (default:10).
    :param iter: iteration index
    :param expectedIter: Total number of iterations expected. If given, the logger also reports the percentage. If not given (or 0), it only reports the iteration in BatchSize. Default: 100s
    :param progressBatchSize: Logs in batches of this size. If not given, the global default=10
    :param humanize: If not calculating percentage, prints the increasing iteration numbers in human readable format like K M B.
    :return:
    """
    effBatchSize = 10 if (progressBatchSize is None or progressBatchSize<=0) else progressBatchSize     #10 default
    if((iter % effBatchSize) == 0):
        msg = ""
        perc:float = None

        if(expectedIter is not None):
            if(expectedIter > 0):
                perc = round(iter/expectedIter*100,2) if expectedIter is not None else None
                valStr = str(iter) if perc is None else str(iter) + "/" + str(expectedIter) + " ("+str(perc)+"%)"
                msg:str = iterstr + ": " + valStr
        else:       #No estimation exits
            msg = iterstr + ": " + FormatHelper.Humanize(iter) if humanize else str(iter)

        logp(msg,anyMode)
        return perc
    return None

_DebugSet:bool = False
_Debug:bool = False
def IsInDebug()->bool:          #Checking the debug with sys.gettrace() is not working with Cython. Therefore, we manually inject debug mode from the main script.
    global _Debug
    global _DebugSet
    if(_DebugSet):
        return _Debug
    else:
        # set debug global var. for the first time.
        t = sys.gettrace()    #It checks whether the #PyCharm debugger is attached.
        if (t is None):
            _Debug = False
            print("Debugger is not attached. _Debug=False")
        else:
            print("Debugger is attached. _Debug=True.")
            _Debug = True
        _DebugSet = True
        return _Debug

def _printWithTime(finalmsg:str):
    now = datetime.now()
    print(now.strftime("%H:%M:%S") + ": " + finalmsg)