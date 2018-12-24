# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import tempfile
import unittest
from ..oc import convert_oc_format, extract_space_after


# class TestConvertOcFormat(unittest.TestCase):
#     def setUp(self):
#         self.temp_dir = tempfile.mkdtemp()
#
#     def tearDown(self):
#         shutil.rmtree(self.temp_dir, ignore_errors=True)
#
#     def testNormal(self):
#         src_file = os.path.join(os.path.dirname(__file__), 'data', 'oc-man-src.xml')
#         dest_file = os.path.join(self.temp_dir, 'oc-man-act.conllu')
#
#         convert_oc_format(src_file, dest_file)
#         with open(dest_file, 'rb') as df:
#             actual = df.read().decode('utf-8')
#             print(actual)
#
#         trg_file = os.path.join(os.path.dirname(__file__), 'data', 'oc-man-trg.conllu')
#         with open(trg_file, 'rb') as tf:
#             expected = tf.read().decode('utf-8')
#
#         self.assertListEqual(expected.split('\n'), actual.split('\n'))


class TestExtractSpaceAfter(unittest.TestCase):
    def testNormal(self):
        text = u'По сравнению с 2009 годом Россия опустилась в рейтинге на 9 позиций (т. е. ситуация в ней улучшилась).'
        tokens = [u'По', u'сравнению', u'с', u'2009', u'годом', u'Россия', u'опустилась', u'в', u'рейтинге', u'на',
                  u'9', u'позиций', u'(', u'т.', u'е.', u'ситуация', u'в', u'ней', u'улучшилась', u')', u'.']
        expected = [True, True, True, True, True, True, True, True, True, True,
                  True, True, False, True, True, True, True, True, False, False, True]

        actual = extract_space_after(text, tokens)
        self.assertListEqual(expected, actual)

    def testComplex1(self):
        text = u'«Вы …  литредакторов нанимать не пытались?'
        tokens = [u'«', u'Вы', u'…', u'литредакторов', u'нанимать', u'не', u'пытались', u'?']
        expected = [False, True, True, True, True, True, False, True]

        actual = extract_space_after(text, tokens)
        self.assertListEqual(expected, actual)

    def testComplex2(self):
        text = u'У С Т А Н О В И Л:'
        tokens = [u'УСТАНОВИЛ']
        expected = [True]

        actual = extract_space_after(text, tokens)
        self.assertListEqual(expected, actual)
