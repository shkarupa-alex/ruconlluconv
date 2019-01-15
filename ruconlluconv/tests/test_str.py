# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import tempfile
import unittest
from ..str import extract_mre_diff


class TestExtractStrMreDiff(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def testNormal(self):
        ud_files = [
            os.path.join(os.path.dirname(__file__), 'data', 'str-ud1-src.conllu'),
            os.path.join(os.path.dirname(__file__), 'data', 'str-ud2-src.conllu')
        ]
        mre_file = os.path.join(os.path.dirname(__file__), 'data', 'str-mre-src.conllu')
        act_file = os.path.join(self.temp_dir, 'str-diff-act.conllu')

        extract_mre_diff(ud_files, mre_file, act_file)
        with open(act_file, 'rb') as df:
            actual = df.read().decode('utf-8')
            # print(actual)

        trg_file = os.path.join(os.path.dirname(__file__), 'data', 'str-diff-trg.conllu')
        with open(trg_file, 'rb') as tf:
            expected = tf.read().decode('utf-8')

        self.assertListEqual(expected.split('\n'), actual.split('\n'))
