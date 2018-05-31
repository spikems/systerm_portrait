#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc position :http://doc.mxspider.top/pages/viewpage.action?pageId=853634
systerm portrain The main control program
1.search
2.cut word and remove advertise article
3.remove duplicate article
4.count word use tfidf
5.GET new brand ,new word burtst word from compare hotwords
input : two dict ,params detail you can look params.py
output :eight file format xlsx  First column is word Seconde column is freq
(main_word ; hotwords ; minor_word hotwords ;new words ; miss words ;burst words;new_brands,miss_brands,burst_brands
) and six list which format is list[(word,freq),(word,freq)](new_brand, miss_brand, burstBrand, newWord, missWord, burstWord)
"""

import sys
import os
from time import time
import logging
import logging.config
logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level = logging.INFO)
from  search import  search_run
from cut import cut_word
from articledup import dedup_near
from count_tfidf import count_tfidf
from compare import compare_brand,compare_word
from writeFile import writeFile
from parms import build_parms
from generalWord import general_word
init_time = time()

class SystemPortrait(object):
    """
    mainObject: TYPE:dict key include ['word','synonyms','qualifiers','stime','etime','count_type','source']
    means : 查询词,同义词,限定词,起始时间,结束时间,计数类型,来源 , 同义词之间
    minorObject is same as mainobject
    special_data : 指定数据来源
    """

    def __init__(self,mainObject,minorObject,filepath,specify_data=False):

        if not specify_data:
            self.mainObject = build_parms('search1',mainObject)
            self.minorObject = build_parms('search2',minorObject)
        else:
            self.mainObject = mainObject
            self.minorObject = minorObject
        self.specify_data = specify_data
        self.filepath = filepath


    def build_words(self,search,filterWord):

        """
        构建可对比的词表
        :param search:
        :return:
        """
        raw_data = search_run(word = search.word, stime = search.stime, etime = search.etime,
                              synonyms = search.synonyms, qualifier = search.qualifiers, source = search.source)
        if not raw_data:
            label = 'do not seach any article according %s  from %s to %s '%(search.word,search.stime,search.etime)
            return  False, label
        cut_data, brand = cut_word(raw_data,filterWord)

        dup_data = dedup_near(cut_data, k=3, b=6)

        count_data = count_tfidf(dup_data, count_type = search.count_type, topn = 1000)

        writeFile('%s_%s'%(search.word,search.etime.split()[0]+'hotword'),count_data,['word','freq'],self.filepath)

        return count_data,brand

    def run(self):
        """
        获取数据,品牌对比,和热词对比
        :param main_brand:
        :param minor_brand:
        :return:
        """
        filterWord = general_word()

        main_data,main_brand = self.build_words(self.mainObject,filterWord)
        if not main_data:
            return main_data,minor_brand,False,False,False,False

        minor_data,minor_brand = self.build_words(self.minorObject,filterWord)
        if not minor_data:
            return minor_data,minor_brand,False,False,False,False

        new_brand, miss_brand, burstBrand = compare_brand(minor_brand,main_brand )

        newWord, missWord, burstWord = compare_word(minor_data,main_data )

        main_file = '%s_%s'%(self.mainObject.word,self.mainObject.etime.split()[0])
        minor_file = '%s_%s'%(self.minorObject.word,self.minorObject.etime.split()[0])

        writeFile('%snewbrand'%main_file, new_brand,['brand','num'],self.filepath)
        writeFile('%smiss_brand'%minor_file,miss_brand,['brand','num'],self.filepath)
        writeFile('%sburstBrand'%main_file,burstBrand,['brand','ratio'],self.filepath)

        writeFile('%snewWord'%main_file,newWord,['word','num'],self.filepath)
        writeFile('%smissWord'%minor_file,missWord,['word','num'],self.filepath)
        writeFile('%sburstWord'%main_file,burstWord,['word','num'],self.filepath)

        logger.info(' %s  task is finished ,all spend time is %s'%(__name__,round(time()-init_time,2)))
        return new_brand, miss_brand, burstBrand, newWord, missWord, burstWord

if __name__ == '__main__':
    ['word', 'synonyms', 'qualifiers', 'stime', 'etime', 'count_type', 'source']
    search1 = {'word':'耐克','stime':'2018-4-1 00:00:00','etime':'2018-4-3 00:00:00','source':'pgc'}
    search2 = {'word':'阿迪','stime':'2018-4-1 00:00:00','etime':'2018-4-3 00:00:00','source':'pgc'}
    filepath = 'output'
    ins = SystemPortrait(search1,search2,filepath)
    ins.run()