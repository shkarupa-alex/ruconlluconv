# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import tempfile
import unittest
from ..mrg import convert_mrg_format


class TestExtractStrMreDiff(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def testNormal(self):
        src_files = [
            os.path.join(os.path.dirname(__file__), 'data', 'mrg-man1-src.txt'),
            os.path.join(os.path.dirname(__file__), 'data', 'mrg-man2-src.txt')
        ]
        act_file = os.path.join(self.temp_dir, 'mrg-cnv-act.conllu')

        convert_mrg_format(src_files, act_file)
        with open(act_file, 'rb') as df:
            actual = df.read().decode('utf-8')
            # print(actual)

        trg_file = os.path.join(os.path.dirname(__file__), 'data', 'mrg-cnv-trg.conllu')
        with open(trg_file, 'rb') as tf:
            expected = tf.read().decode('utf-8')

        self.assertListEqual(expected.split('\n'), actual.split('\n'))
