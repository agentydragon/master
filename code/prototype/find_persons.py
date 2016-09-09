"""
Usage:
    bazel run :find_persons > persons
"""

from py import wikidata
from py import wikidata_util
import sys

NUM_PERSONS = 10000

wikidata_client = wikidata.WikidataClient()
wikidata_client.persist_caches = False
# ?person (instance of) (human)
print("Looking for %d persons..." % NUM_PERSONS)
results = wikidata_client.wikidata_client.get_results("""
    SELECT ?person
    WHERE { ?person wdp:P31 wd:Q5 }
    LIMIT %d
""" % NUM_PERSONS)
results = results['results']['bindings']
names = []
for row in results:
    id = wikidata_util.wikidata_entity_url_to_entity_id(row['person']['value'])
    names.append(wikidata_client.get_entity_name(id))

for nam in sorted(names):
    print(name)
    sys.stdout.flush()
