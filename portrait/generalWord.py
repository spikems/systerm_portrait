#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
get general word and stop word ,database is dm_base
"""
import sys
import os
import time
import logging
import logging.config
logger=logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
dir_path = os.path.dirname(os.path.abspath(__file__))
import pymysql


def general_word():
    conn = pymysql.connect(host='192.168.241.45', port=3306, user='oopin', passwd='OOpin2007Group', db='dm_base',
                           charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('select name from general_word')
    # conn.commit()
    filter_word = set([])
    for sub in  cur.fetchall():
        filter_word.add(sub['name'].strip())
    # 加载停用词表
    [filter_word.add(line.strip().decode('utf-8', 'ignore')) for line in open('%s/conf/stopword.txt' % dir_path).readlines() if
            line.strip()]
    conn.close()
    return filter_word

if __name__ == '__main__':
    pass