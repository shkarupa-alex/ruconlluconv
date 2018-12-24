from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse


def convert_rnc_format(src_file, dest_file):
    with open(src_file, 'rb') as sf:
        source_content = sf.read().decode('utf-8').strip()

    target_corpora = []
    document_name = None
    paragraph_name = None
    paragraph_id = 0
    sentence_id = 0
    word_id = 0
    for xxx, row in enumerate(source_content.split('\n')):
        row = row.strip()

        if row.startswith('==>'):  # new document
            document_name = row.replace('==>', '').replace('<==', '').strip()
            paragraph_id = 0
            sentence_id = 0
            word_id = 0
            continue

        if '==newfile==' == row:  # new paragraph
            paragraph_name = '{}'.format(paragraph_id + 1)
            if sentence_id > 0:
                paragraph_id += 1
            sentence_id = 0
            word_id = 0
            continue

        if len(row) == 0:  # new sentence
            if word_id > 0:
                sentence_id += 1
            word_id = 0
            continue

        if 0 == word_id:
            target_corpora.extend(['', ''])

            if document_name is not None:
                target_corpora.append('# newdoc id = {}'.format(document_name))
                document_name = None

            if paragraph_name is not None:
                target_corpora.append('# newpar id = {}'.format(paragraph_name))
                paragraph_name = None

            target_corpora.append('# sent_id = {}'.format(sentence_id + 1))

        parsed = [col.strip() if len(col.strip()) else '_' for col in row.replace('\t', '\t\n').split('\t')]

        if len(parsed) == 3 and 'PUNCT' == parsed[0]:
            continue

        word = [
            '{}'.format(word_id + 1),  # ID
            parsed[0],  # FORM
            parsed[1],  # LEMMA
            parsed[2],  # UPOSTAG
            '_',  # XPOSTAG
            parsed[3],  # FEATS
            '_',  # HEAD
            '_',  # DEPREL
            '_',  # DEPS
            parsed[4],  # MISC
        ]

        target_corpora.append('\t'.join(word))
        word_id += 1

    target_corpora.extend(['', ''])
    with open(dest_file, 'wb') as df:
        df.write('\n'.join(target_corpora[2:]).encode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description='Convert RNC dataset from MorphoRuEval2017 to CoNLL-U format')
    parser.add_argument(
        'mre_rnc',
        type=argparse.FileType('rb'),
        help='MorphoRuEval2017 RNC dataset')
    parser.add_argument(
        'rnc_dest',
        type=argparse.FileType('wb'),
        help='Destination CoNLL-U file')

    argv, _ = parser.parse_known_args()

    mre_rnc = argv.mre_rnc.name
    argv.mre_rnc.close()

    rnc_dest = argv.rnc_dest.name
    argv.rnc_dest.close()

    convert_rnc_format(mre_rnc, rnc_dest)
