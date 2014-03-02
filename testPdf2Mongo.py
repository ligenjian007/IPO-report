__author__ = 'ligenjian'

import IPOReportExtractor
import re
import os
import pymongo

connection = pymongo.Connection('localhost', 27017)
db = connection.risk_database
collection = db.risk_collection

pdfMatcher = re.compile(r'.*\.txt')

for filename in os.listdir('.'):
    if pdfMatcher.match(filename):
        ipoExtractor = IPOReportExtractor.IPOReportExtractor()
        riskMap = ipoExtractor.processFile(filename, '.')
        collection.insert({'corporation_name':filename.split('.')[0], 'risk_content' : riskMap})