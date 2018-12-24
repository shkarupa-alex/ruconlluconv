from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import collections
import os


def udpos_from_multexteastru(features):
    pos = {
        'A': 'ADJ',
        'C': 'CONJ',  # CCONJ or SCONJ
        'H': 'H',
        'I': 'INTJ',
        'M': 'NUM',
        'N': 'NOUN',
        'P': 'PRON',
        'Q': 'PART',
        'R': 'ADV',
        'S': 'ADP',
        'V': 'VERB',
        'W': 'W',  # Verb or Adj or Adv
        'X': 'X',
        '_': 'X',
        '?': 'X',
    }[features[0]]

    if 'N' == features[0]:
        pos = {
            'c': 'NOUN',
            'p': 'PROPN',
        }[features[1]]

    return pos


def udfeats_from_multexteastru(f):
    if 'N' == f[0]:
        feat = collections.OrderedDict([
            ('Animacy', {
                'n': 'Inan',
                'y': 'Anim',
                '?': '',
            }[f[6]]),

            ('Case', {
                'n': 'Nom',
                'g': 'Gen',
                'd': 'Dat',
                'a': 'Acc',
                'i': 'Ins',
                'l': 'Loc',
                'v': 'Voc',
                '-': '',
                '?': '',
            }[f[4]]),

            ('Gender', {
                'm': 'Masc',
                'f': 'Fem',
                'n': 'Neut',
                'c': 'Com',
                '-': '',
                '?': '',
            }[f[2]]),

            ('Number', {
                's': 'Sing',
                'p': 'Plur',
                'i': 'Inv',
                '?': '',
            }[f[3]]),
        ])
        # N5 — Дополнительный падеж
    elif 'V' == f[0]:
        feat = collections.OrderedDict([
            ('Aspect', {
                'p': 'Imp',
                'i': 'Perf',
                '-': '',
                '?': '',
            }[f[9]]),

            ('Case', {
                'n': 'Nom',
                'g': 'Gen',
                'd': 'Dat',
                'a': 'Acc',
                'i': 'Ins',
                'l': 'Loc',
                'v': 'Voc',
                '-': '',
                '?': '',
            }[f[4]]),

            ('Gender', {
                'm': 'Masc',
                'f': 'Fem',
                'n': 'Neut',
                '-': '',
                '?': '',
            }[f[2]]),

            ('Mood', {
                'i': 'Ind',
                'm': 'Imp',
                'n': '',
                'g': '',
                'p': '',
                'x': '',
                '?': '',
            }[f[1]]),

            ('Number', {
                's': 'Sing',
                'p': 'Plur',
                '-': '',
                '?': '',
            }[f[3]]),

            ('Person', {
                '1': '1',
                '2': '2',
                '3': '3',
                '-': '',
                '?': '',
            }[f[5]]),

            ('Tense', {
                'p': 'Pres',
                'f': 'Fut',
                's': 'Past',
                '*': '',
                '-': '',
                '?': '',
            }[f[6]]),

            ('VerbForm', {
                'i': 'Fin',
                'm': 'Fin',
                'n': 'Inf',
                'g': 'Ger',
                'p': 'Part',
                'x': '',
                '?': '',
            }[f[1]]),

            ('Variant', {
                'f': '',
                's': 'Short',
                '-': '',
                '?': '',
            }[f[11]]),

            ('Voice', {
                'a': 'Act',
                'p': 'Pass',
                's': 'Mid',
                '-': '',
                '?': '',
            }[f[8]]),
        ])
        # V7 — Переходность
        # V10 — Парность
    elif 'A' == f[0]:
        feat = collections.OrderedDict([
            ('Case', {
                'n': 'Nom',
                'g': 'Gen',
                'd': 'Dat',
                'a': 'Acc',
                'i': 'Ins',
                'l': 'Loc',
                'v': 'Voc',
                '-': '',
                '?': '',
            }[f[4]]),

            ('Degree', {
                'p': 'Pos',
                'c': 'Cmp',
                's': 'Sup',
                '?': '',
            }[f[1]]),

            ('Gender', {
                'm': 'Masc',
                'f': 'Fem',
                'n': 'Neut',
                '-': '',
                '?': '',
            }[f[2]]),

            ('Number', {
                's': 'Sing',
                'p': 'Plur',
                'i': '',
                '-': '',
                '?': '',
            }[f[3]]),

            ('Variant', {
                'f': '',
                's': 'Short',
                '-': '',
                '?': '',
            }[f[5]]),

        ])
    elif 'P' == f[0]:
        feat = collections.OrderedDict([
            ('Case', {
                'n': 'Nom',
                'g': 'Gen',
                'd': 'Dat',
                'a': 'Acc',
                'i': 'Ins',
                'l': 'Loc',
                'v': 'Voc',
                '-': '',
                '*': '',
                '#': '',
                '?': '',
            }[f[4]]),

            ('Gender', {
                'm': 'Masc',
                'f': 'Fem',
                'n': 'Neut',
                '-': '',
                '*': '',
                '?': '',
            }[f[2]]),

            ('Number', {
                's': 'Sing',
                'p': 'Plur',
                '-': '',
                '*': '',
                '?': '',
            }[f[3]]),

            ('Person', {
                '1': '1',
                '2': '2',
                '3': '3',
                '-': '',
                '?': '',
            }[f[5]]),

            ('PronType', {
                'p': 'Prs',
                'd': 'Dem',
                'i': 'Ind',
                's': 'Prs',
                'q': 'Int',
                'x': 'Prs',
                'z': 'Neg',
                'n': '',
                '-': '',
                '?': '',
            }[f[1]]),

            ('Reflex', ''),
        ])
        # P6 — Синтаксический тип

        if 'x' == f[1]:
            feat['Reflex'] = 'Yes'
    elif 'M' == f[0]:
        feat = collections.OrderedDict([
            ('Case', {
                'n': 'Nom',
                'g': 'Gen',
                'd': 'Dat',
                'a': 'Acc',
                'i': 'Ins',
                'l': 'Loc',
                'v': 'Voc',
                '-': '',
                '?': '',
            }[f[4]]),

            ('Gender', {
                'm': 'Masc',
                'f': 'Fem',
                'n': 'Neut',
                '-': '',
                '*': '',
                '?': '',
            }[f[2]]),

            ('NumForm', {
                'l': '',
                'd': 'Digit',
                'r': 'Digit',
                '-': '',
                '?': '',
            }[f[5]]),

            ('NumType', {
                'c': 'Card',
                'l': 'Sets',
                'o': 'Ord',
                '*': '',
                '-': '',
                '?': '',
            }[f[1]]),

            ('Number', {
                's': 'Sing',
                'p': 'Plur',
                '-': '',
                '*': '',
                '?': '',
            }[f[3]]),
        ])
    elif 'R' == f[0]:
        feat = collections.OrderedDict([
            ('Degree', {
                'p': 'Pos',
                'c': 'Cmp',
                's': 'Sup',
                '?': '',
            }[f[1]]),
        ])
    else:
        assert f[0] in {'C', 'H', 'I', 'Q', 'S', 'W', 'X', '?'}, f[0]
        feat = collections.OrderedDict()

    fv_map = '|'.join(['{}={}'.format(f, feat[f]) for f in feat.keys() if len(feat[f])])

    return fv_map if len(fv_map) else '_'


