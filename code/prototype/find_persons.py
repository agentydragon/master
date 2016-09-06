"""
Usage:
    bazel run :find_persons > persons
"""

from py import wikidata
from py import wikidata_util
import sys

wikidata_client = wikidata.WikidataClient()
wikidata_client.persist_caches = False
# ?person (instance of) (human)
print("Looking for persons...")
results = wikidata_client.wikidata_client.get_results("""
    SELECT ?person
    WHERE { ?person wdp:P31 wd:Q5 }
    LIMIT 1000
""")
results = results['results']['bindings']
for row in results:
    id = wikidata_util.wikidata_entity_url_to_entity_id(row['person']['value'])
    print(wikidata_client.get_entity_name(id))
    sys.stdout.flush()
