import SPARQLWrapper
import time

STANDARD_PREFIXES = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdp: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

"""
# get entity name
SELECT *
WHERE { wd:Q1 rdfs:label ?b FILTER (langMatches(lang(?desc),"en")) }
"""

class SPARQLClient(object):
    def __init__(self, endpoint):
        self.client = SPARQLWrapper.SPARQLWrapper(endpoint)
        self.client.setReturnFormat(SPARQLWrapper.JSON)

    def get_results(self, query, retry=True):
        try:
            self.client.setQuery(STANDARD_PREFIXES + query)
            return self.client.query().convert()
        except ConnectionResetError, OSError:
            if retry:
                # Try retrying in case of transient failures
                time.sleep(10)
                return self.get_results(query, retry=False)
            else:
                raise