def join_gicr_composite(parts):
    result = parts[-1][:1] + ['', ''] + parts[-1][3:]

    for w in parts:
        result[1] += w[1]
        result[2] += w[2]

    return result


def convert_gicr_format(src_files, dest_file):
    source_content = ''
    for file_name in src_files:
        with open(file_name, 'rb') as sf:
            source_content += 'TEXTID={}'.format(os.path.basename(file_name)) + '\n\n'
            source_content += sf.read().decode('utf-8').strip() + '\n\n'

    target_corpora = []
    document_name = None
    sentence_id = 0
    word_id = 0
    join_words = []
    for row in source_content.split('\n'):
        row = row.strip()

        if row.startswith('TEXTID='):  # new document
            document_name = row.replace('TEXTID=', '').strip()
            sentence_id = 0
            word_id = 0
            continue

        if len(row) == 0:  # new sentence
            if word_id > 0:
                sentence_id += 1
            word_id = 0
            continue

        parsed = [col.strip() if len(col.strip()) else '_' for col in row.replace('\t', '\t\n').split('\t')] + ['_'] * 3
        if 0 == word_id:
            target_corpora.extend(['', ''])

            if document_name is not None:
                target_corpora.append('# newdoc id = {}'.format(document_name))
                document_name = None

            target_corpora.append('# sent_id = {}'.format(sentence_id + 1))

        if parsed[1].isdigit():
            assert len(parsed[2]) > 0
            assert parsed[3].startswith('[') and parsed[3].endswith(']'), parsed

            word = [
                '{}'.format(word_id + 1),  # ID
                parsed[2],  # FORM
                parsed[3][1:-1],  # LEMMA
                udpos_from_multexteastru(parsed[4]),  # UPOSTAG
                '_',  # XPOSTAG
                udfeats_from_multexteastru(parsed[4]),  # FEATS
                '_',  # HEAD
                '_',  # DEPREL
                '_',  # DEPS
                '_',  # MISC
            ]

            if '' == word[2]:  # LEMMA
                word[2] = word[1]
        else:
            assert 'P' == parsed[1]
            assert len(parsed[2]) > 0
            assert set(parsed[3:]) == {'_'}

            word = [
                '{}'.format(word_id + 1),  # ID
                parsed[2],  # FORM
                parsed[2],  # LEMMA
                'PUNCT',  # UPOSTAG
                '_',  # XPOSTAG
                '_',  # FEATS
                '_',  # HEAD
                '_',  # DEPREL
                '_',  # DEPS
                '_',  # MISC
            ]

        if 'X' == word[3]:
            word[2] = word[1]
        if 'NUM' == word[3] and word[2].startswith('#'):
            word[2] = word[1]

        if 'c+' == parsed[5]:
            assert len(join_words) > 0
            join_words.append(word)
            word = join_gicr_composite(join_words)
            join_words = []

        if len(join_words) or 'c-' == parsed[5]:
            join_words.append(word)
            continue

        target_corpora.append('\t'.join(word))
        word_id += 1

    target_corpora.extend(['', ''])
    with open(dest_file, 'wb') as df:
        df.write('\n'.join(target_corpora[2:]).encode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description='Convert GICR corpora to CoNLL-U format')
    parser.add_argument(
        'src_dir',
        type=str,
        help='Directory with source gicr files')
    parser.add_argument(
        'dest_file',
        type=argparse.FileType('wb'),
        help='Destination file')

    argv, _ = parser.parse_known_args()

    assert os.path.exists(argv.src_dir) and os.path.isdir(argv.src_dir)
    src_files = [os.path.join(argv.src_dir, f) for f in os.listdir(argv.src_dir) if f.endswith('.txt')]

    dest_file = argv.dest_file.name
    argv.dest_file.close()

    convert_gicr_format(src_files, dest_file)
