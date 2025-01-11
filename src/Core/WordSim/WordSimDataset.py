# coding=utf-8
import unittest
from operator import index
from typing import List, Optional, Dict, Tuple
from unittest import TestCase
from pandas import DataFrame

from src.Core.Dataset.Dataset import Dataset
from src.Core.Dataset.DiscreteScale import DiscreteScale
from src.Core.Dataset.MetadataParser import MetadataParser
from src.Core.Languages.Grammars.IGrammar import IGrammar
from src.Core.Languages.LinguisticContext import LinguisticContext
from src.Core.WordPair import WordPair
from src.Core.WordSim.IWordSimilarity import IWordSimilarity
from src.Tools import Resources
from src.Tools.Logger import logp


class WordSimDataset(Dataset, IWordSimilarity):

    def __init__(self, filename:str=None, fullPath:str = None, linguisticContext:LinguisticContext=None, scale:DiscreteScale=None) -> None:
        """
        :param filename: To load directly from WordSim files.
        :param fullPath: To load by giving an absolute address. If FullPath is given, it is used.
        """
        super().__init__()
        self.Filename = filename
        self.FullPath = fullPath
        self.Wordpairs:List[WordPair] = []
        self._WPIndex:Dict[str,WordPair] = {}  #WpKey,WordPair
        self.Name:str = filename
        if(scale is None): scale = DiscreteScale(0,10)      #default
        self.Scale:DiscreteScale = scale
        self.LinguisticContext = linguisticContext
        self.GoldSimilarityColumn = "GoldSimilarity"     # Which column should be used for IWordSimilarity evaluations as ground truth for this dataset!

    def _IndexWordpairs(self):
        for wp in self.Wordpairs:
            wpkey = wp.ToKey()
            self._WPIndex[wpkey] = wp

    def LoadWithWordPairs(self, wordpairs:List[WordPair]):
        self.Wordpairs = wordpairs
        self._IndexWordpairs()

    def Persist(self, newPath, metaScale:DiscreteScale = None):
        """
        :param metaScale: Marks the given scale when saving, regardless of the dataset's scale.
        :param newPath:
        :return:
        """
        index:int = 0
        if (len(self.Wordpairs) == 0):
            logp("WARNING! - Wordpairs is set is empty. Nothing to save!",True)
            return

        # Get Schema from the first record. - If it exists in the first record, we assume it exists in the others as well.
        wpFirst = self.Wordpairs[0]
        attrs = vars(wpFirst)
        simColumns:List[str] = []
        simAttrs:List[str] = []
        for attr in attrs:
            if (attr == "GoldSimilarity"): continue
            if attr.__contains__("Similarity"):
                simColumns.append(attr.replace("Similarity","").lower())
                simAttrs.append(attr)

        # Iterate and save
        index = 0
        line:str = ""
        with open(newPath,mode="w+",encoding="utf-8",errors='ignore',) as wr:
            # Header
            header = "w1\tw2\tgold"
            colIndex = 0
            for simColumn in simColumns:
                header = header + "\t" + str(simColumn)
                colIndex += 1
            header = header + "\tNote"     #wp.Note column
            wr.write(header + "\n")

            for wp in self.Wordpairs:
                # Core
                line = wp.Word1 + "\t" + wp.Word2 + "\t" + ("" if wp.GoldSimilarity is None else str(wp.GoldSimilarity))

                # From Other
                colIndex = 0
                for simColumn in simColumns:
                    try:
                        line = line +"\t" + str(wp.__getattribute__(simAttrs[colIndex]))
                        colIndex += 1
                    except Exception as ex:
                        print("An exception occurred: " + str(ex))

                if wp.Note is not None:     # Wp.Note column
                    line = line + "\t'" + wp.Note + "'"        # There should be no special characters in Note!

                index += 1
                wr.write(line + "\n")

        # Add Headers
        effScale = metaScale if metaScale else self.Scale
        if(effScale):
            lines = None
            with open(newPath,encoding="utf-8",errors='ignore') as fp:
                lines = fp.readlines()
            with open(newPath,mode="w+",encoding="utf-8",errors='ignore',) as wr:
                wr.write("#Scale=" + str(effScale.Min) +"-" + str(effScale.Max) + "\n")
                for line in lines:
                    wr.write(line)
        logp("Dataset kaydedildi. Path: " + newPath)

    def ToWSQuestExcel(self, excelFilePath:str):
        """
        Converts to WordSimQuest Excel format.
        :return:
        """
        df:DataFrame = DataFrame()
        index:int = 1
        dsSize:int = len(self.Wordpairs)
        for wp in self.Wordpairs:
            df.at[index,"W1"] = wp.Word1
            df.at[index, "W2"] = wp.Word2
            df.at[index, "Qtype"] = "Sim"
            index += 1
        for wp in self.Wordpairs:
            df.at[index,"W1"] = wp.Word1
            df.at[index, "W2"] = wp.Word2
            df.at[index, "Qtype"] = "Rel"
            index += 1
        df.to_excel(excelFilePath,sheet_name="Questions",columns=["W1","W2","Qtype"],index=True)

    def Load(self, autoLowerCase:bool=True):
        # Validate
        if(autoLowerCase and self.LinguisticContext is None): raise Exception("Cannot lowercase when LinguisticContext is null!")

        # Effective path
        path:str = None
        if (self.FullPath):
            path = self.FullPath
        else:
            path = Resources.GetWordSimilarityFile(self.Filename)

        # Load
        wordpairs, metadata = self.ReadWordPairs(path)
        grammar:IGrammar = self.LinguisticContext.BuildGrammar() if self.LinguisticContext else None
        for wp in wordpairs:
            if(autoLowerCase):
                wp.Word1 = grammar.ToLowerCase(wp.Word1)
                wp.Word2 = grammar.ToLowerCase(wp.Word2)
            self.Wordpairs.append(wp)
        self._IndexWordpairs()
        self.Scale = self.GetMetadataScaleOrDefault(metadata)
        return self

    def LoadScale(self):
        scale = self.ReadScale()
        self.Scale = scale

    def ReadScale(self):
        # Effective path
        path:str =None
        if (self.FullPath):
            path = self.FullPath
        else:
            path = Resources.GetWordSimilarityFile(self.Filename)

        wordpairs, metadata = self.ReadWordPairs(path, metadataOnly=True)
        return self.GetMetadataScaleOrDefault(metadata)

    @staticmethod
    def GetMetadataScaleOrDefault(metadata:Dict[str,str])->DiscreteScale:
        if (not metadata): return DiscreteScale()
        if(metadata.__len__() == 0): return DiscreteScale()
        scale:str = metadata.get("Scale")
        if(scale):
            segments = scale.split("-")
            return DiscreteScale(float(segments[0]),float(segments[1]))
        return DiscreteScale()

    def Name(self)->str:
        return self.Name

    @property
    def Size(self)->int:
        return len(self.Wordpairs)

    def __str__(self) -> str:
        return self.Name + " (" + str(self.Size) + ")"

    def __repr__(self) -> str:
        return self.__str__()

    #region IWordSimilarity
    def WordSimilarity(self, w1: str, w2: str) -> Optional[float]:
        wpq:WordPair = WordPair(w1,w2)
        qkey = wpq.ToKey()
        wp:WordPair = self._WPIndex.get(qkey)
        if(wp is None): return None
        return self.GetGoldValue(wp)

    def SimilarityScale(self) -> DiscreteScale:
        return self.Scale

    def GetSimilarityColumns(self)->List[str]:
        """
        Lists the Similarity columns that the dataset data has.
        :return:
        """
        if len(self.Wordpairs) == 0: raise Exception("Dataset should be loaded first to get that info!")
        wp = self.Wordpairs[0]      #Using the first instance
        columns = []
        for k,v in wp.__dict__.items():
            if(k.__contains__("Similarity")):
                columns.append(k)
        return columns

    def GetGoldSimilarityColumn(self):
        return self.GoldSimilarityColumn

    def SetGoldSimilarityColumn(self, simcol:str):
        simcols = self.GetSimilarityColumns()
        if not (simcol in simcols): raise Exception("Should be in the list: " + str(simcols))
        self.GoldSimilarityColumn = simcol

    def GetGoldValue(self, wp:WordPair):
        """
        Returns the sim/rel value according to the column marked as Gold in the dataset.
        :param wp:
        :return:
        """
        simType = self.GoldSimilarityColumn.replace("Similarity","")
        return wp.GetOtherSimilarity(simType)

    #endregion

    @staticmethod
    def ReadWordPairs(path:str, delimiter='\t', case_insensitive=False, minGoldSimilarity:float = None, maxGoldSimilarity = None, autoTrimWords:bool = False, metadataOnly:bool = False)->Tuple[List[WordPair], Dict[str,str]]:
        """
        Reads WordSim files from the filesystem.
        :param path:
        :param delimiter:
        :param case_insensitive:
        :param minGoldSimilarity: Min value filter.
        :param maxGoldSimilarity: If given, does not load word pairs with values greater than the given max value.
        :return:
        """
        wordpairs:List[WordPair] = []
        headerLine:str = None

        # Meta
        metaParse = MetadataParser()
        metadatas:Dict[str,str] = {}

        with open(path,encoding="utf-8",errors='strict') as fp:
            logp("Loading wordpair dataset into memory..." + path,True)
            lines = fp.readlines()
            scale:int = 10
            lineIndex = 0
            for line in lines:
                lineIndex += 1
                #print(lineIndex)
                if line.lower().startswith('#w1\t') or line.lower().startswith('w1\t'):       # skip header.
                    headerLine = line
                    continue
                # metaheaders
                elif (line.lower().startswith("#") and lineIndex <= 2):     # We only accept the header in the first 2 lines. We detect comments in other lines.
                    metadatas = metaParse.ParseMetaHeader(line)
                elif (line.lower().startswith("#")):        # Disabled word-pair     ex: #car automobile 5
                    continue
                else:
                    # Read WordPair
                    if(metadataOnly): continue      # Only get metadata and exit.
                    a:str = None
                    b:str = None
                    goldsimstr:str = None
                    index:int = 0
                    wp: WordPair = WordPair("","")
                    for col in line.split(delimiter):
                        col = col.replace("\r","").replace("\n","")
                        if (index == 0): a = col
                        if (index == 1): b = col
                        if (index == 2): goldsimstr = col
                        # Other sim columns

                        if (index > 2):
                            if (headerLine):                            # If there is no header, more than 3 columns cannot be loaded.
                                colName = headerLine.split(delimiter)[index].replace("\r","").replace("\n","")
                                if(colName.lower() == "note"):
                                    if(col is not None): wp.Note = col
                                else:
                                    attrName = colName + "Similarity"
                                    colval:float = float(col) if (col and col != 'None') else None
                                    wp.__setattr__(attrName,colval)
                                    if(colval is None): logp("'None' value for' " + attrName + "'. Line: " + line)
                        index += 1

                    # Format
                    sim_gold:float = float(goldsimstr) if(goldsimstr) else None
                    if(autoTrimWords):
                        a = a.strip()
                        b = b.strip()
                        if (case_insensitive):
                            a = a.upper()
                            b = b.upper()
                    wp.Word1 = a
                    wp.Word2 = b
                    wp.GoldSimilarity = sim_gold
                    # Filters
                    if (wp.GoldSimilarity):     # Apply filter if not empty
                        if(minGoldSimilarity):
                            if (wp.GoldSimilarity < minGoldSimilarity): continue
                        if(maxGoldSimilarity):
                            if (wp.GoldSimilarity > maxGoldSimilarity): continue
                    wordpairs.append(wp)

        # set metadatas
        logp("Loaded wordpairs from path: " + path + " ("+ str(len(wordpairs)) + " items)",True)
        return wordpairs, metadatas

    #region OOV

    def CountOOVs(self):
        """
        Count OOV flagged word-pairs in the dataset.
        :return:
        """
        oovs:int = 0
        for wp in self.Wordpairs:
            if(wp.IsOOV == True): oovs = oovs+1
        return oovs

    #endregion

    #region Merge

    @staticmethod
    def MergeDatasets(datasets, newName:str,scale:DiscreteScale, autoRemoveDuplicates:bool = True):
        """
        Merges datasets without removing duplicates
        :param self:
        :param datasets:
        :param newName:
        :return:
        """
        dsMerged:WordSimDataset = WordSimDataset(newName + ".csv", scale=scale)
        wpset = set()
        for ds in datasets:
            for wp in ds.Wordpairs:
                gold = wp.GoldSimilarity
                goldScaled:float = WordSimDataset.ApplyScaling(gold,ds.Scale,dsMerged.Scale)
                wpNew:WordPair = WordPair(wp.Word1, wp.Word2, goldScaled)
                key:str = wpNew.ToKey()
                if(not key in wpset):
                    dsMerged.Wordpairs.append(wpNew)
                    wpset.add(key)
        return dsMerged

    #endregion


class WordSimDatasetTest(TestCase):

    def test_MergeDatasets_MergeTwoWithDifferentScales_NoDuplicates(self):
        ds1 = WordSimDataset(scale=DiscreteScale(0,10))
        ds1.Wordpairs.append(WordPair("word1","word2",5))

        ds2 = WordSimDataset(scale=DiscreteScale(0, 5))
        ds2.Wordpairs.append(WordPair("word11", "word12", 2))
        ds2.Wordpairs.append(WordPair("word11", "word12", 2))       #duplicate

        merged:WordSimDataset = WordSimDataset.MergeDatasets([ds1,ds2],"merged",DiscreteScale(0,1))
        self.assertEqual(2, len(merged.Wordpairs))
        self.assertEqual(0.5, merged.Wordpairs[0].GoldSimilarity)
        self.assertEqual(0.4, merged.Wordpairs[1].GoldSimilarity)


if __name__ == '__main__':
    unittest.main()