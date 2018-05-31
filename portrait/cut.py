#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import division
import sys
import os
import time
import logging
import logging.config
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
from wcut.jieba.norm import norm_cut,load_industrydict
from wcut import jieba
load_industrydict([0])
dir_path = os.path.dirname(os.path.abspath(__file__))
import esm


#加载广告词表
adver = [line.strip() for line in open('%s/conf/advertiseWord.txt'%dir_path).readlines()]
adver_esm = esm.Index()

for word in adver:
    adver_esm.enter(word)
adver_esm.fix()

def trim(words):
    if words:
        return words.encode('utf-8','ignore').replace('\r', '').replace('\t', '').replace('\n', '')
    else:
        return ''

def cut_word(data,filterWord):
    """
    cut word and extract brands After remove advertise articles and stop words
    :param data:
    :param filterWord: stop word and general word such as '的','有'
    :return: cutword type is list format like ['wo xi huan dazhong che ',] a string segmentation is space
    brands  type is list format like ['dazhong','benchi']
    """
    cutword = []
    brands = []
    sentLen = []
    jieba.enable_parallel(30)
    all_num = 0
    cut_num = 0
    for lineSource in data:
        all_num +=1
        outline = trim(lineSource['title']) + '.' + trim(lineSource['text'])
        if  'brands' in lineSource:
            for brand in lineSource['brands']:
                brands.append(brand.encode('utf-8','ignore'))
        sentlenth =  len(outline.decode('utf-8', 'ignore'))
        sentLen.append(sentlenth)
        if adver_esm.query(outline):
            continue
        if 5 < sentlenth< 4000 :
            cutword.append(' '.join([i for i in norm_cut(outline) if i not in filterWord]).encode('utf-8'))
            cut_num+=1
    jieba.disable_parallel()
    logger.info('avg sent length %.2f'%(sum(sentLen)/all_num))
    logger.info('all_num is %s;cutnum is %s,percentage is %.2f'%(all_num,cut_num,cut_num/all_num))
    return cutword ,brands

if __name__ == '__main__':
    data1, data2 = run(word='中年', stime='2018-04-01 00:00:00', etime='2018-04-2 00:00:00',
                       stime2='2018-04-10 00:00:00', etime2='2018-04-11 00:00:00')
    cword, brands = cut_word(data1)
    cword2, brands2 = cut_word(data2)
