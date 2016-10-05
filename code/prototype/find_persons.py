"""
Usage:
    bazel run :find_persons > persons
"""

from prototype.lib import wikidata
from prototype.lib import wikidata_util
from prototype.lib import flags
import sys
import progressbar

flags.add_argument('--num_persons', type=int, default=10000)
flags.make_parser(description='TODO')
args = flags.parse_args()

wikidata_client = wikidata.WikidataClient()
print("Looking for %d persons..." % args.num_persons)

results = wikidata_client.wikidata_client.get_result_values("""
    SELECT *
    WHERE {
        # instance-of human
        ?person wdp:P31 wd:Q5 .

        ?person rdfs:label ?label .
        FILTER (lang(?label) = "en")
    }
    LIMIT %d
""" % args.num_persons)

#         ?person owl:sameAs ?dbpedia_person .
#         ?dbpedia_person foaf:isPrimaryTopicOf ?wikipedia_page .

bar = progressbar.ProgressBar()
persons = set()
for row in bar(results):
    id = wikidata_util.wikidata_entity_url_to_entity_id(row['person'])
    name = row['label']
#    wikipedia_page = row['wikipedia_page']
    wikipedia_page = '???'
    persons.add((name, id, wikipedia_page)) # add: because of multiplicities

    print(name, id, wikipedia_page)

for name, id, wikipedia_page in sorted(persons):
    print('%s\t%s' % (id, name))
    sys.stdout.flush()
