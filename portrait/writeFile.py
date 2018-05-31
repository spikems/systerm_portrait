#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
写入excel;
"""
import sys
import os
import time
import pandas as pd

import re
import logging
import logging.config
logger=logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)

def writeFile(fname,Listf,columus,filepath=''):
    """
    文件名称
    :param fname:
    :param Listf:
    :param delimiter:
    :param not_tuple:
    :return:
    """
    # fname = re.sub('\s','',fname).encode('utf-8')
    if os.path.exists(filepath) is False:
        os.makedirs(filepath)
    else:
        os.system("""find %s -mtime +1 -name '*.xlsx' -exec rm -rf {} \;"""%filepath)

    writer = pd.ExcelWriter('%s/%s.xlsx'%(filepath,fname))
    Listformat = [(i[0].decode('utf-8'),i[1])  for i in Listf]
    df = pd.DataFrame(Listformat,columns=columus)
    df.to_excel(writer)
    writer.save()

    # if delimiter =='\n' and not_tuple:
    #     writer.write(delimiter.join(Listf))
    #
    # elif (delimiter=='\n') and not (not_tuple):
    #     for sub in Listf:
    #         writer.write(sub[0]+'\t'+str(sub[1])+'\n')


if __name__ == '__main__':
    l = [('wangwei',26),('wangwei',25)]
    writeFile('enroll',l,columus=['name','age'])