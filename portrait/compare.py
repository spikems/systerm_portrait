#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import division
import sys
import os
import time
import logging
from collections import Counter
import logging.config
logger=logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)

def compute_burst(dataFirst,dataLast,coexist):
    burstWord = {}
    for word in coexist:
        burstWord[word] = round((dataLast[word] - dataFirst[word])/dataFirst[word],2)
    return sorted(burstWord.items(),key=lambda x:x[1],reverse=True)[:1000]



def compare_brand(brandFisrt,brandLast):
    """
    比较品牌
    :param brandFisrt:
    :param brandLast:
    :return:新品牌,消失的品牌,爆发的品牌
    """
    new_brand = set(brandLast) - set(brandFisrt)
    miss_brand = set(brandFisrt) - set(brandLast)
    coexist = set(brandLast)&set(brandFisrt)
    cdataF = Counter(brandFisrt)
    cdataL = Counter(brandLast)
    burstWord = compute_burst(cdataF,cdataL,coexist)
    return build_tuple(new_brand,cdataL),build_tuple(miss_brand,cdataF),burstWord

def build_tuple(remain_word,dword):
    """
    为了给newword 和missword加上词频
    :param word:
    :return:
    """
    words = []
    for word in remain_word:
        words.append((word,dword[word]))
    return sorted(words,key=lambda x:x[1],reverse=True)


def compare_word(wordsFormer,wordsLater):
    """
    比较新词,和消失的词
    :param wordsFormer:次要的对象
    :param wordsLater: 主要的对象
    :return: 新词,消失的词,爆发词
    """
    wordsFormer=dict(wordsFormer)
    wordsLater = dict(wordsLater)
    newWord = set(wordsLater.keys()) - set(wordsFormer.keys())
    missWord = set(wordsFormer.keys()) - set(wordsLater.keys())
    coexist = set(wordsFormer.keys())&set(wordsLater.keys())
    burstWord = compute_burst(wordsFormer,wordsLater,coexist)
    return build_tuple(newWord,wordsLater),build_tuple(missWord,wordsFormer),burstWord


if __name__ == '__main__':
    compare_brand(['大众','长城'],['奔驰','长城'])