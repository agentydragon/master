import SPARQLWrapper

STANDARD_PREFIXES = """
PREFIX wd: <http://www.wikidata.org/entity/>
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

    def get_results(self, query):
        self.client.setQuery(STANDARD_PREFIXES + query)
        return self.client.query().convert()
