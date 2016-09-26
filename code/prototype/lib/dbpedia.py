from prototype.lib import sparql_client
from prototype.lib import wikidata_util
from prototype.lib import zk
from prototype.lib import flags

flags.add_argument('--dbpedia_endpoint',
                   help=('DBpedia SPARQL endpoint. '
                         'Example: http://dbpedia.org/sparql, '
                         'http://hador:3030/wikidata/query'))

default_dbpedia_url = 'http://dbpedia.org/sparql'

def get_default_endpoint_url():
    endpoint = flags.parse_args().dbpedia_endpoint
    if endpoint:
        return endpoint

    zk_endpoint = zk.get_dbpedia_endpoint()
    if zk_endpoint:
        print("Grabbed DBpedia endpoint from ZK:", zk_endpoint)
        return ('http://%s/dbpedia-sameas/query' % zk_endpoint)

    raise Exception('No DBpedia endpoint available.')

    # print("WARN: Falling back to Wikimedia Foundation's DBpedia")
    # return default_dbpedia_url

class DBpediaClient(object):
    def __init__(self, endpoint=None):
        self.dbpedia_to_wikidata_cache = {}

        if not endpoint:
            endpoint = get_default_endpoint_url()

        self.dbpedia_client = sparql_client.SPARQLClient(endpoint)

    def dbpedia_uri_to_wikidata_id(self, uri):
        if uri in self.dbpedia_to_wikidata_cache:
            return self.dbpedia_to_wikidata_cache[uri]

        results = self.dbpedia_client.get_results("""
            SELECT ?same
            WHERE { <%s> owl:sameAs ?same . }
        """ % uri)
        wikidata_entity = None
        for x in results['results']['bindings']:
            value = x['same']['value']
            if wikidata_util.is_wikidata_entity_url(value):
                wikidata_entity = wikidata_util.wikidata_entity_url_to_entity_id(value)
                break
        self.dbpedia_to_wikidata_cache[uri] = wikidata_entity

        return wikidata_entity
