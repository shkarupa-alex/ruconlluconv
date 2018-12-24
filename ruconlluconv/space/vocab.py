from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import tensorflow as tf
from nlpvocab import Vocabulary
from .input import train_input_fn


def extract_vocab(dest_path, min_freq=5, batch_size=256):
    wildcard = os.path.join(dest_path, 'train-*.txt')
    dataset = train_input_fn(wildcard, batch_size)
    iterator = dataset.make_one_shot_iterator()
    next_element = iterator.get_next()
    ngrams = next_element[0]['ngrams'].values

    vocab = Vocabulary()
    with tf.Session() as sess:
        while True:
            try:
                result = sess.run(ngrams)
            except tf.errors.OutOfRangeError:
                break
            result = [n.decode('utf-8') for n in result if n != b'' and n != b'<>']
            # only non-alpha, including suffixes, postfixes and other interesting parts
            result = [n for n in result if not n.isalpha()]
            vocab.update(result)
    vocab.trim(min_freq)

    return vocab


def main():
    parser = argparse.ArgumentParser(
        description='Extract ngram vocabulary from dataset')
    parser.add_argument(
        'src_path',
        type=str,
        help='Path with train files')
    parser.add_argument(
        'ngram_vocab',
        type=str,
        help='Output vocabulary file')

    argv, unparsed = parser.parse_known_args()
    assert os.path.exists(argv.src_path) and os.path.isdir(argv.src_path)

    tf.logging.set_verbosity(tf.logging.INFO)

    vocab = extract_vocab(argv.src_path)
    vocab.save(argv.ngram_vocab, Vocabulary.FORMAT_BINARY_PICKLE)
    vocab.save(os.path.splitext(argv.ngram_vocab)[0] + '.tsv', Vocabulary.FORMAT_TSV_WITH_HEADERS)
