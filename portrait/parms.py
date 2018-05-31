#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
参数检查并且转换格式
"""
import sys
import os
import time
import logging
import logging.config
logger=logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
from collections import namedtuple


def check_parms(parmdic):
    """
    检验参数
    1.如果word没有
    2.如果时间格式不对
    3.如果结束时间小于起始时间
    :param namedic:
    :return:
    """
    if  not parmdic.word.strip():
        logger.error('no main word ')
        return False

    if  not all((is_valid(parmdic.stime),is_valid(parmdic.etime))):
        logger.error('time format is not right')
        return False

    if time.strptime(parmdic.etime,'%Y-%m-%d %H:%M:%S') <= time.strptime(parmdic.stime,'%Y-%m-%d %H:%M:%S'):
        logger.error('etime is larger than start time')
        return False

    if parmdic.source not in ['pgc','ugc','news','all']:
        logger.error('source is not in our field')
        return False

    return parmdic


def is_valid(sdate1,):
    """
    检查时间格式
    :param sdate1:
    :return:
    """
    try:
        time.strptime(sdate1,'%Y-%m-%d %H:%M:%S')
        return True
    except:
        logger.error(sdate1)
        return False


def build_parms(name,sdic):
    """
    更改参数格式 word['age']=22 word.age=22
    :param name:
    :param sdic:
    :return:
    """

    User = namedtuple(name,['word','synonyms','qualifiers','stime','etime','count_type','source'])

    name = User(word=sdic['word'].decode('utf-8').strip(),
                synonyms =sdic.get('symnonyms','').decode('utf-8'),
                qualifiers=sdic.get('qualifiers','').decode('utf-8') ,
                stime=sdic['stime'],
                etime=sdic['etime'],
                count_type =sdic.get('count_type','tfidf'),
                source =sdic['source'])

    if check_parms(name):
        return name
    else:
        logger.error('Sorry parm is wrong ')
        return False


if __name__ == '__main__':
    pass