#!/usr/bin/python3

import wikidata
import sys

michelle_obama = 'Q13133'
barack_obama = 'Q76'

triples = wikidata.get_all_triples_of_entity(michelle)

found = False
for sub, rel, obj in triples:
    if set(sub, obj) == set(michelle_obama, barack_obama):
        found = rel

if not found:
    print("Failed to find expected relation between Michelle and Barack Obama")
    sys.exit(1)
else:
    print("Relation between Michelle and Barack Obama: %s" % found)
