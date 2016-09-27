from prototype.lib import wikidata
from prototype.lib import flags

flags.add_argument('--limit', type=int, default=None)
flags.make_parser(description='TODO')
args = flags.parse_args()

properties = [21, 22, 25, 27, 7, 9, 26, 451, 40, 43, 44, 1038, 103, 69, 172,
              106, 101, 108, 140, 91, 1066, 802, 185, 53, 512, 552, 734, 1037,
              1344, 1340, 1303, 1399, 1416, 54, 413, 1532, 241, 410, 598, 607,
              452, 159, 807, 31, 112, 740, 1387, 1313, 1290]
propparts = ""
for property in properties[:-1]:
    propparts += ('{ ?a wdt:P%s ?c } UNION\n' % property)
query = """
    SELECT ?a ?b ?c
    WHERE {
        %s
    }
"""
if args.limit:
    query += "LIMIT " + str(args.limit)

results = wikidata.WikidataClient().wikidata_client.get_results(query)
for row in results['results']['bindings']:
    subject, relation, object = row['a']['value'], row['b']['value'], row['c']['value']
    triple = wikidata_util.transform_relation(subject, relation, object)
    if not triple:
        continue

    subject, relation, object = triple
    print(subject, relation, object)
