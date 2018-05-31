#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
function :remove similar article from simhash
input  a list  format like ['wo xi huan dazhong che ',] a string segmentation is space
return a list format like ['wo xi huan dazhong che ',] a string segmentation is space
"""
import sys
import os
import time
import logging
import logging.config
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
import simhash


def compute(text):
    """
        compute hash for a document by shingles
    """

    tokens = text.split()
    phrases = (' '.join(phrase) for phrase in simhash.shingle(tokens, 4))

    hashes = map(simhash.unsigned_hash, phrases)

    return simhash.compute(hashes)


def dedup_near(data,k,b):
    removelist = []
    grplist = []


    duphash = {}   #hash -> set(lineid)
    linecnt = 0
    data_h = []   #list of hash val
    index = {}  # hash val -> lineid
    data_v = {}  # lineid -> data

    for line in data:
        hash = compute(line)
        if hash in index:
            if hash in duphash:
                duphash[hash].append(linecnt)
            else:
                duphash[hash] = [index[hash],]
                duphash[hash].append(linecnt)
        else:
            index[hash] = linecnt
        data_v[linecnt] = line
        data_h.append(hash)
        linecnt+=1

    for key in duphash.keys():
        ids = duphash[key]
        removelist.extend(ids[1:])
        grplist.append(ids)
    logger.info('duphash removecnt=%d, linecnt = %s', len(removelist), linecnt)
    matches = simhash.find_all(data_h,b,k)
    marks = {}  # lineid -> groupid
    grpindex = {}  # groupid -> [lineids]
    groupid = 0
    for A, B in matches:
        grpidA, grpidB = -1, -1
        if index[A] in marks:
            grpidA = marks[index[A]]
        if index[B] in marks:
            grpidB = marks[index[B]]
        if grpidA == -1 and grpidB == -1:
            # new pair
            marks[index[A]] = groupid
            marks[index[B]] = groupid
            grpindex[groupid] = set([index[A], index[B]])

            groupid += 1
        elif grpidA == -1:
            # add B to group A
            marks[index[A]] = grpidB
            grpindex[grpidB].add(index[A])
        elif grpidB == -1:
            marks[index[B]] = grpidA
            grpindex[grpidA].add(index[B])
        else:
            # merge two old groups
            for lid in grpindex[grpidB]:
                marks[lid] = grpidA
                grpindex[grpidA].add(lid)
            grpindex[grpidB].clear()

    linecntx = 0
    for grp in grpindex.keys():
        if grpindex[grp]:
            ids = [lid for lid in grpindex[grp]]
            ids = sorted(ids, reverse=True)

            linecntx += len(ids[1:])
            # output the first one
            removelist.extend(ids[1:])
            grplist.append(ids)

    logger.info('total removecnt=%d, linecntx = %s, grpcnt=%d', len(removelist), linecntx, len(grpindex.keys()))

    remain = []
    remove = set(removelist)
    for lid in range(linecnt):
        if lid not in remove and lid in data_v:
            remain.append(data_v[lid])

    with open('grp', 'w') as grpf:
        for grp in grplist:
            if len(grp) > 1:
                for id in grp:
                    grpf.write('%s\n'%(data_v[id].replace(" ","")))
                grpf.write('###############\n')
    return remain
    # for A,B in matches:

if __name__ == '__main__':
    # data = ['我 是 中国 人','你 是 中国 人','他 是 中国 人','它 是 中国 人']
    data1, data2 = run(word='中年', stime='2018-04-01 12:00:00', etime='2018-04-2 00:00:00',
                       stime2='2018-04-10 00:00:00', etime2='2018-04-11 00:00:00')
    cword, brands = cut_word(data1)
    # cword2, brands2 = cut_word(data2)
    remain1 = dedup_near(cword,k=3,b=6)   #b 值一定要大于K值,K越大去重越厉害