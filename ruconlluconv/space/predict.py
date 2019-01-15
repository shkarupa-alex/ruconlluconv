from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import collections
import os
import tensorflow as tf
from conllu import parse
from nlpvocab import Vocabulary
from .train import build_estimator
from .input import predict_input_fn


def predict_spaces(ngram_vocab, model_path, source_rows):
    estimator = build_estimator(ngram_vocab, model_path)

    pred_rows = estimator.predict(input_fn=lambda: predict_input_fn(
        sentences=source_rows,
        batch_size=256,
    ))

    result = []
    for pr in pred_rows:
        row_words = []
        row_labels = []
        for w, l in zip(pr['words'], pr['classes']):
            if b'' == w:
                continue
            row_words.append(w.decode('utf-8'))
            row_labels.append(l[0].decode('utf-8'))
        row_labels[-1] = 'Y'
        result.append((row_words, row_labels))

    return result


def main():
    parser = argparse.ArgumentParser(description='Train, evaluate and export tfdstbd model')
    parser.add_argument(
        'ngram_vocab',
        type=str,
        help='Pickle-encoded ngram vocabulary file')
    parser.add_argument(
        'model_path',
        type=str,
        help='Path to store model checkpoints')
    parser.add_argument(
        'src_path',
        type=str,
        help='Path with source .conllu files')
    parser.add_argument(
        'dest_path',
        type=str,
        help='Path to store .conllu files with text and SpaceAfter attribute')

    argv, _ = parser.parse_known_args()
    assert os.path.exists(argv.ngram_vocab) and os.path.isfile(argv.ngram_vocab)
    assert os.path.isdir(argv.model_path)
    assert os.path.isdir(argv.src_path)
    assert not os.path.exists(argv.dest_path) or os.path.isdir(argv.dest_path)
    os.makedirs(argv.dest_path, exist_ok=True)

    tf.logging.set_verbosity(tf.logging.INFO)

    # Load vocabulary
    ngram_vocab = Vocabulary.load(argv.ngram_vocab, format=Vocabulary.FORMAT_BINARY_PICKLE)

    src_files = [f for f in os.listdir(argv.src_path) if f.endswith('.conllu')]
    for sf in src_files:
        with open(os.path.join(argv.src_path, sf), 'rb') as f:
            content = f.read().decode('utf-8').strip()
            sentences = [s for s in parse(content) if len(s)]

        source_rows = [' '.join([w['form'].replace(' ', '_') for w in s]) for s in sentences]
        rows_labels = predict_spaces(
            ngram_vocab=ngram_vocab,
            model_path=argv.model_path,
            source_rows=source_rows,
        )

        with open(os.path.join(argv.dest_path, sf), 'wb') as f:
            for sentence, words_labels in zip(sentences, rows_labels):
                text = []
                assert len(sentence) == len(words_labels[0]) == len(words_labels[1]), (sf, sentence)
                for i in range(len(sentence)):
                    assert sentence[i]['form'].replace(' ', '_') == words_labels[0][i]
                    text.append(sentence[i]['form'])
                    if words_labels[1][i] == 'N':
                        if sentence[i]['misc'] is None:
                            sentence[i]['misc'] = collections.OrderedDict()
                        sentence[i]['misc']['SpaceAfter'] = 'No'
                    else:
                        text.append(' ')
                sentence.metadata['text'] = ''.join(text).strip()
                f.write(sentence.serialize().encode('utf-8'))
