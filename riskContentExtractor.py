#-*- coding: utf8 -*-

__author__ = 'ligenjian'

import IPOReportExtractor
import re
import os

error = 0
passed = 0

txtMatcher = re.compile(r'.*\.txt')

for filename in os.listdir('/Users/ligenjian/Downloads/loss'):
    if txtMatcher.match(filename):
        try:
            ipoExtractor = IPOReportExtractor.IPOReportExtractor()
            riskContent = ipoExtractor.extractRisk(filename, '/Users/ligenjian/Downloads/loss')
            riskFile = open('/Users/ligenjian/Downloads/riskFile/'+filename,'w')
            riskFile.write(riskContent)
            passed += 1
            print passed, ' files have been parsed'
        except:
            error += 1
            print 'error when dumping file ', filename, ' number ',error