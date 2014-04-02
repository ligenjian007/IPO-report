__author__ = 'ligenjian'

import IPOReportExtractor
import re
import os
import pymongo

connection = pymongo.Connection('localhost', 27017)
db = connection.risk_database
collection = db.risk_collection

pdfMatcher = re.compile(r'.*\.txt')

numParsed = 0
numError = 0

for filename in os.listdir('/home/ligenjian/Downloads/pass'):
    if pdfMatcher.match(filename):
        try:
            ipoExtractor = IPOReportExtractor.IPOReportExtractor()
            riskMap = ipoExtractor.processFile(filename, '/home/ligenjian/Downloads/pass')
            if filename.split('_')[0] == '1':
                passed = True
            else:
                passed = False
            collection.insert({'corporation_number':filename.split('.')[0], 'risk_content' : riskMap, 'passed':passed})
            numParsed += 1
            print 'we have parsed ',numParsed, ' files'
        except Exception,e:
            numError += 1
            print 'problem when parsing file', filename.decode('utf-8'), 'number', numError
            print Exception,":",e
