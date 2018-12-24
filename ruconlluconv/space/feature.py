# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tfunicode import expand_split_chars, expand_char_ngrams
from tfunicode import transform_normalize_unicode, transform_wrap_with, transform_zero_digits
from tfunicode import transform_lower_case, transform_title_case, transform_upper_case, transform_string_replace

_MAX_LENGTH = 15.


def extract_case_length_features(input_words):
    input_words = transform_normalize_unicode(input_words, 'NFKC')
    input_chars = expand_split_chars(input_words)
    input_words_lower = transform_lower_case(input_words)
    input_words_upper = transform_upper_case(input_words)
    input_words_title = transform_title_case(input_words)

    chars_count = tf.sparse_reduce_sum_sparse(tf.SparseTensor(
        indices=input_chars.indices,
        values=tf.ones_like(input_chars.values, dtype=tf.float32),
        dense_shape=input_chars.dense_shape,
    ), axis=-1)

    word_length_values = tf.where(
        tf.greater(chars_count.values, _MAX_LENGTH),
        tf.fill(tf.shape(chars_count.values), _MAX_LENGTH),
        chars_count.values
    )
    word_length_values = tf.divide(word_length_values, _MAX_LENGTH)
    word_length_values.set_shape(input_words.values.shape)
    word_length = tf.SparseTensor(
        indices=input_words.indices,
        values=word_length_values,
        dense_shape=input_words.dense_shape,
    )

    no_case_value = tf.logical_and(
        tf.equal(input_words_lower.values, input_words_upper.values),
        tf.equal(input_words_upper.values, input_words_title.values)
    )
    no_case = tf.SparseTensor(
        indices=input_words.indices,
        values=tf.to_float(no_case_value),
        dense_shape=input_words.dense_shape
    )

    lower_case_value = tf.logical_and(
        tf.logical_not(no_case_value),
        tf.equal(input_words.values, input_words_lower.values)
    )
    lower_case = tf.SparseTensor(
        indices=input_words.indices,
        values=tf.to_float(lower_case_value),
        dense_shape=input_words.dense_shape
    )

    upper_case_value = tf.logical_and(
        tf.logical_not(no_case_value),
        tf.equal(input_words.values, input_words_upper.values)
    )
    upper_case = tf.SparseTensor(
        indices=input_words.indices,
        values=tf.to_float(upper_case_value),
        dense_shape=input_words.dense_shape
    )

    title_case_value = tf.logical_and(
        tf.logical_not(no_case_value),
        tf.equal(input_words.values, input_words_title.values)
    )
    title_case = tf.SparseTensor(
        indices=input_words.indices,
        values=tf.to_float(title_case_value),
        dense_shape=input_words.dense_shape
    )

    mixed_case_value = tf.logical_not(tf.logical_or(
        tf.logical_or(no_case_value, lower_case_value),
        tf.logical_or(upper_case_value, title_case_value)
    ))
    mixed_case = tf.SparseTensor(
        indices=input_words.indices,
        values=tf.to_float(mixed_case_value),
        dense_shape=input_words.dense_shape
    )

    return word_length, no_case, lower_case, upper_case, title_case, mixed_case


def extract_ngram_features(input_words, minn, maxn):
    input_words = transform_normalize_unicode(input_words, 'NFKC')
    input_words = transform_string_replace(input_words, [  # accentuation
        u'\u0060', u' \u0301', u'\u02CA', u'\u02CB', u'\u0300', u'\u0301'], [''] * 6)
    input_words = transform_lower_case(input_words)
    input_words = transform_zero_digits(input_words)
    input_words = transform_wrap_with(input_words, '<', '>')
    char_ngrams = expand_char_ngrams(input_words, minn, maxn, itself='ALONE')

    return char_ngrams
