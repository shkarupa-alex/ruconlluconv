from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from xml.etree import ElementTree


def convert_oc_format(src_file, dest_file):
    source_annotation = ElementTree.parse(src_file)
    target_corpora = parse_annotation(source_annotation.getroot())

    target_corpora.append('')
    with open(dest_file, 'wb') as df:
        df.write('\n'.join(target_corpora).encode('utf-8'))


def parse_annotation(annotation):
    annotation_content = []

    assert 'annotation' == annotation.tag
    for text in annotation:
        if len(annotation_content):
            annotation_content.extend(['', ''])

        text_content = parse_text(text)
        annotation_content.extend(text_content)

    return annotation_content


def parse_text(text):
    text_content = []

    assert 'text' == text.tag
    for child in text:
        if 'tags' == child.tag:
            continue

        assert 'paragraphs' == child.tag
        for paragraph in child:
            if len(text_content):
                text_content.append('')

            par_id = paragraph.attrib['id']
            assert par_id is not None and len(par_id)

            text_content.append('# newpar id = {}'.format(par_id))

            paragraph_content = parse_paragraph(paragraph)
            text_content.extend(paragraph_content)

    if len(text_content):
        doc_name = text.attrib['name']
        assert doc_name is not None and len(doc_name)

        text_content.insert(0, '# newdoc id = {}'.format(doc_name))

    return text_content


def parse_paragraph(paragraph):
    paragraph_content = []

    assert 'paragraph' == paragraph.tag
    for sentence in paragraph:
        if len(paragraph_content):
            paragraph_content.append('')

        sentence_content = parse_sentence(sentence)
        paragraph_content.extend(sentence_content)

    return paragraph_content


def parse_sentence(sentence):
    sentence_content = []
    sent_id = None
    sent_text = None

    assert 'sentence' == sentence.tag
    if 'id' in sentence.attrib:
        sent_id = sentence.attrib['id'].strip()

    for child in sentence:
        if 'source' == child.tag:
            sent_text = child.text.replace('\n', ' ').strip()
            continue

        assert 'tokens' == child.tag
        for ti, token in enumerate(child):
            token_content = parse_token(ti, token)
            sentence_content.append(token_content)

    assert sent_text is not None

    # # Combine abbreviations
    # right_pos = len(sentence_content) - 1
    # while right_pos > 0:
    #     left_token = sentence_content[right_pos - 1].split('\t')
    #     right_token = sentence_content[right_pos].split('\t')
    #
    #     if '.' == right_token[1] and 'Abbr=Yes' in left_token[5] and \
    #             (left_token[1].islower() or 1 == len(left_token[1])):
    #         sent_text = sent_text.replace('{} .'.format(left_token[1]), '{}.'.format(left_token[1]))
    #         left_token[1] += '.'
    #         left_token[2] += '.'
    #         sentence_content = sentence_content[:right_pos - 1] + \
    #                            ['\t'.join(left_token)] + \
    #                            sentence_content[right_pos + 1:]
    #     right_pos -= 1
    #
    # # Reindex after abbreviations joins
    # for i in range(len(sentence_content)):
    #     word = sentence_content[i].split('\t')
    #     word[0] = '{}'.format(i + 1)
    #     sentence_content[i] = '\t'.join(word)

    sent_tokens = [s.split('\t')[1] for s in sentence_content]
    spaces_after = extract_space_after(sent_text, sent_tokens)

    for i in range(len(sentence_content)):
        if spaces_after[i]:
            continue
        word = sentence_content[i].split('\t')
        assert '_' == word[-1]
        word[-1] = 'SpaceAfter=No'
        sentence_content[i] = '\t'.join(word)

    if len(sentence_content):
        assert sent_text is not None
        sentence_content.insert(0, '# text = {}'.format(sent_text))

        assert sent_id is not None
        sentence_content.insert(0, '# sent_id = opcorpora_{}'.format(sent_id))

    return sentence_content


