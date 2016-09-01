#!/usr/bin/python3
# Input:
#   Each line:
#      (Article name) [\t] (JSON from hadoop/DocumentProcessorMapper)
# Output:
#   Each line:
#      (Relation) [\t] (Sentence expressing the relation)

import sys
import json
import xml.etree.ElementTree as ET
import parse_xmls_to_protos
import annotate_coreferences
import get_training_samples
from google.protobuf import text_format

import dbpedia
dbpedia.persist_cache = False

def process_article(article_name, mr_json):
    """
    Args:
        article_name str
        mr_json {"text": ..., "corenlp_xml": ..., "spotlight_json": ...}
    """

    plaintext = mr_json['text']
    document_root = ET.fromstring(mr_json['corenlp_xml'])

    #print(plaintext)

    document_proto = parse_xmls_to_protos.document_to_proto(document_root,
                                                            plaintext)

    spotlight_json = json.loads(mr_json['spotlight_json'])
    spotlight_json = annotate_coreferences.spotlight_to_mentions(spotlight_json)
    annotate_coreferences.propagate_entities(document_proto, spotlight_json)
    sentences = get_training_samples.load_document(document_proto)
    document_training_data = get_training_samples.join_sentences_entities(sentences)

    for relation, samples in document_training_data.training_data.items():
        for sample in samples:
            #sample_json = json.dumps({"sample": sample.SerializeToString()})
            sample_json = json.dumps({"sample": text_format.MessageToString(sample)})
            sys.stdout.write("%s\t%s\n" % (relation, sample_json))
            sys.stdout.flush()

def main():
    for line in sys.stdin:
        article_name, json_str = line.strip().split('\t')
        mr_json = json.loads(json_str)
        process_article(article_name, mr_json)

if __name__ == '__main__':
    main()
