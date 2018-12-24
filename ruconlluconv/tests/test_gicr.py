# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import tempfile
import unittest
from ..gicr import join_gicr_composite, convert_gicr_format


class TestJoinGicrComposite(unittest.TestCase):
    def testDense(self):
        source = [
            ['2', 'одно', 'одно', 'X', '_', '_', '_', '_', '_', '_'],
            ['2', 'бортные', 'бортный', 'ADJ', '_', 'Number=Plur|Case=Nom|Degree=Pos', '_', '_', '_', '_'],
        ]
        expected = ['2', 'однобортные', 'однобортный', 'ADJ', '_', 'Number=Plur|Case=Nom|Degree=Pos', '_', '_', '_',
                    '_']
        actual = join_gicr_composite(source)

        self.assertListEqual(expected, actual)

    def testSparse(self):
        source = [
            ['17', 'экс', 'экс', 'X', '_', '_', '_', '_', '_', '_'],
            ['17', '-', '-', 'PUNCT', '_', '_', '_', '_', '_', '_'],
            ['17', 'глава', 'глава', 'NOUN', '_', 'Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing', '_', '_', '_', '_']
        ]
        expected = ['17', 'экс-глава', 'экс-глава', 'NOUN', '_', 'Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing', '_',
                    '_', '_', '_']
        actual = join_gicr_composite(source)

        self.assertListEqual(expected, actual)

    def testContinuous(self):
        source = [
            ['9', 'мини', 'мини', 'X', '_', '_', '_', '_', '_', 'SpaceAfter=No'],
            ['9', '-', '-', 'PUNCT', '_', '_', '_', '_', '_', 'SpaceAfter=No'],
            ['9', 'шорто', 'шорты', 'X', '_', '_', '_', '_', '_', 'SpaceAfter=No'],
            ['9', '-', '-', 'PUNCT', '_', '_', '_', '_', '_', 'SpaceAfter=No'],
            ['9', 'юбки', 'юбка', 'NOUN', '_', 'Animacy=Inan|Case=Nom|Gender=Fem|Number=Plur', '_', '_', '_', '_'],
        ]
        expected = [
            '9', 'мини-шорто-юбки', 'мини-шорты-юбка', 'NOUN', '_', 'Animacy=Inan|Case=Nom|Gender=Fem|Number=Plur', '_', '_', '_', '_']
        actual = join_gicr_composite(source)

        self.assertListEqual(expected, actual)


class TestConvertGicrFormat(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def testNormal(self):
        gicr_files = [
            os.path.join(os.path.dirname(__file__), 'data', 'gicr-man1-src.txt'),
            os.path.join(os.path.dirname(__file__), 'data', 'gicr-man2-src.txt')
        ]
        act_file = os.path.join(self.temp_dir, 'gicr-cnv-act.conllu')

        convert_gicr_format(gicr_files, act_file)
        with open(act_file, 'rb') as df:
            actual = df.read().decode('utf-8')
            print(actual)

        trg_file = os.path.join(os.path.dirname(__file__), 'data', 'gicr-cnv-trg.conllu')
        with open(trg_file, 'rb') as tf:
            expected = tf.read().decode('utf-8')

        self.assertListEqual(expected.split('\n'), actual.split('\n'))
