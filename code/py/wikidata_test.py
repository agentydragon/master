import wikidata
import sys

michelle_obama = 'Q13133'
barack_obama = 'Q76'
united_states = 'Q30'
potus = 'Q11696'

client = wikidata.WikidataClient()
#client.persist_caches = False
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

true_triples = client.get_triples_between_entities([
    barack_obama, michelle_obama, united_states, potus
])

print(true_triples)

truth = [(potus, 'P1001', united_states),
         (potus, 'P1308', barack_obama),
         (potus, 'P17', united_states),
         (michelle_obama, 'P26', barack_obama),
         (michelle_obama, 'P27', united_states),
         (united_states, 'P1313', potus),
         (united_states, 'P17', united_states),
         (united_states, 'P1906', potus),
         (united_states, 'P6', barack_obama),
         (barack_obama, 'P26', michelle_obama),
         (barack_obama, 'P27', united_states),
         (barack_obama, 'P39', potus)]

assert true_triples == truth

assert client.relation_exists(barack_obama, 'P39', potus)
assert not client.relation_exists(barack_obama, 'P40', potus)
