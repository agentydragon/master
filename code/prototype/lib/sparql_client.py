import SPARQLWrapper
import time
import urllib
import urllib.error

STANDARD_PREFIXES = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdp: <http://www.wikidata.org/prop/direct/>
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

    def get_results(self, query, retry=4):
        try:
            self.client.setQuery(STANDARD_PREFIXES + query)
            return self.client.query().convert()
        except (ConnectionResetError, OSError, urllib.error.URLError, SPARQLWrapper.SPARQLExceptions.EndPointInternalError) as e:
            error = e
            if not retry:
                raise
        # Try retrying in case of transient failures
        time_to_sleep = 10 * (2 ** (4 - retry))
        print(error, "Retrying in %d seconds (retries left:" % time_to_sleep, retry, ")")
        time.sleep(time_to_sleep)
        return self.get_results(query, retry=retry-1)
