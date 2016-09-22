import SPARQLWrapper
import time
import urllib
import urllib.error

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

    def get_results(self, query, retry=5):
        try:
            self.client.setQuery(STANDARD_PREFIXES + query)
            return self.client.query().convert()
        except (ConnectionResetError, OSError, urllib.error.URLError, SPARQLWrapper.SPARQLExceptions.EndPointInternalError) as e:
            if retry:
                # Try retrying in case of transient failures
                print(e, "Retrying in 10 seconds (retries left:", retry, ")")
                time.sleep(10)
                return self.get_results(query, retry=retry-1)
            else:
                raise
