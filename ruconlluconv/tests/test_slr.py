# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import tempfile
import unittest
from ..slr import convert_slr_format


class TestConvertSlrFormat(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def testNormal(self):
        src_file = os.path.join(os.path.dirname(__file__), 'data', 'slr-man-src.dat')
        dest_file = os.path.join(self.temp_dir, 'slr-cnv-act.conllu')

        convert_slr_format(src_file, dest_file)
        with open(dest_file, 'rb') as df:
            actual = df.read().decode('utf-8')

        trg_file = os.path.join(os.path.dirname(__file__), 'data', 'slr-cnv-trg.conllu')
        with open(trg_file, 'rb') as tf:
            expected = tf.read().decode('utf-8')

        self.assertListEqual(expected.split('\n'), actual.split('\n'))
