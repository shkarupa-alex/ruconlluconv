from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import os
import tensorflow as tf
from nlpvocab import Vocabulary
from tf1 import f1_binary
from tfseqestimator import SequenceItemsClassifier, RnnType
from .input import input_feature_columns, train_input_fn


def build_estimator(ngram_vocab, model_path):
    # Prepare sequence estimator
    sequence_feature_columns = input_feature_columns(
        ngram_vocab=ngram_vocab,
        ngram_dimension=30,
    )
    estimator = SequenceItemsClassifier(
        label_vocabulary=['Y', 'N'],  # Not a boundary, Boundary
        sequence_columns=sequence_feature_columns,
        sequence_dropout=0.1,
        rnn_type=RnnType.REGULAR_BIDIRECTIONAL_LSTM,
        rnn_layers=[20],
        rnn_dropout=0.1,
        model_dir=model_path,
        config=tf.estimator.RunConfig().replace(save_summary_steps=10)  # TODO: check
    )

    # Add F1 metrics
    def custom_metrics(features, labels, predictions):
        weights_ = tf.to_float(tf.not_equal(features['words'], ''))

        token_labels = tf.math.not_equal(
            labels,
            tf.fill(tf.shape(labels), 'Y')
        )
        token_predictions = tf.math.not_equal(
            predictions['classes'],
            tf.fill(tf.shape(predictions['classes']), 'Y')
        )

        return {
            'f1': f1_binary(labels=token_labels, predictions=token_predictions, weights=weights_),
        }

    estimator = tf.contrib.estimator.add_metrics(estimator, custom_metrics)

    # Forward splitted words
    estimator = tf.contrib.estimator.forward_features(estimator, 'words')

    return estimator


def train_eval(ngram_vocab, model_path, train_data):
    estimator = build_estimator(ngram_vocab, model_path)

    metrics = None
    for _ in range(10):
        # Run training
        train_wildcard = os.path.join(train_data, 'train*.txt')
        train_steps = 1 if not os.path.exists(model_path) else None  # Make evaluation after first step
        estimator.train(input_fn=lambda: train_input_fn(
            wild_card=train_wildcard,
            batch_size=512,
        ), steps=train_steps)

        # Save vocabulary for TensorBoard
        ngram_vocab.update(['<UNK_{}>'.format(i) for i in range(1)])
        ngram_vocab.save(os.path.join(model_path, 'tensorboard.tsv'), Vocabulary.FORMAT_TSV_WITH_HEADERS)

        # Run evaluation
        eval_wildcard = os.path.join(train_data, 'test*.txt')
        metrics = estimator.evaluate(input_fn=lambda: train_input_fn(
            wild_card=eval_wildcard,
            batch_size=512,
        ))

    return metrics


def main():
    parser = argparse.ArgumentParser(description='Train, evaluate and export tfdstbd model')
    parser.add_argument(
        'train_data',
        type=str,
        help='Directory with TFRecord files for training')
    parser.add_argument(
        'ngram_vocab',
        type=str,
        help='Pickle-encoded ngram vocabulary file')
    parser.add_argument(
        'model_path',
        type=str,
        help='Path to store model checkpoints')

    argv, _ = parser.parse_known_args()
    assert os.path.exists(argv.train_data) and os.path.isdir(argv.train_data)
    assert os.path.exists(argv.ngram_vocab) and os.path.isfile(argv.ngram_vocab)
    assert not os.path.exists(argv.model_path) or os.path.isdir(argv.model_path)

    tf.logging.set_verbosity(tf.logging.INFO)

    # Load vocabulary
    ngram_vocab = Vocabulary.load(argv.ngram_vocab, format=Vocabulary.FORMAT_BINARY_PICKLE)

    metrics = train_eval(
        ngram_vocab=ngram_vocab,
        model_path=argv.model_path,
        train_data=argv.train_data,
    )
    if metrics is not None:
        print(metrics)
