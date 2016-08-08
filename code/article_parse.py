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
        self.coreferences = None
        self.sentences = None

    def load(self, plaintext_path, spotlight_json_path, parse_xml_path):
        self.load_coreferences()

    def find_resources_between(self, start, end):
        for resource in self.resources:
            if resource['start'] >= start and resource['end'] <= end:
                yield resource

    def load_coreferences(self):
        # 'or []': TODO: sometimes there are no coreferences
        coreferences = self.document.find('coreference') or []
        results = []
        for coreference in coreferences:
            best_resource = None

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
                if len(uris) == 1:
                    best_match = full_matches[0]['uri']
                else:
                    # print(full_matches[0])
                    print("fail: multiple urls:", uris)
                    # TODO: count occurrences and find the better one
            results.append({
                'mentions': mentions,
                'entity_uri': best_match
            })

        self.coreferences = results
        print('coreferences done')

    def annotate_sentences_with_wikidata_ids(self):
        print('annotating with wikidata ids')
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
                print(uri, '...')
                wikidata_ids.add(myutil.dbpedia_uri_to_wikidata_id(uri))
                print(uri, 'done')

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
