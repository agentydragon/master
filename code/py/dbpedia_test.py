from py import dbpedia

wikidata_id = dbpedia.dbpedia_uri_to_wikidata_id('http://dbpedia.org/resource/Barack_Obama')
print(wikidata_id)
assert wikidata_id == 'Q76'

wikidata_id = dbpedia.dbpedia_uri_to_wikidata_id('http://dbpedia.org/resource/Brentwood_School,_Essex')
print(wikidata_id)
assert wikidata_id == 'Q4961791'
