dbpedia_client = sparql_client.SPARQLClient('http://dbpedia.org/sparql')

dbpedia_to_wikidata_cache = json_cache.JsonCache('dbpedia_to_wikidata_cache')

def load_cache():
    dbpedia_to_wikidata_cache.load()

def save_cache():
    dbpedia_to_wikidata_cache.save()

def dbpedia_uri_to_wikidata_id(uri):
    load_cache()

    if uri in dbpedia_to_wikidata_cache:
        return dbpedia_to_wikidata_cache[uri]

    results = sparql_client.get_results("""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?same
        WHERE { <%s> owl:sameAs ?same . }
    """ % uri)
    wikidata_entity = None
    for x in results['results']['bindings']:
        value = x['same']['value']
        if wikidata_util.is_wikidata_entity_url(value):
            wikidata_entity = wikidata_util.wikidata_entity_url_to_entity_id(value)
            break
    #print(uri, 'wikidata entity:', wikidata_entity)
    #print()
    dbpedia_to_wikidata_cache[uri] = wikidata_entity

    # TODO HAX
    save_cache()

    return wikidata_entity
