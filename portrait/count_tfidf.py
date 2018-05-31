#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from __future__ import division
import sys
import os
import time
import redis
import heapq
from collections import Counter
import logging
import logging.config
logger=logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
_redis = redis.Redis(host='192.168.241.46', db=1)


def count_tfidf(sents,count_type=None,topn=1000):
    """
    count tfidf
    :param sents:type is list format like ['wo xi huan dazhong che ',] a string segmentation is space
    :param count_type: [tfidf ,chi2] now only include tfidf
    :param topn: top n words
    :return: [(word,freq).....],which length is topn  
    """
    words = []
    for line in sents:
        if line:
            words.extend(filter(lambda x:len(x.decode('utf-8'))>1,line.split()))
    del_word = {}
    dwords = Counter(words)
    words_num = len(dwords)
    if count_type == 'tfidf':
        for keyword, freq in dwords.items():
            word = keyword.strip()
            if _redis.get('idf_%s' % word):
                tfidf = freq * float(_redis.get('idf_%s' % word))  # tf*idf
                dwords[keyword] = tfidf
            else:
                tfidf = freq * 1.2
                dwords[keyword] = tfidf
    # del_num = len(del_word)
    # sort_del = sorted(del_word.items(),key=lambda x:x[1],reverse=True)
    # [logger.info('%s:%s\n'%(i[0],i[1])) for i in sort_del[:10]]
    # logger.info('all num is %s,del word num is %s ,percentage is %.2f' % (words_num,del_num,del_num/words_num))
    sort_dword = heapq.nlargest(n=topn,iterable=dwords.items(),key=lambda x:x[1])
    return sort_dword

if __name__ == '__main__':
    sent = ['我 在 吃饭 好不好','你 说 什么 我 听不到']