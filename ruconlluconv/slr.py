from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import re
from conllu import parse


def convert_slr_format(src_file, dest_file):
    with open(src_file, 'rb') as f:
        content = f.read().decode('utf-8').replace('\r', '')

    prepared = []
    for s in content.split('\n\n'):
        for w in s.split('\n'):
            parts = w.split('\t')
            assert len(parts) in {0, 1, 5}

            if len(parts) == 5:
                parts[1] = re.sub(' {2,}', ' ', parts[1])
                parts[2] = re.sub(' {2,}', ' ', parts[2])

                feats = parts[4]
                if '_' != feats:
                    feats = feats.replace('Variant=Brev', 'Variant=Short')
                    feats = feats.split('|')
                    feats = sorted(feats)
                    feats = '|'.join(feats)
                    parts[4] = feats

                parts = parts[:4] + ['_'] + parts[4:] + ['_'] * 5
            prepared.append('\t'.join(parts))
        prepared.append('\n')
    content = '\n'.join(prepared)

    sentences = parse(content)

    with open(dest_file, 'wb') as f:
        for i, s in enumerate(sentences):
            if not len(s):
                continue
            f.write('# sent_id = solarix_{}\n'.format(i + 1).encode('utf-8'))
            f.write(s.serialize().encode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description='Convert Solarix dataset')
    parser.add_argument(
        'src_file',
        type=argparse.FileType('rb'),
        help='Solarix dataset')
    parser.add_argument(
        'dest_file',
        type=argparse.FileType('wb'),
        help='Destination CoNLL-U file')

    argv, _ = parser.parse_known_args()

    src_file = argv.src_file.name
    argv.src_file.close()

    dest_file = argv.dest_file.name
    argv.dest_file.close()

    convert_slr_format(src_file, dest_file)
