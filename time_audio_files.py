#!/usr/bin/env python
# encoding: utf-8

from pyannote.audio.features.utils import get_audio_duration
import glob

subpath = '/vol/work3/maurice/AlbayzinEvaluationIberSPEECH-RTVE2018/data/RTVE2018DB/dev2/'
path = subpath + 'audio/'
files = glob.glob(path+'*-16000.wav')
for f in files:
    print(f.split('/')[-1].split('-mono')[0], get_audio_duration({'audio':f}))

path = subpath + 'enrollment/'
files = glob.glob(path+'*/*-16000.wav')
for f in files:
    print(f.split('/')[-1].split('-16000')[0], get_audio_duration({'audio':f}))
