# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import tempfile
import unittest
from ..rnc import convert_rnc_format


class TestConvertMreRnc(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def testNormal(self):
        src_file = os.path.join(os.path.dirname(__file__), 'data', 'rnc-mre-src.conll')
        dest_file = os.path.join(self.temp_dir, 'rnc-cnv-mre-act.conllu')

        convert_rnc_format(src_file, dest_file)
        with open(dest_file, 'rb') as df:
            actual = df.read().decode('utf-8')
            # print(actual)

        trg_file = os.path.join(os.path.dirname(__file__), 'data', 'rnc-cnv-trg.conllu')
        with open(trg_file, 'rb') as tf:
            expected = tf.read().decode('utf-8')

        self.assertListEqual(expected.split('\n'), actual.split('\n'))
