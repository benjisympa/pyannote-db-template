#!/usr/bin/env python
# encoding: utf-8

# AUTHORS
# Benjamin MAURICE - maurice@limsi.fr

import pandas as pd
import os

def rttm_to_mdtm(uri):
    df = pd.read_table(uri, delim_whitespace=True, header=None)
    df.insert(loc=5, column='a', value=df[0])
    df = df.ix[:,1:-1]
    df.to_csv(uri.rsplit('.',1)[0]+'.mdtm', sep=' ', encoding='utf-8', header=False, index=False)

path = '/vol/work3/maurice/AlbayzinEvaluationIberSPEECH-RTVE2018/data/RTVE2018DB/dev2/rttm/'
for file in os.listdir(path):
    if file.endswith('.rttm'):
        print(file)
        rttm_to_mdtm(path+file)