def parse_token(index, token):
    assert 'token' == token.tag

    id = '{}'.format(index + 1)

    form_value = token.attrib['text']
    assert form_value is not None and len(form_value)

    assert len(token) == 1 and 'tfr' == token[0].tag
    tfr = token[0]

    assert len(tfr) == 1 and 'v' == tfr[0].tag
    v = tfr[0]

    assert len(v) == 1 and 'l' == v[0].tag
    l = v[0]

    lemma_value = l.attrib['t']
    assert lemma_value is not None and len(lemma_value)

    assert len(l) > 0
    pos, feats = l[0], l[1:]

    pos_value, add_feat = parse_pos(pos)
    pos_swap, feats_value = parse_feats(feats)

    if '' != pos_swap and 'ADJ' != pos_value:
        assert 'NOUN' == pos_value and 'PROPN' == pos_swap, (pos_value, form_value)
        pos_value = pos_swap

    if len(add_feat):
        feats_value = feats_value.split('|') if '_' != feats_value else []
        feats_value += add_feat.split('|') if len(add_feat) else []
        feats_value = '|'.join(sorted(feats_value)) if len(feats_value) else '_'

    token_content = [
        id,
        form_value,
        lemma_value,
        pos_value,
        '_',  # XPOSTAG
        feats_value,
        '_',  # HEAD
        '_',  # DEPREL
        '_',  # DEPS
        '_',  # MISC
    ]

    return '\t'.join(token_content)


def parse_pos(pos):
    assert 'g' == pos.tag

    pos_value = pos.attrib['v']
    assert pos_value is not None and len(pos_value)

    pos_ud, add_feat = {
        'ADJF': ('ADJ', ''),
        'ADJS': ('ADJ', 'Variant=Short'),
        'ADVB': ('ADV', ''),
        'COMP': ('COMP', 'Degree=Cmp'),  # Adj or Adv or Pred
        'CONJ': ('CONJ', ''),  # CCONJ or SCONJ
        'GRND': ('VERB', 'VerbForm=Ger'),
        'INFN': ('VERB', 'VerbForm=Inf'),
        'INTJ': ('INTJ', ''),
        'LATN': ('X', ''),
        'NOUN': ('NOUN', ''),
        'NPRO': ('PRON', ''),
        'NUMB': ('NUM', ''),  # NumForm=Digit
        'NUMR': ('NUM', ''),
        'PNCT': ('PUNCT', ''),
        'PRCL': ('PART', ''),
        'PRED': ('PRED', ''),  # Verb or Adj or Adv (same as W in GICR)
        'PREP': ('ADP', ''), # ADJ or Adv or other (Noun, Verb, Pron)
        'PRTF': ('VERB', 'VerbForm=Part'),
        'PRTS': ('VERB', 'Variant=Short|VerbForm=Part'),
        'ROMN': ('NUM', ''),  # NumForm=Digit
        'SYMB': ('SYM', ''),
        'UNKN': ('X', ''),
        'VERB': ('VERB', 'VerbForm=Fin'),
    }[pos_value]

    return pos_ud, add_feat


