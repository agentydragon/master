import json
from prototype.lib import dbpedia
from prototype.lib import sentence

dbpedia_client = dbpedia.DBpediaClient(dbpedia.PUBLIC_DBPEDIA_ENDPOINT)

with open('testdata/Obama.txt.out') as f:
    corenlp_xml = f.read()
with open('testdata/Obama.txt') as f:
    plaintext = f.read()
with open('testdata/Obama.spotlight.json') as f:
    spotlight_json = json.load(f)

document = sentence.SavedDocument(
    plaintext = plaintext,
    corenlp_xml = corenlp_xml,
    spotlight_json = spotlight_json,
    proto = None,
    title = 'hello',

    sentences = None,
    coreferences = None,
    spotlight_mentions = None,
)

document.add_proto_to_document(dbpedia_client)
print(str(document.sentences))
print(str(document.coreferences))
print(str(document.spotlight_mentions))
# TODO
