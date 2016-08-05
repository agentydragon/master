#!/usr/bin/python3

"""
TODO

Usage:
    TODO
"""

import xml.etree.ElementTree as ET
import sentence_pb2
from google.protobuf import text_format
import argparse
import os.path

def spans(array, y_fn):
    last_y = None
    span = []
    spans = []
    for x in array:
        this_y = y_fn(x)
        assert this_y is not None

        if last_y is None:
            last_y = this_y

        if this_y == last_y:
            span.append(x)
        else:
            spans.append((last_y, span))
            span = [x]
            last_y = this_y
    if len(span) > 0:
        spans.append((last_y, span))
    return spans

def find_token_in_sentence_by_id(sentence, token_id):
    for token in sentence.tokens:
        if token.id == token_id:
            return token

def handle_named_entity(sentence, start, end, document):
    # named entity is part of a coreference
    found = False
    for coreference in document.coreferences:
        for mention in coreference.mentions:
            if (mention.sentenceId == sentence.id and
                    mention.startWordId >= start.id and
                    (mention.endWordId - 1) <= end.id):
                found = True
                break
    if found:
        return

    mention_text = document.text[start.start_offset:end.end_offset]
    print("named entity: [", mention_text, ']')
    coreferences = document.coreferences.add()
    mention = coreferences.mentions.add()
    mention.sentenceId = sentence.id
    mention.startWordId = start.id
    mention.endWordId = end.id + 1
    mention.text = mention_text

def add_single_referenced_entities_to_coreferences(document):
    for sentence in document.sentences:
        last_ner = None
        last_ne_tokens = []

        ners_tokens = spans(sentence.tokens, lambda token: token.ner)
        #print(ners_tokens)
        for ner, tokens in ners_tokens:
            if ner == 'O':
                continue  # not a named entity

            if ner == 'ORDINAL':
                continue  # 'second', 'thirty-fourth', ...

            print(ner)
            #for token in tokens:
            #    print(token.lemma)
            #handle_named_entity(tokens[0].start_offset,
            #                    tokens[-1].end_offset,
            #                    document)
            handle_named_entity(sentence,
                                tokens[0], tokens[-1],
                                document)

def document_to_proto(document_root, plaintext):
    assert document_root.tag == 'root'
    document = document_root[0]
    assert document.tag == 'document'

    output_document = sentence_pb2.Document()
    output_document.text = plaintext

    for sentence_tag in document.find('sentences'):
        output_sentence = output_document.sentences.add()

        sentence_begin = None
        sentence_end = None

        for token in sentence_tag.find('tokens'):
            token_id = int(token.attrib['id'])
            token_start = int(token.find('CharacterOffsetBegin').text)
            token_end = int(token.find('CharacterOffsetEnd').text)

            output_token = output_sentence.tokens.add()
            output_token.id = token_id
            output_token.start_offset = token_start
            output_token.end_offset = token_end
            output_token.lemma = token.find('word').text
            output_token.pos = token.find('POS').text
            output_token.ner = token.find('NER').text

            if sentence_begin is None:
                sentence_begin = token_start
            sentence_end = token_end

        sentence_text = plaintext[sentence_begin:sentence_end]
        output_sentence.text = sentence_text
        output_sentence.id = int(sentence_tag.attrib['id'])

    for coreference_tag in (document.find('coreference') or []):
        output_coreference = output_document.coreferences.add()

        for mention_tag in coreference_tag.findall('mention'):
            sentenceid = int(mention_tag.find('sentence').text)
            #sentence = self.sentences[sentenceid]

            mention_start_id = int(mention_tag.find('start').text)
            #mention_start = sentence['tokens'][mention_start_id]['start']
            mention_end_id = int(mention_tag.find('end').text)
            #mention_end = sentence['tokens'][mention_end_id]['end']
            #mention_head_id = int(mention_tag.find('head').text)
            #mention_head = sentence['tokens'][mention_head_id]['word']

            output_mention = output_coreference.mentions.add()
            output_mention.sentenceId = sentenceid
            output_mention.startWordId = mention_start_id
            output_mention.endWordId = mention_end_id
            output_mention.text = mention_tag.find('text').text
            #output_mention.startCharOffset = mention_start
            #output_mention.endCharOffset = mention_end
            # TODO: headword

    add_single_referenced_entities_to_coreferences(output_document)

    return output_document

def parse_xml_to_proto(plaintext_path, parse_path):
    with open(plaintext_path) as f:
        plaintext = f.read()

    tree = ET.parse(parse_path)
    document_root = tree.getroot()
    return document_to_proto(document_root, plaintext)

def main():
    parser = argparse.ArgumentParser(description='todo')
    parser.add_argument('--plaintexts_dir')
    parser.add_argument('--parse_xmls_dir')
    parser.add_argument('--outputs_dir')
    args = parser.parse_args()

    if not os.path.isdir(args.outputs_dir):
        os.makedirs(args.outputs_dir)

    for root, subdirs, files in os.walk(args.plaintexts_dir):
        for filename in files:
            plaintext_path = os.path.join(root, filename)
            article_sanename = '.'.join(filename.split('.')[:-1])

            # (parse_xmls_dir)/Anarchism_in_France.txt.out
            parse_path = os.path.join(args.parse_xmls_dir, article_sanename + ".txt.out")
            if not os.path.isfile(parse_path):
                print(article_sanename, "skipped, not parsed")
                continue

            output_path = os.path.join(args.outputs_dir, article_sanename + ".parse.pb")
            if os.path.isfile(output_path):
                print(article_sanename, "already processed")
                continue

            print(article_sanename, "processing")

            output_document = parse_xml_to_proto(plaintext_path, parse_path)
            output_document.article_sanename = article_sanename

            print(text_format.MessageToString(output_document))
            with open(output_path, 'wb') as f:
                f.write(output_document.SerializeToString())


if __name__ == '__main__':
    main()
