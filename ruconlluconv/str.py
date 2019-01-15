from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import re
from conllu import parse


def sentence_key(sentence):
    skip_pos = {'PUNCT', 'SYM'}
    tokens = [t['form'] for t in sentence if t['upostag'] not in skip_pos]

    key = ' '.join(tokens).replace('_', ' ').strip().lower()
    key = re.sub(r'\s+', ' ', key, flags=re.UNICODE)

    return key


def extract_mre_diff(ud_files, mre_file, mre_diff):
    known_keys = set()
    for ud_f in ud_files:
        with open(ud_f, 'rb') as f:
            content = f.read().decode('utf-8')
            sentences = parse(content)
            keys = [sentence_key(s) for s in sentences]
            known_keys.update(keys)

    with open(mre_file, 'rb') as f:
        content = f.read().decode('utf-8').replace('\r', '')

    prepared = []
    for s in content.split('\n\n'):
        for w in s.split('\n'):
            parts = w.split('\t')
            assert len(parts) in {0, 1, 5}

            if len(parts) == 5:
                parts[4] = parts[4].replace('NumForm=Digit', '').replace('||', '|').strip('|')
                parts = parts[:4] + ['_'] + parts[4:] + ['_'] * 5
            prepared.append('\t'.join(parts))
        prepared.append('\n')
    content = '\n'.join(prepared)

    sentences = parse(content)
    sentences = [s for s in sentences if sentence_key(s) not in known_keys]

    with open(mre_diff, 'wb') as f:
        for i, s in enumerate(sentences):
            if not len(s):
                continue
            f.write('# sent_id = syntagrus_add_mre17_{}\n'.format(i + 1).encode('utf-8'))
            f.write(s.serialize().encode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description='Extract STR additional sentences from MorphoRuEval2017 dataset')
    parser.add_argument(
        'ud_files',
        type=str,
        help='Directory with UD files')
    parser.add_argument(
        'mre_train',
        type=argparse.FileType('rb'),
        help='MorphoRuEval2017 train file')
    parser.add_argument(
        'mre_diff',
        type=argparse.FileType('wb'),
        help='MorphoRuEval2017 diff file')

    argv, _ = parser.parse_known_args()

    assert os.path.exists(argv.ud_files) and os.path.isdir(argv.ud_files)
    ud_files = [os.path.join(argv.ud_files, f) for f in os.listdir(argv.ud_files) if f.endswith('.conllu')]

    mre_train = argv.mre_train.name
    argv.mre_train.close()

    mre_diff = argv.mre_diff.name
    argv.mre_diff.close()

    extract_mre_diff(ud_files, mre_train, mre_diff)
