from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
from conllu import parse


def convert_mrg_format(src_files, target_file):
    content = ''

    for src_f in src_files:
        with open(src_f, 'rb') as f:
            content += f.read().decode('utf-8') + '\n\n'
    content = content.replace('\r', '')

    prepared = []
    for s in content.split('\n\n'):
        s = s.strip()

        for w in s.split('\n'):
            parts = w.split('\t')
            assert len(parts) in {0, 1, 5}

            if len(parts) == 5:
                parts = parts[:4] + ['_'] + parts[4:] + ['_'] * 5
            prepared.append('\t'.join(parts))
        prepared.append('')
    content = '\n'.join(prepared)

    sentences = parse(content)

    with open(target_file, 'wb') as f:
        for i, s in enumerate(sentences):
            if not len(s):
                continue
            f.write('# sent_id = mre17_test_{}\n'.format(i + 1).encode('utf-8'))
            f.write(s.serialize().encode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description='Convert MorphoRuEval2017 gold (GIKR) dataset')
    parser.add_argument(
        'mre_files',
        type=str,
        help='Directory with mre files')
    parser.add_argument(
        'mre_test',
        type=argparse.FileType('wb'),
        help='MorphoRuEval2017 gold test file')

    argv, _ = parser.parse_known_args()

    assert os.path.exists(argv.mre_files) and os.path.isdir(argv.mre_files)
    mre_files = [os.path.join(argv.mre_files, f) for f in os.listdir(argv.mre_files) if f.endswith('.txt')]

    mre_test = argv.mre_test.name
    argv.mre_test.close()

    convert_mrg_format(mre_files, mre_test)
