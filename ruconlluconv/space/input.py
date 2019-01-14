from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tfscc3d import sequence_categorical_column_with_vocabulary_list
from tensorflow import feature_column as core_columns
from tensorflow.contrib import feature_column as contrib_columns
from tfunicode import expand_split_words
from .feature import extract_case_length_features, extract_ngram_features


def input_feature_columns(ngram_vocab, ngram_dimension, ngram_oov=1, ngram_combiner='sum'):
    ngram_categorial_column = sequence_categorical_column_with_vocabulary_list(
        key='ngrams',
        vocabulary_list=ngram_vocab,
        dtype=tf.string,
        num_oov_buckets=ngram_oov,
    )
    ngram_embedding_column = core_columns.embedding_column(
        categorical_column=ngram_categorial_column,
        dimension=ngram_dimension,
        combiner=ngram_combiner,
    )

    return [
        ngram_embedding_column,
        contrib_columns.sequence_numeric_column('word_length'),
        contrib_columns.sequence_numeric_column('is_no_case'),
        contrib_columns.sequence_numeric_column('is_lower_case'),
        contrib_columns.sequence_numeric_column('is_upper_case'),
        contrib_columns.sequence_numeric_column('is_title_case'),
        contrib_columns.sequence_numeric_column('is_mixed_case'),
    ]


def features_from_documens(documents, ngram_minn=2, ngram_maxn=4):
    # Transformation should be equal with train dataset tokenization
    words = tf.string_split(documents)
    length, no_case, lower_case, upper_case, title_case, mixed_case = extract_case_length_features(words)
    ngrams = extract_ngram_features(words, ngram_minn, ngram_maxn)

    return {
        'document': documents,
        'words': tf.sparse_tensor_to_dense(words, default_value=''),  # Required to pass in prediction
        'ngrams': ngrams,
        'word_length': length,
        'is_no_case': no_case,
        'is_lower_case': lower_case,
        'is_upper_case': upper_case,
        'is_title_case': title_case,
        'is_mixed_case': mixed_case,
    }


def train_input_fn(wild_card, batch_size, threads_count=12, cycle_length=4):
    def _transform_examples(sentences, labels):
        features = features_from_documens(sentences)

        labels = tf.string_split(labels)
        labels = tf.sparse_tensor_to_dense(labels, default_value='Y')

        return features, labels

    with tf.name_scope('input'):
        files = tf.data.Dataset.list_files(wild_card)
        dataset = files.apply(tf.data.experimental.parallel_interleave(
            lambda filename: tf.data.experimental.CsvDataset(filename, record_defaults=[tf.string, tf.string]),
            cycle_length=cycle_length
        ))

        dataset = dataset.batch(batch_size)
        dataset = dataset.map(_transform_examples, num_parallel_calls=threads_count)
        dataset = dataset.repeat(5)
        dataset = dataset.shuffle(1000)
        dataset = dataset.prefetch(threads_count)

        return dataset


def predict_input_fn(sentences, batch_size, threads_count=12, cycle_length=4):
    with tf.name_scope('input'):
        dataset = tf.data.Dataset.from_tensor_slices(sentences)
        dataset = dataset.batch(batch_size)
        dataset = dataset.map(features_from_documens, num_parallel_calls=threads_count)
        dataset = dataset.prefetch(threads_count)

        return dataset
