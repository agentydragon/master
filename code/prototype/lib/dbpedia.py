from prototype.lib import sparql_client
from prototype.lib import wikidata_util
from prototype.lib import zk
from prototype.lib import flags

flags.add_argument('--dbpedia_endpoint',
                   help=('DBpedia SPARQL endpoint. '
                         'Example: http://dbpedia.org/sparql, '
                         'http://hador:3030/wikidata/query'))

PUBLIC_DBPEDIA_ENDPOINT = 'http://dbpedia.org/sparql'

def get_default_endpoint_url():
    endpoint = flags.parse_args().dbpedia_endpoint
    if endpoint:
        return endpoint

    zk_endpoint = zk.get_dbpedia_endpoint()
    if zk_endpoint:
        print("Grabbed DBpedia endpoint from ZK:", zk_endpoint)
        return zk_endpoint

    raise Exception('No DBpedia endpoint available.')

    # print("WARN: Falling back to Wikimedia Foundation's DBpedia")
    # return PUBLIC_DBPEDIA_ENDPOINT

class DBpediaClient(object):
    def __init__(self, endpoint=None):
        self.dbpedia_to_wikidata_cache = {}

        if not endpoint:
            endpoint = get_default_endpoint_url()

        self.dbpedia_client = sparql_client.SPARQLClient(endpoint)

    def dbpedia_uris_to_wikidata_ids(self, uris):
        uris = list(sorted(uris))
        to_fetch = []
        result = {}
        for uri in uris:
            if uri in self.dbpedia_to_wikidata_cache:
                result[uri] = self.dbpedia_to_wikidata_cache[uri]
            else:
                to_fetch.append(uri)

        batch_size = 100
        for i in range(0, len(to_fetch), batch_size):
            uri_batch = to_fetch[i:i+batch_size]

            uris_list = ' '.join(map(sparql_client.url_to_query, uri_batch))
            results = self.dbpedia_client.get_result_values("""
                SELECT ?entity ?same
                WHERE {
                    VALUES ?entity { %s } .
                    ?entity owl:sameAs ?same .
                }
            """ % (uris_list))
            for row in results:
                uri, value = row['entity'], row['same']
                if wikidata_util.is_wikidata_entity_url(value):
                    wikidata_entity = wikidata_util.wikidata_entity_url_to_entity_id(value)
                    assert uri not in result
                    result[uri] = wikidata_entity
                    self.dbpedia_to_wikidata_cache[uri] = wikidata_entity
        return result

    def dbpedia_uri_to_wikidata_id(self, uri):
        if uri in self.dbpedia_to_wikidata_cache:
            return self.dbpedia_to_wikidata_cache[uri]

        results = self.dbpedia_client.get_result_values("""
            SELECT ?same
            WHERE { <%s> owl:sameAs ?same . }
        """ % uri)
        # TODO: LIMIT 1
        wikidata_entity = None
        for x in results:
            value = x['same']
            if wikidata_util.is_wikidata_entity_url(value):
                wikidata_entity = wikidata_util.wikidata_entity_url_to_entity_id(value)
                break
        self.dbpedia_to_wikidata_cache[uri] = wikidata_entity

        return wikidata_entity
