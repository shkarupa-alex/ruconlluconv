# -*- coding: utf-8 -*-
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
        'H': 'H',  # TODO
        'I': 'INTJ',
        'M': 'NUM',
        'N': 'NOUN',
        'P': 'PRON',
        'Q': 'PART',
        'R': 'ADV',
        'S': 'ADP',
        'V': 'VERB',
        'W': 'PRED',  # Verb or Adj or Adv
        'X': 'X',
        '_': 'X',
        '?': 'X',
    }[features[0]]

    if 'N' == features[0]:
        pos = {
            'c': 'NOUN',
            'p': 'PROPN',
        }[features[1]]

    # if 'P' == features[0]:  # TODO
    #     pos = {
    #         'n': 'PRON',
    #         'a': 'ADJ',
    #         'r': 'ADV',
    #     }[features[6]]

    if 'X' == features[0] and len(features) == 2:
        pos = {
            'u': 'X',
            'd': 'NUM',
            'c': 'NUM',
            'p': 'X',
            'f': 'X',
            'z': 'X',  # TODO
            'r': 'X',  # saw only *
            's': 'X',
            'g': 'X',
            't': 'X',
            '-': 'X',
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

        if f[5] not in {'-', '?'}:
            feat['Case'] = {
                'l': 'Loc',
                'p': 'Par',
            }[f[5]]
    elif 'V' == f[0]:
        feat = collections.OrderedDict([
            ('Aspect', {
                'i': 'Imp',
                'p': 'Perf',
                'P': 'Perf',  # ?
                '-': '',
                '*': '',
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

            ('Variant', {
                'f': '',
                's': 'Short',
                '-': '',
                '?': '',
            }[f[11]]),

            ('VerbForm', {
                'i': 'Fin',
                'm': 'Fin',
                'n': 'Inf',
                'g': 'Ger',
                'p': 'Part',
                'x': '',
                '?': '',
            }[f[1]]),

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

            ('Number', {
                's': 'Sing',
                'p': 'Plur',
                '-': '',
                '*': '',
                '?': '',
            }[f[3]]),

            # TODO
            # ('NumForm', {
            #     'l': '',
            #     'd': 'Digit',
            #     'r': 'Digit',
            #     '-': '',
            #     '?': '',
            # }[f[5]]),

            ('NumType', {
                'c': 'Card',
                'l': 'Sets',
                'o': 'Ord',
                '*': '',
                '-': '',
                '?': '',
            }[f[1]]),
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


def break_combined_paragraphs(source_content):
    target_content = []

    last_id = 0
    for row in source_content.split('\n'):
        cols = row.split('\t')
        if not len(row.strip()) or len(cols) < 2:
            last_id = 0
            target_content.append(row)
            continue

        if 'P' == cols[1].strip():
            target_content.append(row)
            continue

        id = int(cols[1].strip())
        if id < last_id:
            target_content.extend(['', ''])

        last_id = id
        target_content.append(row)

    return '\n'.join(target_content)


def join_gicr_splits(source_corpora):
    processed_corpora = []

    for sentence in source_corpora.split('\n\n'):
        if '\tXf' not in sentence or '\n' not in sentence:
            processed_corpora.append(sentence)
            continue

        sentence = sentence.split('\n')

        for wi, word0 in enumerate(sentence):
            if '\tXf' not in word0:
                continue

            word0 = [w.strip() for w in word0.split('\t')]

            assert wi > 0
            word1 = [w.strip() for w in sentence[wi - 1].split('\t')]

            if 'P' != word1[1]:
                if word0[2].isalnum():
                    continue

                word1[3] = u'[{}{}]'.format(word1[3][1:-1], word0[3][1:-1])
                word1[2] = word1[2] + word0[2]
                sentence[wi - 1] = '\t'.join(word1)
                sentence[wi] = ''
                continue

            assert wi > 1
            word2 = [w.strip() for w in sentence[wi - 2].split('\t')]

            word2[3] = u'[{}{}{}]'.format(word2[3][1:-1], word1[2], word0[3][1:-1])
            word2[2] = word2[2] + word1[2] + word0[2]
            sentence[wi - 2] = '\t'.join(word2)
            sentence[wi - 1] = ''
            sentence[wi] = ''
        sentence = [w for w in sentence if len(w)]

        processed_corpora.append('\n'.join(sentence))

    return '\n\n'.join(processed_corpora)


def repair_broken_composites(source_content):
    target_content = []

    composite_start = []
    composite_end = []
    sentence_end = []
    for row in source_content.split('\n'):
        cols = row.split('\t')
        if not len(row.strip()) or len(cols) < 2:
            composite_start.append(False)
            composite_end.append(False)
            sentence_end.append(True)
            target_content.append(row)
            continue
        sentence_end.append(False)

        if len(cols) == 6:
            cols[5] = cols[5].replace('c-c+', '')
            composite_start.append('c-' in cols[5])
            composite_end.append('c+' in cols[5])
        else:
            composite_start.append(False)
            composite_end.append(False)
        row = '\t'.join(cols)

        target_content.append(row)

    assert len(composite_start) == len(composite_end) == len(sentence_end)

    composite_started = -1
    composite_errors = []
    for i, cs, ce, se in zip(range(len(composite_start)), composite_start, composite_end, sentence_end):
        assert not cs or not ce
        if cs:
            if composite_started >= 0:
                composite_errors.append(composite_started)
            composite_started = i
        if ce:
            composite_started = -1

        if se and composite_started >= 0:
            composite_errors.append(composite_started)
            composite_started = -1

    for idx, i in enumerate(composite_errors):
        cols = target_content[i].split('\t')
        assert len(cols) == 6, cols

        cols1 = target_content[i + 1].split('\t')
        if 5 == len(cols1):
            cols1.append('')
        assert len(cols1) == 6 or len(cols1) == 3 or len(cols1) == 1 and sentence_end[i + 1]

        if sentence_end[i + 1] or sentence_end[i + 2]:
            cols[5] = cols[5].replace('c-', '')
            composite_errors[idx] = 0
        elif len(cols1) == 6:
            cols[5] = cols[5].replace('c-', '')
            composite_errors[idx] = 0
        elif len(cols1) == 3 and cols1[2].strip()[0] not in {'.', '-'}:
            cols[5] = cols[5].replace('c-', '')
            composite_errors[idx] = 0
        elif len(cols1) == 3 and cols1[2].strip()[0] in {'.', '-'}:
            cols1 += ['', '', 'c+']
            composite_errors[idx] = 0

        target_content[i] = '\t'.join(cols)
        target_content[i + 1] = '\t'.join(cols1)

    assert 0 == sum(composite_errors)

    return '\n'.join(target_content)


def join_gicr_composite(parts):
    result = parts[-1][:1] + ['', ''] + parts[-1][3:]
    if 'PUNCT' == parts[-1][3]:
        result = parts[-2][:1] + ['', ''] + parts[-2][3:]

    for w in parts:
        result[1] += w[1]
        result[2] += w[2]

    return result


def convert_gicr_format(src_files, dest_file):
    source_content = ''
    for file_name in src_files:
        with open(file_name, 'rb') as sf:
            source_content += '\n\nTEXTID={}\n\n'.format(os.path.basename(file_name))
            source_content += sf.read().decode('utf-8').strip() + '\n\n'
            source_content = source_content.replace('\r', '')

    source_content = break_combined_paragraphs(source_content)
    source_content = join_gicr_splits(source_content)
    source_content = repair_broken_composites(source_content)

    target_corpora = []
    document_name = None
    sentence_id = 0
    word_id = 0
    join_words = []
    for row in source_content.split('\n'):
        row = row.strip()

        if row.startswith('TEXTID='):  # new document
            document_name = row.replace('TEXTID=', '').strip()
            word_id = 0
            continue

        if len(row.strip()) == 0:  # new sentence
            if word_id > 0:
                sentence_id += 1
            word_id = 0
            continue

        parsed = [col.strip() if len(col.strip()) else '_' for col in row.replace('\t', '\t\n').split('\t')] + ['_'] * 3
        if 0 == word_id:
            target_corpora.append('')

            if document_name is not None:
                target_corpora.append('# newdoc id = {}'.format(document_name))
                document_name = None

            target_corpora.append('# sent_id = gicr_gold_1.2_{}'.format(sentence_id + 1))

        if parsed[1].isdigit():
            assert len(parsed[2]) > 0
            assert parsed[3].startswith('[') and parsed[3].endswith(']'), parsed

            word = [
                '{}'.format(word_id + 1),  # ID
                parsed[2].replace(' ', '_'),  # FORM
                parsed[3][1:-1].replace(' ', '_'),  # LEMMA
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
            assert len(set(parsed[3:]) - {'_', 'c+'}) == 0

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

        word = '\t'.join(word)
        assert ' ' not in word, word

        target_corpora.append(word)
        word_id += 1

    target_corpora.append('')
    with open(dest_file, 'wb') as df:
        df.write('\n'.join(target_corpora[1:]).encode('utf-8'))


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
