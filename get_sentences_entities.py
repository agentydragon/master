#!/usr/bin/python

"""
Creates list of Wikidata entities mentioned in each sentence
by joining Spotlight's entity linking with CoreNLP's coreference resolution.

Usage:
    ./get_sentences_entities.py \
        --article_plaintext_path=/mnt/crypto/data/wiki-articles/Allan_Dwan.txt \
        --article_parse_xml_path=Allan_Dwan.txt.out \
        --article_spotlight_json_path=Allan_Dwan.spotlight.json \
        --output_path=allan_dwan.json
"""

import argparse

parser = argparse.ArgumentParser(description='Propagace entity links through coreferences')
parser.add_argument('--article_plaintext_path', type=str)
parser.add_argument('--article_parse_xml_path', type=str)
parser.add_argument('--article_spotlight_json_path', type=str)
parser.add_argument('--output_path', type=str)
args = parser.parse_args()


# TODO: Spotlight does not extract numbers
#   (e.g., He directed his last movie in 1961. -- should be extracted)

import myutil

import requests
import xml.etree.ElementTree as ET
import json

myutil.load_cache()

text = open(args.article_plaintext_path).read()

tree = ET.parse(args.article_parse_xml_path)
root = tree.getroot()
assert root.tag == 'root'
document = root[0]
assert document.tag == 'document'

def load_spotlight_resources():
    with open(args.article_spotlight_json_path) as jsonfile:
        spotlight = json.loads(jsonfile.read())
    resources = spotlight['Resources']

    result = []

    for resource in resources:
        offset = int(resource['@offset'])
        surface_form = resource['@surfaceForm']
        end = offset+len(surface_form)
        actual_sf = text[offset:end]
        assert actual_sf == surface_form
        uri = resource['@URI']
        #print(offset, surface_form, uri)

        result.append({
            'start': offset,
            'end': end,
            'uri': uri,
            'surface_form': surface_form
        })

    return result

def find_resources_between(start, end):
    for resource in resources:
        if resource['start'] >= start and resource['end'] <= end:
            yield resource

def load_sentences():
    sentences = document[0]
    assert sentences.tag == 'sentences'
    # print('sentences:')
    result = {}
    for sentence in sentences:
        tokens = sentence[0]

        trs = {}
        sentence_begin = None
        sentence_end = None

        for token in tokens:
            token_id = int(token.attrib['id'])
            token_start = int(token.find('CharacterOffsetBegin').text)
            token_end = int(token.find('CharacterOffsetEnd').text)
            word = token.find('word').text
            trs[token_id] = {
                'start': token_start,
                'end': token_end,
                'word': word
            }

            if sentence_begin is None:
                sentence_begin = token_start
            sentence_end = token_end

        sentence_text = text[sentence_begin:sentence_end]
        sentence_id = int(sentence.attrib['id'])
        result[sentence_id] = {
            'start': sentence_begin,
            'end': sentence_end,
            'text': sentence_text,
            'tokens': trs
        }
    return result

sentencedict = load_sentences()

resources = load_spotlight_resources()

def load_coreferences():
    # print()
    # print('reporting coreferences')
    # print()
    coreferences = document.find('coreference')
    results = []
    for coreference in coreferences:
        best_resource = None

        mentions = []
        for mention in coreference.findall('mention'):
            if 'representative' in mention.attrib:
                pass
                # print("representative")
            sentenceid = int(mention.find('sentence').text)
            sentence = sentencedict[sentenceid]
            mention_start_id = int(mention.find('start').text)
            mention_start = sentence['tokens'][mention_start_id]['start']
            mention_end_id = int(mention.find('end').text) - 1
            mention_end = sentence['tokens'][mention_end_id]['end']
            mention_head_id = int(mention.find('head').text)
            mention_head = sentence['tokens'][mention_head_id]['word']

            mention_text = mention.find('text').text

            mentions.append({
                'sentence_id': sentenceid,
                'start': mention_start,
                'end': mention_end,
                'head_id': mention_head_id,
                'head_word': mention_head,
                'text': mention_text
            })

        full_matches = []
        for mention in mentions:
            mention_start = mention['start']
            mention_end = mention['end']
            mention_head = mention['head_word']
            mention_actual_text = text[mention_start:mention_end]

            # print(mention_start, mention_end, mention_actual_text)
            # print("\theadword=" + mention_head)
            # print('\t', mention_start, mention_end, mention_text)

            for resource in find_resources_between(mention_start, mention_end):
                if resource['surface_form'] == mention_text or resource['surface_form'] == mention_actual_text:
                    # print('\tFULL MATCH mention resource:', resource['uri'], 'surface_form:', resource['surface_form'])
                    full_matches.append(resource)
                    break
                else:
                    # print('\tmention resource:', resource['uri'], 'surface_form:', resource['surface_form'])
                    pass

        best_match = None
        if len(full_matches) > 0:
            # print("found full match:")
            uris = {resource['uri'] for resource in full_matches}
            assert len(uris) == 1
            # print(full_matches[0])
            best_match = full_matches[0]['uri']

        results.append({
            'mentions': mentions,
            'entity_uri': best_match
        })

    return results

coreferences = load_coreferences()
#print(coreferences)

# print()

for sentence_id, sentence in sentencedict.items():
    text = sentence['text']

    # entities: a) detected by Spotlight, b) added by coreference.
    #print(text)
    #print('Spotlight:')
    resources = list(find_resources_between(sentence['start'], sentence['end']))
    #for resource in resources:
    #    print('\t', resource['uri'])
    #print('Coreference:')
    coreference_uris = set()
    for coreference in coreferences:
        if coreference['entity_uri'] is None:
            continue
        is_here = False
        for mention in coreference['mentions']:
            if mention['sentence_id'] == sentence_id:
                is_here = True
                break
        if is_here:
            #print('\t', coreference['entity_uri'])
            coreference_uris.add(coreference['entity_uri'])

    all_uris = set()
    all_uris = all_uris.union(coreference_uris)
    all_uris = all_uris.union({resource['uri'] for resource in resources})
    # print(text)
    # print(all_uris)

    wikidata_ids = set()
    for uri in all_uris:
        wikidata_ids.add(myutil.dbpedia_uri_to_wikidata_id(uri))

    sentence['wikidata_ids'] = wikidata_ids

json_data = []
for sentence in sentencedict.values():
    json_data.append({
        'text': sentence['text'],
        # TODO: also say WHERE in the sentence are the IDs
        'wikidata_ids': list(sentence['wikidata_ids'])
    })
with open(args.output_path, 'w') as f:
    f.write(json.dumps(json_data))

myutil.save_cache()
