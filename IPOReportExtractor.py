#-*- coding: utf8 -*-
__author__ = 'ligenjian'

import unittest
import re
import os
import json
import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Chapter:

    def __init__(self, totalContent, nameStart, nameEnd):
        #self.title = totalContent[nameStart: nameEnd]
        self.title = totalContent[nameStart: nameEnd].split('、')[1]
        self.totalcontent = totalContent
        self.nameStart = nameStart
        self.nameEnd = nameEnd

    def extractContent(self, nextPoint):
        self.content = self.totalcontent[self.nameEnd: nextPoint]
        return self.content


class IPOReportExtractor:

    def __init__(self):
        pass

    def openDocument(self, filename, path = './'):

        if path[-1] == '/':
            filePath = path
        else:
            filePath = path + '/'
        prevName = filename.split('.')[0]
        if not os.path.isfile(filePath + prevName + '.txt' ):
            os.system('pdf2txt.py ' + filePath + prevName + '.pdf > ' + filePath + prevName + '.txt')
        self.fp = codecs.open(filePath + prevName + '.txt', encoding='utf-8')
        self.content = ''.join(self.fp.readlines())
        self.prevName = prevName
        #print self.content:

    def documentContent(self):

        return self.content

    def riskContent(self):

        riskNav = re.compile(u'^\s*第四[章节].*风险因素', re.MULTILINE)
        riskMatch = riskNav.finditer(self.documentContent())
        i= 0
        for match in riskMatch:
            i += 1
            if i == 2:
                riskMatch = match
                #print self.documentContent()[riskMatch.start(): riskMatch.end()]

        founderNav = re.compile(u'^\s*第五[章节].*发行人基本情况', re.MULTILINE)
        founderMatch = founderNav.finditer(self.documentContent())

        i = 0
        for match in founderMatch:
            i += 1
            if i == 2:
                founderMatch = match
                #print self.documentContent()[founderMatch.start(): founderMatch.end()]

        riskContent = self.documentContent()[riskMatch.start(): founderMatch.end()]
        return self.documentContent()[riskMatch.end(): founderMatch.start()]

    def chapterSplit(self,content):
        chapterNav = re.compile(u'^\s*[一二三四五六七八九十]+、.*', re.MULTILINE)
        chapterList = []
        for chapterMatch in chapterNav.finditer(content):
            chapterList.append(Chapter(content, chapterMatch.start(), chapterMatch.end()))
        for i in range(0,len(chapterList)-1):
            chapterList[i].extractContent(nextPoint = chapterList[i+1].nameStart)
        chapterList[-1].content = content[chapterList[-1].nameEnd:]
        self.chapterList = chapterList
        for chapter in chapterList:
            chapter.content = ''.join(re.split('\s', chapter.content))
        return chapterList

    def riskMapper(self):

        riskMap = {}
        for chapter in self.chapterList:
            riskMap[chapter.title] = chapter.content
        self.riskMap = riskMap
        #for key in riskMap:
            #print 'title:', key
            #print 'content:', riskMap[key]
        return riskMap

    def jsonDump(self):
        fileName = self.prevName + '.json'
        fp = open(fileName, 'w+b')
        jsonContent = json.dumps(self.riskMapper(),ensure_ascii=False).decode('utf-8')
        fp.write(jsonContent)
        return jsonContent

    def processFile(self, fileName):
        self.openDocument(fileName)
        self.chapterSplit(self.documentContent())
        #print self.jsonDump()


class TestIPOReportExtractor(unittest.TestCase):

    def setUp(self):
        self.ipoExtractor = IPOReportExtractor()
        self.ipoExtractor.openDocument('H2_AN201401070004912270_1.pdf')

    def testFullDocument(self):
        assert len(self.ipoExtractor.documentContent()) > 0

    def testPageNumber(self):
        assert len(self.ipoExtractor.riskContent()) > 0

    def testChapterSplit(self):
        riskContent = self.ipoExtractor.riskContent()
        self.ipoExtractor.chapterSplit(riskContent)

    def testRiskMap(self):
        riskContent = self.ipoExtractor.riskContent()
        chapters = self.ipoExtractor.chapterSplit(riskContent)
        self.ipoExtractor.riskMapper()
        self.ipoExtractor.jsonDump()

    def testProcessFile(self):
        ipoExtractor = IPOReportExtractor()
        ipoExtractor.processFile('P020120406524008592384.pdf')

if __name__ == '__main__':
    unittest.main()