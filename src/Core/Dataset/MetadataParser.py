# coding=utf-8
from typing import Dict
from unittest import TestCase
from src.Tools import StringHelper

class MetadataParser(object):
    """
    Allows parsing metadata defined in the first line of each file after the # sign, independent of task and data.
    """
    def ParseMetaHeader(self, line:str) ->Dict[str,str]:
        if(StringHelper.IsNullOrEmpty(line)): return {}
        if(line[0] != "#"): raise Exception("Not a meta header: '" + line + '"')
        eline = line[1:]
        metadatas:Dict[str,str] = {}
        attrs = eline.split('|')
        if(attrs.__len__() == 0): return {}
        for attr in attrs:
            keyvalpair = attr.strip().split('=')
            metadatas[keyvalpair[0]] = keyvalpair[1]
        return metadatas

class MetadataParserTest(TestCase):

    def test_ParseMetaHeader_Empty_ReturnEmptyHeaders(self):
        self.assertEqual(0, MetadataParser().ParseMetaHeader("").__len__())

    def test_ParseMetaHeader_MultipleAttrWithBlanks_Parse(self):
        metas = MetadataParser().ParseMetaHeader("#Scale=0-10 | Size=500")
        self.assertEqual("0-10",metas["Scale"])
        self.assertEqual("500",metas["Size"])

    def test_ParseMetaHeader_SingleAttr_Parse(self):
        self.assertEqual("0-10",MetadataParser().ParseMetaHeader("#Scale=0-10")["Scale"])
