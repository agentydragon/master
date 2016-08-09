#!/usr/bin/python3

"""
TODO

Usage:
    TODO
"""

import sentence_pb2
from google.protobuf import text_format
import argparse
import os.path
import dbpedia

import json

def spotlight_to_mentions(spotlight):
    resources = spotlight['Resources']
    output_mentions = []
    for resource in resources:
        mention = sentence_pb2.SpotlightMention()
        mention.start_offset = int(resource['@offset'])
        surface_form = resource['@surfaceForm']
        if surface_form is None:
            # TODO HAX?
            continue
        mention.end_offset = mention.start_offset + len(surface_form)
        mention.surface_form = surface_form
        mention.uri = resource['@URI']
        output_mentions.append(mention)
    return output_mentions

def load_document(path):
    document = sentence_pb2.Document()
    with open(path, 'rb') as f:
        document.ParseFromString(f.read())
    return document

def load_spotlight(spotlight_path):
    with open(spotlight_path) as jsonfile:
        spotlight = json.loads(jsonfile.read())
    return spotlight_to_mentions(spotlight)

def find_sentence_by_id(document, sentence_id):
    for sentence in document.sentences:
        if sentence.id == sentence_id:
            return sentence

def find_sentence_token(sentence, token_id):
    for token in sentence.tokens:
        if token.id == token_id:
            return token

def get_mention_start(document, mention):
    sentence = find_sentence_by_id(document, mention.sentenceId)
    token = find_sentence_token(sentence, mention.startWordId)

    # TODO: HAX
    if token is None:
        return None

    return token.start_offset

def get_mention_end(document, mention):
    sentence = find_sentence_by_id(document, mention.sentenceId)
    token = find_sentence_token(sentence, mention.endWordId - 1)

    # TODO: HAX
    if token is None:
        return None

    return token.end_offset

def find_resources_between(spotlight, start, end):
    for resource in spotlight:
        if resource.start_offset >= start and resource.end_offset <= end:
            yield resource

def propagate_entities(document, spotlight):
    for coreference in document.coreferences:
        best_resource = None
        full_matches = []
        for mention in coreference.mentions:
            mention_start = get_mention_start(document, mention)
            mention_end = get_mention_end(document, mention)

            # TODO: HAX
            if mention_end is None:
                continue

            mention_text = mention.text
            mention_actual_text = document.text[mention_start:mention_end]
            print((mention_text, mention_actual_text))
            # TODO: check this out.
            # assert mention_text == mention_actual_text
            for resource in find_resources_between(spotlight, mention_start, mention_end):
                if resource.surface_form == mention_text or resource.surface_form == mention_actual_text:
                    # print('\tFULL MATCH mention resource:', resource['uri'], 'surface_form:', resource['surface_form'])
                    full_matches.append(resource)
                    break
                else:
                    # print('\tmention resource:', resource['uri'], 'surface_form:', resource['surface_form'])
                    pass
            best_match = None
            if len(full_matches) > 0:
                # print("found full match:")
                uris = {resource.uri for resource in full_matches}
                if len(uris) == 1:
                    best_match = full_matches[0].uri
                else:
                    # print(full_matches[0])
                    print("fail: multiple urls:", uris)
                    # TODO: count occurrences and find the better one
            if best_match:
                wikidata_id = dbpedia.dbpedia_uri_to_wikidata_id(best_match)
                if wikidata_id:
                    coreference.wikidataEntityId = wikidata_id # best_match
                else:
                    print("cannot get wikidata id:", best_match)

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--input_protos_dir', required=True)
    parser.add_argument('--spotlight_dir', required=True)
    parser.add_argument('--output_protos_dir', required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.output_protos_dir):
        os.makedirs(args.output_protos_dir)

    for root, subdirs, files in os.walk(args.input_protos_dir):
        for filename in files:
            input_proto_path = os.path.join(root, filename)
            document = sentence_pb2.Document()
            with open(input_proto_path, 'rb') as f:
                document.ParseFromString(f.read())

            article_sanename = document.article_sanename
            spotlight_path = os.path.join(args.spotlight_dir, article_sanename + ".spotlight.json")
            if not os.path.isfile(spotlight_path):
                print(article_sanename, "skipped, parsed but not spotlighted")
                continue

            output_path = os.path.join(args.output_protos_dir, article_sanename + ".propagated.pb")
            if os.path.isfile(output_path):
                print(article_sanename, "already processed")
                continue

            print(article_sanename, "processing")

            spotlight = load_spotlight(spotlight_path)
            propagate_entities(document, spotlight)

            print(text_format.MessageToString(document))
            with open(output_path, 'wb') as f:
                f.write(document.SerializeToString())

if __name__ == '__main__':
    main()
