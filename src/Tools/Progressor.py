# coding=utf-8
from datetime import timedelta, time
from typing import Optional
from timeit import default_timer as timer
from src.Tools.Logger import logpif, logp


class Progressor(object):
    """
    Uses the same schema as Logger but measures the time elapsed between the previous iteration and estimates the duration.
    """

    def __init__(self, expectedIteration:int=None, reportRemaniningTime:bool = True, reportElapsedTime:bool = False) -> None:
        """
        :param expectedIteration: If this expected value is not given, it cannot perform percentage estimation.
        :param reportRemaniningTime:
        :param reportElapsedTime:
        """
        super().__init__()
        self.StartTime = None
        self.ReportRemainingTime = reportRemaniningTime
        self.ReportElapsedTime = reportElapsedTime
        self.ExpectedIteration = expectedIteration

    def logpif(self, iter:int, iterstr:str = "iter", progressBatchSize:int = None, anyMode:bool=True)->Optional[float]:
        """
        Logs the progress according to the fixed ProgressBatchSize.
        :param anyMode: If True, it logs in every mode.
        :param iter: iteration index
        :param expectedIter: Total number of iterations expected. If given, the logger also reports the percentage.
        :param progressBatchSize: Logs in batches of this size. If not given, the global default=10
        :return:
        """
        if (self.StartTime is None): self.StartTime = timer()
        perc:float = logpif(iter,iterstr,self.ExpectedIteration,progressBatchSize,anyMode)
        if (perc):
            #Record for estimation
            if (self.ExpectedIteration):
                if(perc > 0): self._ReportRemaningTime(perc, anyMode)
            return perc
        return None

    def _ReportRemaningTime(self, perc:float, anyMode):
        now = timer()
        duration = now - self.StartTime
        estimation = (100 * duration / perc) - duration
        if(self.ReportElapsedTime):     logp("Took:      " + timedelta(seconds=duration).__str__(), anyMode)
        if(self.ReportRemainingTime):   logp("Remaining: " + timedelta(seconds=estimation).__str__(), anyMode)

