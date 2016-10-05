import sys

from prototype.lib import dbpedia

client = dbpedia.DBpediaClient(endpoint=dbpedia.PUBLIC_DBPEDIA_ENDPOINT)

wikidata_id = client.dbpedia_uri_to_wikidata_id('http://dbpedia.org/resource/Barack_Obama')
print(wikidata_id)
assert wikidata_id == 'Q76'

wikidata_id = client.dbpedia_uri_to_wikidata_id('http://dbpedia.org/resource/Brentwood_School,_Essex')
print(wikidata_id)
assert wikidata_id == 'Q4961791'

uri_map = client.dbpedia_uris_to_wikidata_ids([
    'http://dbpedia.org/resource/Barack_Obama',
    'http://dbpedia.org/resource/Brentwood_School,_Essex',
    'http://dbpedia.org/resource/FASdfhdkjflhdsagalkdshmvalvjmld',
])

assert uri_map['http://dbpedia.org/resource/Barack_Obama'] == 'Q76'
assert uri_map['http://dbpedia.org/resource/Brentwood_School,_Essex'] == 'Q4961791'
assert 'http://dbpedia.org/resource/FASdfhdkjflhdsagalkdshmvalvjmld' not in uri_map
