#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2017 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr
# Benjamin MAURICE - maurice@limsi.fr

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import os.path as op
from pyannote.core import Segment, Timeline, Annotation
from pyannote.database import Database
from pyannote.database.protocol import SpeakerSpottingProtocol, SpeakerDiarizationProtocol
from pandas import read_table
from os import listdir
import os

# this protocol defines a speaker diarization protocol: as such, a few methods
# needs to be defined: trn_iter, dev_iter, and tst_iter.

def read_rttm_file(file):
    # load whole file
    df = read_table(file,
    delim_whitespace=True,
    header=None, names=['type', 'uri', 'channel', 'start', 'duration', 'modality', 'confidence', 'label', 'gender'],
    keep_default_na=False, na_values=[])

    # remove comment lines
    # (i.e. lines for which all fields are either None or NaN)
    #keep = [not all(pandas.isnull(item) for item in row[3:4])
    #        for row in df.itertuples()]
    #df = df[keep]
    df = df.loc[~df['type'].str.contains('-INFO')]
    return df

class RTVE2018SpeakerSpottingProtocolAll(SpeakerSpottingProtocol):
    """Speaker spotting protocol for the Albayzin Evaluation of IberSPEECH from RTVE2018 dataset on dev2
    Parameters
    ----------
    preprocessors : dict or (key, preprocessor) iterable
        When provided, each protocol item (dictionary) are preprocessed, such
        that item[key] = preprocessor(**item). In case 'preprocessor' is not
        callable, it should be a string containing placeholder for item keys
        (e..{'wav': '/path/to/{uri}.wav'})
    """

    def __init__(self, preprocessors={}, **kwargs):
        super(RTVE2018SpeakerSpottingProtocolAll, self).__init__(
            preprocessors=preprocessors, **kwargs)

    def _subset(self, protocol, corpus, subset):

        data_dir = op.join(op.dirname(op.realpath(__file__)), 'data')

        # load annotations
        #path = op.join(data_dir, '{protocol}.{subset}.mdtm'.format(subset=subset, protocol=protocol))
        #rttms = self.rttm_parser_.read(path)

        path = op.join(data_dir, '{protocol}.{corpus}.{subset}.lst'.format(subset=subset, corpus=corpus, protocol=protocol))
        with open(path) as f:
            uris = f.readlines()
        uris = [x.strip() for x in uris]

        rttms = {}
        for path in listdir(op.join(data_dir, 'rttm')):
            if 'FACEREF' in path:
                continue
            rttm = read_rttm_file(op.join(data_dir, 'rttm', path))
            uri = rttm['uri'].iloc[0]
            annotation = Annotation()
            for index, row in rttm.iterrows():
                annotation[Segment(float(row['start']), float(row['start']) + float(row['duration']))] = row['label']
            rttms[uri] = annotation

        #By default it take all the file time
        '''path = op.join(data_dir, '{protocol}.{corpus}.{subset}.time'.format(subset=subset, corpus=corpus, protocol=protocol))
        with open(path) as f:
            rows = f.readlines()
        times = {}
        for row in rows:
            kv = row.split(' ')
            times[kv[0]] = Segment(0, float(kv[1]))'''

        for uri in uris:
            #annotated = times[uri]
            annotation = rttms[uri]
            current_file = {
                'database': 'RTVE2018',
                'uri': uri,
            #    'annotated': annotated,
                'annotation': annotation}
            yield current_file

    def _subset_enrollment(self, protocol, subset):
        data_dir = op.join(op.dirname(op.realpath(__file__)), 'data')
        enrolments = op.join(data_dir, '{protocol}.{subset}.txt'.format(subset=subset, protocol=protocol))
        names = ['uri', 'NA0', 'start', 'duration', 'NA1', 'NA2', 'NA3', 'model_id']
        enrolments = read_table(enrolments, delim_whitespace=True, names=names)

        for model_id, turns in enrolments.groupby(by='model_id'):

            # gather enrolment data
            segments = []
            for t, turn in enumerate(turns.itertuples()):
                if t == 0:
                    raw_uri = turn.uri
                    uri = f'{raw_uri}'
                segment = Segment(start=turn.start, end=turn.start + turn.duration)
                if segment:
                    segments.append(segment)
            enrol_with = Timeline(segments=segments, uri=uri)

            current_enrolment = {
                'database': 'RTVE2018',
                'uri': uri,
                'model_id': model_id,
                'enrol_with': enrol_with,
            }

            yield current_enrolment

    def trn_iter(self):
        return self._subset('RTVE2018', 'Dev2', 'train')

    def dev_iter(self):
        return self._subset('RTVE2018', 'Dev2', 'dev')

    def tst_iter(self):
        for _ in []:
            yield
        #return self._subset('RTVE2018', 'test')

    def dev_enrol_iter(self):
        return self._subset_enrollment('RTVE2018', 'enrollment')

    def trn_enrol_iter(self):
        for _ in []:
            yield

    def trn_try_iter(self):
        for _ in []:
            yield

    def def_try_iter(self):
        for _ in []:
            yield

    def tst_enroll_iter(self):
        for _ in []:
            yield

    def tst_try_iter(self):
        for _ in []:
            yield

# this is where we define each protocol for this database.
# without this, `pyannote.database.get_protocol` won't be able to find them...

class RTVE2018(Database):
    """Database RTVE2018 on dev2"""

    def __init__(self, preprocessors={}, **kwargs):
        super(RTVE2018, self).__init__(preprocessors=preprocessors, **kwargs)
        #super().all(*args, **kwargs)

        # register the first protocol: it will be known as
        # MyDatabase.SpeakerDiarization.MyFirstProtocol
        self.register_protocol('SpeakerSpotting', 'all_annotations', RTVE2018SpeakerSpottingProtocolAll)
