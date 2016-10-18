from prototype.lib import wikidata
from prototype.lib import wikidata_util
from prototype.lib import flags
import paths
import sys
import progressbar

def main():
    flags.add_argument('--num_persons', type=int, default=10000)
    flags.add_argument('--write', type=bool, default=False)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    wikidata_client = wikidata.WikidataClient()
    print("Looking for %d persons..." % args.num_persons)

    results = wikidata_client.wikidata_client.get_result_values("""
        SELECT *
        WHERE {
            # instance-of human
            ?person wdp:P31 wd:Q5 .

            ?person rdfs:label ?label
            FILTER (lang(?label) = "en")

            BIND(URI(REPLACE(STR(?person), STR(wd:), "http://wikidata.org/entity/")) AS ?person2)
            ?dbpedia_person owl:sameAs ?person2 .
            ?dbpedia_person foaf:isPrimaryTopicOf ?wikipedia_page
        }
        LIMIT %d
    """ % args.num_persons)

    bar = progressbar.ProgressBar()
    persons = set()
    for row in bar(results):
        id = wikidata_util.wikidata_entity_url_to_entity_id(row['person'])
        name = row['label']
        wikipedia_page = row['wikipedia_page']
        persons.add((name, id, wikipedia_page)) # add: because of multiplicities

        print(name, id, wikipedia_page)

    f = sys.stdout
    if flags.parse_args().write:
        f = open(paths.ARTICLE_LIST_PATH, 'w')

    for name, id, wikipedia_page in sorted(persons):
        f.write('%s\t%s\t%s\n' % (id, name, wikipedia_page))
        f.flush()

    if flags.parse_args().write:
        f.close()

if __name__ == '__main__':
    main()
