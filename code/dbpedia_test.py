import dbpedia

dbpedia.persist_cache = False
wikidata_id = dbpedia.dbpedia_uri_to_wikidata_id('http://dbpedia.org/resource/Barack_Obama')
print(wikidata_id)
assert wikidata_id == 'Q76'
