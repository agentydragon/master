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

# ?person instance-of human
results = wikidata_client.wikidata_client.get_results("""
    SELECT *
    WHERE { ?person wdp:P31 wd:Q5
          . ?person rdfs:label ?label
          . FILTER (lang(?label) = "en") }
    LIMIT %d
""" % args.num_persons)
results = results['results']['bindings']
bar = progressbar.ProgressBar()
names = set()
for row in bar(results):
    # print(row['person']['value'], row['label']['value'], row['label'])
    names.add(row['label']['value']) # add: because of multiplicities

    # id = wikidata_util.wikidata_entity_url_to_entity_id(row['person']['value'])
    # names.append(wikidata_client.get_entity_name(id))

for name in sorted(names):
    print(name)
    sys.stdout.flush()
# print(len(names))
