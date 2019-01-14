from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import csv
import os
import random
from conllu import parse


def create_dataset(src_files, dest_path):
    data = []

    for sf in src_files:
        with open(sf, 'rb') as f:
            sentences = parse(f.read().decode('utf-8'))

        for s in sentences:
            tokens = []
            labels = []

            for t in s:
                tokens.append(t['form'].replace(' ', '_'))
                labels.append('N' if t['misc'] is not None and 'SpaceAfter' in t['misc'] else 'Y')

            if not len(tokens):
                continue

            data.append((
                ' '.join(tokens),
                ' '.join(labels)
            ))

    random.shuffle(data)
    test_size = len(data) // 100
    test_data, train_data = data[:test_size], data[test_size:]
    del data

    with open(os.path.join(dest_path, 'test.txt'), 'w', newline='') as f:
        csvwriter = csv.writer(f, quoting=csv.QUOTE_ALL)
        for d in test_data:
            csvwriter.writerow(d)

    curr_id = 0
    while len(train_data):
        curr_data, train_data = train_data[:10000], train_data[10000:]
        curr_id += 1
        with open(os.path.join(dest_path, 'train-{}.txt'.format(curr_id)), 'w', newline='') as f:
            csvwriter = csv.writer(f, quoting=csv.QUOTE_ALL)
            for d in curr_data:
                csvwriter.writerow(d)


def main():
    parser = argparse.ArgumentParser(
        description='Create dataset from files with CoNLL-U markup')
    parser.add_argument(
        'src_path',
        type=str,
        help='Directory with source CoNLL-U files')
    parser.add_argument(
        'dest_path',
        type=str,
        help='Directory to store dataset files')

    argv, _ = parser.parse_known_args()
    assert os.path.exists(argv.src_path) and os.path.isdir(argv.src_path)
    assert not os.path.exists(argv.dest_path) or os.path.isdir(argv.dest_path)

    source_files = []
    for root, _, files in os.walk(argv.src_path):
        source_files.extend([os.path.join(root, file) for file in files if file.endswith('.conllu')])

    create_dataset(source_files, argv.dest_path)
