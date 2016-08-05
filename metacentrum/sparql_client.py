import SPARQLWrapper

dbpedia_sparql = SPARQLWrapper.SPARQLWrapper("http://dbpedia.org/sparql")
dbpedia_sparql.setReturnFormat(SPARQLWrapper.JSON)

STANDARD_PREFIXES = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

"""
# get entity name
SELECT *
WHERE { wd:Q1 rdfs:label ?b FILTER (langMatches(lang(?desc),"en")) }
"""

def get_results(query):
    dbpedia_sparql.setQuery(STANDARD_PREFIXES + query)
    return dbpedia_sparql.query().convert()
