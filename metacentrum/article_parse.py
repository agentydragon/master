import myutil

import xml.etree.ElementTree as ET
import json

myutil.load_cache()

# TODO: Spotlight does not extract numbers
#   (e.g., He directed his last movie in 1961. -- should be extracted)

class ArticleParse(object):
    def __init__(self):
        self.text = None
        self.document = None
        self.resources = None
        self.coreferences = None
        self.sentences = None

    def load(self, plaintext_path, spotlight_json_path, parse_xml_path):
        with open(plaintext_path) as f:
            self.text = f.read()

        tree = ET.parse(parse_xml_path)
        root = tree.getroot()
        assert root.tag == 'root'
        self.document = root[0]
        assert self.document.tag == 'document'

        self.load_sentences()
        self.load_spotlight_resources(spotlight_json_path)
        self.load_coreferences()

    def load_sentences(self):
        sentences = self.document[0]
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

            sentence_text = self.text[sentence_begin:sentence_end]
            sentence_id = int(sentence.attrib['id'])
            result[sentence_id] = {
                'start': sentence_begin,
                'end': sentence_end,
                'text': sentence_text,
                'tokens': trs
            }
        self.sentences = result

    def load_spotlight_resources(self, spotlight_json_path):
        with open(spotlight_json_path) as jsonfile:
            spotlight = json.loads(jsonfile.read())
        resources = spotlight['Resources']

        result = []

        for resource in resources:
            offset = int(resource['@offset'])
            surface_form = resource['@surfaceForm']
            end = offset+len(surface_form)
            actual_sf = self.text[offset:end]
            assert actual_sf == surface_form
            uri = resource['@URI']
            #print(offset, surface_form, uri)

            result.append({
                'start': offset,
                'end': end,
                'uri': uri,
                'surface_form': surface_form
            })

        self.resources = result

    def find_resources_between(self, start, end):
        for resource in self.resources:
            if resource['start'] >= start and resource['end'] <= end:
                yield resource

    def load_coreferences(self):
        coreferences = self.document.find('coreference')
        results = []
        for coreference in coreferences:
            best_resource = None

            mentions = []
            for mention in coreference.findall('mention'):
                if 'representative' in mention.attrib:
                    pass
                    # print("representative")
                sentenceid = int(mention.find('sentence').text)
                sentence = self.sentences[sentenceid]
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
                mention_actual_text = self.text[mention_start:mention_end]

                # print(mention_start, mention_end, mention_actual_text)
                # print("\theadword=" + mention_head)
                # print('\t', mention_start, mention_end, mention_text)

                for resource in self.find_resources_between(mention_start, mention_end):
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

        self.coreferences = results

    def annotate_sentences_with_wikidata_ids(self):
        for sentence_id, sentence in self.sentences.items():
            text = sentence['text']

            # entities: a) detected by Spotlight, b) added by coreference.
            #print(text)
            #print('Spotlight:')
            resources = list(self.find_resources_between(sentence['start'], sentence['end']))
            #for resource in resources:
            #    print('\t', resource['uri'])
            #print('Coreference:')
            coreference_uris = set()
            for coreference in self.coreferences:
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

    def get_sentences_with_wikidata_ids(self):
        json_data = []
        for sentence in self.sentences.values():
            json_data.append({
                'text': sentence['text'],
                # TODO: also say WHERE in the sentence are the IDs
                'wikidata_ids': list(sentence['wikidata_ids'])
            })
        return json_data
