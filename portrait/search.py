#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get ES data according mainword ,synonyms,limited words ,start time ,end time,media type;
"""
import sys
import os
import time
import re

from elasticsearch import Elasticsearch
import pickle
# from multiprocessing import Pool
from elasticsearch import helpers
import logging
import logging.config
logger=logging.getLogger(__name__)
logging.root.setLevel(level = logging.INFO)
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s')
es = Elasticsearch(["http://192.168.241.35:9200", "http://192.168.241.46:9200", "192.168.241.50:9201",
                    "http://192.168.241.47:9201"], sniffer_timeout = False)
dir_path = os.path.dirname(os.path.abspath(__file__))

def build_should_body(synonyms):
    """
    build the core query
    :param synonyms:format 'adidas 阿迪达斯' warning: segmentation is space
    :return: query sentence
    """
    should_body = []
    for group in synonyms:
        if not group:
            continue
        bool_body = {"bool": {"must": []}}
        for word in group.split():
            multi_body = {
                "multi_match": {
                    "minimum_should_match": "100%",
                    "query": word,
                    "type": "phrase",
                    "slop": 0,
                    "fields": ["title", "text"]}}
            bool_body["bool"]["must"].append(multi_body)
        should_body.append(bool_body)
    return should_body

def build_mustnot_body(limited_word):
    """
    build reverse query when you are searching for  '智能车寨' and do not want see an article on "智能音箱"
    :param limited_word: format '大众 奔驰' warning: segmentation is space
    :return:must_not query
    """
    must_not_body = []
    for group in limited_word:
        if not group:
            continue
        for word in group.split():
            multi_body = {
                "multi_match": {
                    "minimum_should_match": "100%",
                    "query": word,
                    "type": "phrase",
                    "slop": 0,
                    "fields": ["title", "text"]}}
            must_not_body.append(multi_body)
    return must_not_body

def build_source(source):
    """
    Designated media sources
    :param source: now include ['ugc','pgc'] ,it should actually be include 'news'
    :return: term query
    """
    if source  == 'ugc':
        terms = {"terms": {"site_id": []}}
        with open('%s/conf/ugc.txt','rb'%dir_path) as inf:
            for line in inf :
                if line.strip():
                    terms["terms"]["site_id"].append(line.strip())
        return terms

    elif source =='pgc':
        return {"range":{"influence":{"gte" : 20}}}

    return False

def build_body(word,limited_words,stime,etime,source=False):
    """
    build es query
    :param word:
    :param limited_words:
    :param stime:
    :param etime:
    :return:
    """

    body = {"query":{"bool":{"must":[{"range": {"post_time":
                                    {"gte": stime,
                                     "lt": etime, }}},{"term":{"text_repeat":"F"}}],
                             "minimum_should_match": 1,
                             "should": build_should_body(word)
                             }}}
    if source:
        terms = build_source(source)
        if terms:
            body["query"]["bool"]["must"].append(terms)


    if limited_words:
        must_not_body = build_mustnot_body(limited_words)
        body["query"]["bool"]["must_not"] = must_not_body
    return  body

def search(body,limit_size=50000):
    """
    execute search
    :param body: query sentence
    :param limit_size:ramdom select some article
    :return: search result type is yield ,format like [{"text":"avx","title":"","brands":"" ...}, so on ]
    """
    count_result = es.count(index='community2', body=body)
    if count_result['count'] == 0:
        logger.error('es search data num is 0')

    logger.info('how many word %s in seach'%count_result)
    es_re = helpers.scan(es,query = body,index = 'community2',size = 800,request_timeout = 600)
    num = 0
    for sub in es_re:
        num += 1
        yield  (sub['_source'])
        if num >= limit_size:
            break

def search_run(word,stime,etime,synonyms='',qualifier='',source=''):
    """
    control search
    :param word:
    :param stime:
    :param etime:
    :param synonyms: segmentation is '#'
    :param qualifier: segmentation is '#'
    :param source: ['ugc','pgc','ogc']
    :return:
    """
    lword = []
    limit_word = []
    lword.append(word)
    if synonyms.strip():
        lword.extend(synonyms.strip().split('#'))
    if qualifier.strip():
        limit_word.extend(qualifier.strip().split('#'))

    body = build_body(word=lword,limited_words=limit_word,stime=stime,etime=etime,source=source)
    logger.info(body)
    return search(body)


if __name__ == '__main__':
    search_run(word='智能 手机连接',stime='2018-04-01 00:00:00',etime='2018-04-1 01:00:00')



