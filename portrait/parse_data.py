#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from kword.QA_Extract import NewQAExtractWord
from input_data import Saver
from datetime import datetime
import logging
import sys ,os

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
import logging.config
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info('task is start')

reload(sys)
sys.setdefaultencoding('utf-8')
newqa =  NewQAExtractWord()
classdic = {} #词和词类别
save = Saver()
wrongfile = open('wrong_data','wb')
#获取已经存在对应表 like 发动机:组件

with open('word_rela.txt','rb') as inf:
    for line in inf :
        lines = line.strip().split('\t')
        if len(lines)>1:
            classdic[lines[0].strip()] = lines[1]

#获取对应关系
def get_class(word):
    classfy = newqa.extract_master(word,1)
    for key,value in classfy.items():
        if value and key !='is_contrast':
            return key
    return False

#存入哪些数据
def make_dic(dic):
    if dic['relaword'] in classdic:
        dic['classfy'] = classdic[dic['relaword']]
    else:
        result = get_class(dic['relaword'])
        if result:
            dic['classfy'] = result
            classdic[dic['relaword']] = result
        else:
            dic['classfy'] = 'issue'
            classdic[dic['relaword']] = 'issue'
    return dic

infile = open(sys.argv[1],'rb')
num = 0
loadinnum = 0
lossnum = 0
for line in infile:
    dic = {}
    num+=1
    if num % 10000 == 0:
        logger.info('已经处理了%s个'%num)
    lines = line.strip().split('\t')
    dic['mainword'] = lines[0]
    dic['relaword'] = lines[1]
    dic['coefficient'] = lines[2]
    dic['Acoefficient'] = lines[3]
    dic['Bcoefficient'] = lines[4]
    dic['Ccoefficient'] = lines[5]
    dic['Dcoefficient'] = lines[6]
    fdic = make_dic(dic)
    if fdic:
        save.pass_data(fdic)
        loadinnum +=1
    else:
        lossnum+=1
        logger.info('%s数据存入失败'%str(lossnum))
        logger.info(line)
        wrongfile.write(line)
        exit()
    #交换一下位置
    tmpword = dic['mainword']
    dic['mainword'] = dic['relaword']
    dic['relaword'] = tmpword
    sdic = make_dic(dic)
    if sdic:
        save.pass_data(sdic)
        loadinnum += 1
    else:
        lossnum+=1
        logger.info('%s数据存入失败'%str(lossnum))
        logger.info(line)
        wrongfile.write(line)
logger.info('已经处理了%s个' % num)

outfile = open('word_rela0327','wb') #词与字典对应关系
for i,v in classdic.items():
    outfile.write('%s\t%s\n'%(i,v))
outfile.close()
infile.close()
wrongfile.close()