def parse_feats(feats):
    pos_swap = ''
    feats_values = []

    feat_ud = {
        'ANim': ('', ''),  # no value
        'anim': ('', 'Animacy=Anim'),
        'inan': ('', 'Animacy=Inan'),

        'GNdr': ('', ''),  # no value
        'masc': ('', 'Gender=Masc'),
        'femn': ('', 'Gender=Fem'),
        'neut': ('', 'Gender=Neut'),
        'Ms-f': ('', 'Gender=Com'),
        'ms-f': ('', 'Gender=Com'),

        'NMbr': ('', ''),  # no value
        'sing': ('', 'Number=Sing'),
        'plur': ('', 'Number=Plur'),

        'Sgtm': ('', ''),  # has children
        'Pltm': ('', ''),  # has children
        'Fixd': ('', ''),  # no value

        'CAse': ('', ''),  # no value
        'nomn': ('', 'Case=Nom'),
        'gent': ('', 'Case=Gen'),
        'datv': ('', 'Case=Dat'),
        'accs': ('', 'Case=Acc'),
        'ablt': ('', 'Case=Ins'),
        'loct': ('', 'Case=Loc'),
        'voct': ('', 'Case=Voc'),
        'gen1': ('', 'Case=Gen'),
        'gen2': ('', 'Case=Par'),
        'acc2': ('', 'Case=Acc'),
        'loc1': ('', 'Case=Loc'),
        'loc2': ('', 'Case=Loc'),

        'Abbr': ('', 'Abbr=Yes'),
        'Name': ('PROPN', ''),
        'Surn': ('PROPN', ''),
        'Patr': ('PROPN', ''),
        'Geox': ('PROPN', ''),
        'Orgn': ('PROPN', ''),
        # 'Trad': ('PROPN', ''),
        'Subx': ('', ''),
        'Supr': ('', 'Degree=Sup'),
        'Qual': ('', ''),  # TODO: Degree=Pos ?
        'Apro': ('', ''),
        'Anum': ('', ''),
        'Poss': ('', ''),
        'V-ey': ('', ''),
        'V-oy': ('', ''),
        'Cmp2': ('', 'Degree=Cmp'),
        'V-ej': ('', ''),

        'ASpc': ('', ''),  # no value
        'perf': ('', 'Aspect=Perf'),
        'impf': ('', 'Aspect=Imp'),

        'TRns': ('', ''),  # no value
        'tran': ('', ''),
        'intr': ('', ''),

        'Impe': ('', ''),  # no value
        'Impx': ('', ''),  # no value
        # 'Mult': ('', ''),  # no value
        # 'Refl': ('', 'Reflex=Yes'),  # no value

        'PErs': ('', ''),  # no value
        '1per': ('', 'Person=1'),
        '2per': ('', 'Person=2'),
        '3per': ('', 'Person=3'),

        'TEns': ('', ''),  # no value
        'pres': ('', 'Tense=Pres'),
        'past': ('', 'Tense=Past'),
        'futr': ('', 'Tense=Fut'),

        'MOod': ('', ''),  # no value
        'indc': ('', 'Mood=Ind'),
        'impr': ('', 'Mood=Imp'),

        'INvl': ('', ''),  # no value
        'incl': ('', ''),  # TODO Clusivity=In
        'excl': ('', ''),  # TODO Clusivity=Ex

        'VOic': ('', ''),  # no value
        'actv': ('', 'Voice=Act'),
        'pssv': ('', 'Voice=Pass'),

        'Infr': ('', ''),
        'Slng': ('', ''),
        'Arch': ('', ''),
        'Litr': ('', ''),
        'Erro': ('', ''),
        'Dist': ('', ''),
        'Ques': ('', ''),
        'Dmns': ('', ''),
        'Prnt': ('', ''),  # H?
        'V-be': ('', ''),
        'V-en': ('', ''),
        'V-ie': ('', ''),
        'Prdx': ('', ''),
        'Coun': ('', ''),
        'Coll': ('', ''),
        'V-sh': ('', ''),
        'Af-p': ('', ''),
        'Inmx': ('', ''),
        'Vpre': ('', ''),
        'Anph': ('', ''),
        'Adjx': ('', ''),

    }

    for feat in feats:
        assert 'g' == feat.tag

        feat_value = feat.attrib['v']
        assert feat_value is not None and len(feat_value)

        p, f = feat_ud[feat_value]
        if len(p):
            assert not len(pos_swap)
            pos_swap = p
        feats_values.append(f)

    feats_values = [v for v in feats_values if len(v)]
    if len(feats_values):
        return pos_swap, '|'.join(sorted(feats_values))

    return '', '_'


def extract_space_after(text, tokens):
    if not len(tokens):
        return []

    text = text.replace('\t', ' ').replace('   ', ' ').replace('  ', ' ')
    spaces = [True] * len(tokens)

    joined_text = ''
    for i, t in enumerate(tokens):
        joined_no_space = joined_text + t
        assert text.startswith(joined_no_space) or len(tokens) < text.count(' ') + 1, (text, joined_no_space, t)

        joined_space = joined_no_space + ' '
        if text.startswith(joined_space):
            joined_text = joined_space
            continue

        spaces[i] = False
        joined_text = joined_no_space

    spaces[-1] = True
    assert len(spaces) == len(tokens)

    return spaces


def main():
    parser = argparse.ArgumentParser(description='Convert OC dataset to CoNLL-U format')
    parser.add_argument(
        'oc_src',
        type=argparse.FileType('rb'),
        help='MorphoRuEval2017 RNC dataset')
    parser.add_argument(
        'oc_dest',
        type=argparse.FileType('wb'),
        help='Destination CoNLL-U file')

    argv, _ = parser.parse_known_args()

    oc_src = argv.oc_src.name
    argv.oc_src.close()

    oc_dest = argv.oc_dest.name
    argv.oc_dest.close()

    convert_oc_format(oc_src, oc_dest)
