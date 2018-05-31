#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import sys
import os
import time
import logging
import logging.config
logger=logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
from  search import  search_run
from collections import Counter
import heapq

raw_data = search_run(word=u"nike",stime="2018-03-10 00:00:00",etime="2018-03-31 00:00:00",synonyms=u"耐克",qualifier="",source="pgc")
brands = []
for sub in raw_data:
    if 'brands' in sub:
        for brand in sub['brands'] :
            brands.append(brand.encode('utf-8', 'ignore'))

result = sorted(Counter(brands).items(),key=lambda x:x[1],reverse=True)[:10]
for line in result:
    brand,num = line
    print brand,num


if __name__ == '__main__':
    pass

