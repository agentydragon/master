import json
from prototype.lib import dbpedia
from prototype.lib import sentence
from prototype.lib import parse_xmls_to_protos

dbpedia_client = dbpedia.DBpediaClient(dbpedia.PUBLIC_DBPEDIA_ENDPOINT)

with open('testdata/Obama.txt.out') as f:
    corenlp_xml = f.read()
with open('testdata/Obama.txt') as f:
    plaintext = f.read()
with open('testdata/Obama.spotlight.json') as f:
    spotlight_json = json.load(f)

document_proto = parse_xmls_to_protos.document_to_proto(
    title = 'hello',
    document = sentence.SavedDocument(
        plaintext = plaintext,
        corenlp_xml = corenlp_xml,
        spotlight_json = spotlight_json,
        proto = None,
        title = 'hello'
    ),
    dbpedia_client = dbpedia_client
)

print(str(document_proto))
# TODO
