# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import tempfile
import unittest
from ..gicr import join_gicr_composite, join_gicr_splits, convert_gicr_format


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
            '9', 'мини-шорто-юбки', 'мини-шорты-юбка', 'NOUN', '_', 'Animacy=Inan|Case=Nom|Gender=Fem|Number=Plur', '_',
            '_', '_', '_']
        actual = join_gicr_composite(source)

        self.assertListEqual(expected, actual)


class TestJoinGicrSplits(unittest.TestCase):
    def testSparse(self):
        source = [
            '', '',
            u'627448	0006	Ростов             	[Ростов]                   	Npmsn-n',
            u'627448	   P	-',
            u'627448	0007	на-Дону            	[на-Дону]                  	Xf',
            u'627448	0008	2                  	[#Number]                  	M*---d',
            '', '',
        ]
        expected = [
            '', '',
            u'627448	0006	Ростов-на-Дону	[Ростов-на-Дону]	Npmsn-n',
            u'627448	0008	2                  	[#Number]                  	M*---d',
            '', '',
        ]
        actual = join_gicr_splits('\n'.join(source))

        self.assertListEqual(expected, actual.split('\n'))

    def testDense(self):
        source = [
            '', '',
            u'528358	   P	"',
            u'528358	0124	Лента              	[лента]                    	Ncfsn-n',
            u'528358	0125	.ру                	[.ру]                      	Xf',
            u'528358	   P	"',
            u'528358	0126	вела               	[вести]                    	Vifs--syaim-',
            u'528358	0127	онлайн             	[онлайн]                   	Rp',
            u'528358	0128	этой               	[этот]                     	Pdfsi-a',
            u'528358	0129	встречи            	[встреча]                  	Ncfpa-n',
            u'528358	   P	.',
            '', '',
        ]
        expected = [
            '', '',
            u'528358	   P	"',
            u'528358	0124	Лента.ру	[лента.ру]	Ncfsn-n',
            u'528358	   P	"',
            u'528358	0126	вела               	[вести]                    	Vifs--syaim-',
            u'528358	0127	онлайн             	[онлайн]                   	Rp',
            u'528358	0128	этой               	[этот]                     	Pdfsi-a',
            u'528358	0129	встречи            	[встреча]                  	Ncfpa-n',
            u'528358	   P	.',
            '', '',
        ]
        actual = join_gicr_splits('\n'.join(source))

        self.assertListEqual(expected, actual.split('\n'))

    def testSkip(self):
        source = [
            '', '',
            u'619603	0261	Поддерживать       	[поддержать]               	Vn-----yaim-',
            u'619603	   P	"',
            u'619603	0262	статус             	[статус]                   	Ncmsa-n',
            u'619603	0263	кво                	[кво]                      	Xf',
            u'619603	   P	."',
            '', '',
        ]
        actual = join_gicr_splits('\n'.join(source))

        self.assertListEqual(source, actual.split('\n'))


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

        trg_file = os.path.join(os.path.dirname(__file__), 'data', 'gicr-cnv-trg.conllu')
        with open(trg_file, 'rb') as tf:
            expected = tf.read().decode('utf-8')

        self.assertListEqual(expected.split('\n'), actual.split('\n'))

    def testGold(self):
        gicr_files = [
            os.path.join(os.path.dirname(__file__), 'data', 'gicr-gold-src.txt'),
        ]
        act_file = os.path.join(self.temp_dir, 'gicr-cnv-act.conllu')

        convert_gicr_format(gicr_files, act_file)
        with open(act_file, 'rb') as df:
            actual = df.read().decode('utf-8')

        trg_file = os.path.join(os.path.dirname(__file__), 'data', 'gicr-gold-trg.conllu')
        with open(trg_file, 'rb') as tf:
            expected = tf.read().decode('utf-8')

        actual = [w for w in actual.split('\n') if '\t~' not in w]
        expected = [w for w in expected.split('\n') if '\t~' not in w]
        self.assertListEqual(expected, actual)
