#!/usr/bin/python3

import wikidata
import sys

michelle_obama = 'Q13133'
barack_obama = 'Q76'

client = wikidata.WikidataClient()
client.persist_caches = False
triples = client.get_all_triples_of_entity(michelle_obama)

# wdt:P26 wd:Q76

found = False
print(triples)
for sub, rel, obj in triples:
    if set([sub, obj]) == set([michelle_obama, barack_obama]):
        found = rel

if not found:
    print("Failed to find expected relation between Michelle and Barack Obama")
    sys.exit(1)

if found != 'P26':
    print("Relation between Michelle and Barack Obama: %s, not P26 (married)" % found)
    sys.exit(1)

print("Relation between Michelle and Barack Obama: OK")
