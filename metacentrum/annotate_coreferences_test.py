#!/usr/bin/python3

from google.protobuf import text_format
import get_training_samples
import annotate_coreferences
import parse_xmls_to_protos

document = parse_xmls_to_protos.parse_xml_to_proto('testdata/Obama.txt',
                                                   'testdata/Obama.txt.out')
print(text_format.MessageToString(document))

spotlight = annotate_coreferences.load_spotlight('testdata/Obama.spotlight.json')
annotate_coreferences.propagate_entities(document, spotlight)
print(text_format.MessageToString(document))

ts = get_training_samples.load_document(document)
td = get_training_samples.join_sentences_entities(ts)
samples = td.to_proto()
print(text_format.MessageToString(samples))
