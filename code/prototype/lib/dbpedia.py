from prototype.lib import sparql_client
from prototype.lib import wikidata_util

dbpedia_url = 'http://dbpedia.org/sparql'

class DBpediaClient(object):
    def __init__(self, endpoint=None):
        self.dbpedia_to_wikidata_cache = {}
        if endpoint is None:
            endpoint = dbpedia_url
        self.dbpedia_client = sparql_client.SPARQLClient('http://dbpedia.org/sparql')

    def dbpedia_uri_to_wikidata_id(self, uri):
        if uri in self.dbpedia_to_wikidata_cache:
            return self.dbpedia_to_wikidata_cache[uri]

        results = dbpedia_client.get_results("""
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