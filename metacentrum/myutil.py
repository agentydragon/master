import os
import os.path
import json
import SPARQLWrapper

cache_dir = 'cache'
if not os.path.isdir(cache_dir):
    os.makedirs(cache_dir)

dbpedia_to_wikidata_cache = {}
cache_path = cache_dir + '/dbpedia_to_wikidata_cache.json'

wikidata_relations_cache = {}
wikidata_cache_path = cache_dir + '/wikidata_cache.json'

wikidata_entity_prefix = 'http://www.wikidata.org/entity/'
wikidata_property_prefix = 'http://www.wikidata.org/wiki/Property:'

dbpedia_sparql = SPARQLWrapper.SPARQLWrapper("http://dbpedia.org/sparql")
dbpedia_sparql.setReturnFormat(SPARQLWrapper.JSON)

def load_cache():
    if os.path.isfile(cache_path):
        with open(cache_path) as f:
            dbpedia_to_wikidata_cache = json.loads(f.read())
    if os.path.isfile(wikidata_cache_path):
        with open(wikidata_cache_path) as f:
            wikidata_relations_cache = json.loads(f.read())

def save_cache():
    with open(cache_path, 'w') as f:
        f.write(json.dumps(dbpedia_to_wikidata_cache))
    with open(wikidata_cache_path, 'w') as f:
        f.write(json.dumps(wikidata_relations_cache))

def wikidata_entity_url_to_entity_id(url):
    assert url.startswith(wikidata_entity_prefix)
    return url[len(wikidata_entity_prefix):]

def wikidata_property_url_to_property_id(url):
    assert url.startswith(wikidata_property_prefix)
    return url[len(wikidata_property_prefix):]

def is_wikidata_entity_url(url):
    return url.startswith(wikidata_entity_prefix)

def relation_interesting(relation):
    if relation in ['http://schema.org/description',
                    'http://www.w3.org/2004/02/skos/core#altLabel',
                    'http://www.w3.org/2000/01/rdf-schema#label']:
        return False
    if 'wikidata' not in relation:
        return False
    return True

def normalize_relation(rel):
    # http://www.wikidata.org/entity/P9999c => http://www.wikidata.org/wiki/Property:P9999
    if rel.startswith('http://www.wikidata.org/entity/P') and rel.endswith('s'):
        rel = rel[:-1]
        rel = rel.replace('http://www.wikidata.org/entity/P',
                          'http://www.wikidata.org/wiki/Property:P')
    if rel.startswith('http://www.wikidata.org/entity/P') and rel.endswith('c'):
        rel = rel[:-1]
        rel = rel.replace('http://www.wikidata.org/entity/P',
                          'http://www.wikidata.org/wiki/Property:P')
    return rel

def is_statement(url):
    # uuid-like stuff (statements)
    dashes = 0
    for c in url:
        if c == '-':
            dashes += 1
#        if other.startswith('http://www.wikidata.org/entity/') and dashes == 4:
#            other = other.replace('http://www.wikidata.org/entity/Q',
#                              'http://www.wikidata.org/entity/statement/Q')

    return url.startswith('http://www.wikidata.org/entity/') and dashes == 4

def collect_forward_properties(wikidata_id):
    print('forward for', wikidata_id)

    dbpedia_sparql.setQuery("""
        PREFIX wd: <http://www.wikidata.org/entity/>
        SELECT ?rel ?other
        WHERE { wd:%s ?rel ?other . }
    """ % wikidata_id)
    results = dbpedia_sparql.query().convert()

    properties=[]
    for x in results['results']['bindings']:
        rel = x['rel']['value']
        other = x['other']['value']

        # skip uninteresting stuff
        if not relation_interesting(rel):
            continue
        rel = normalize_relation(rel)
        if is_statement(other):
            continue
        if '/Q' not in other:
            continue
        if '/P' not in rel:
            continue
        other = wikidata_entity_url_to_entity_id(other)
        rel = wikidata_property_url_to_property_id(rel)

        triple = (wikidata_id, rel, other)
        print(triple)
        properties.append(triple)
    return properties

# TODO DRY
def collect_backward_properties(wikidata_id):
    dbpedia_sparql.setQuery("""
        PREFIX wd: <http://www.wikidata.org/entity/>
        SELECT ?rel ?other
        WHERE { ?other ?rel wd:%s . }
    """ % wikidata_id)
    print('backward for', wikidata_id)
    results = dbpedia_sparql.query().convert()

    properties=[]
    for x in results['results']['bindings']:
        rel = x['rel']['value']
        other = x['other']['value']

        # skip uninteresting stuff
        if not relation_interesting(rel):
            continue
        rel = normalize_relation(rel)
        if is_statement(other):
            continue
        if '/Q' not in other:
            continue
        if '/P' not in rel:
            continue
        other = wikidata_entity_url_to_entity_id(other)
        rel = wikidata_property_url_to_property_id(rel)
        triple = (other, rel, wikidata_id)
        print(triple)
        properties.append(triple)
    return properties

def wikidata_query(wikidata_id):
    if wikidata_id in wikidata_relations_cache:
        return wikidata_relations_cache[wikidata_id]

    properties = []
    properties.extend(collect_forward_properties(wikidata_id))
    properties.extend(collect_backward_properties(wikidata_id))

    wikidata_relations_cache[wikidata_id] = properties
    return properties

def dbpedia_uri_to_wikidata_id(uri):
    if uri in dbpedia_to_wikidata_cache:
        return dbpedia_to_wikidata_cache[uri]
    sparql = SPARQLWrapper.SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?same
        WHERE { <%s> owl:sameAs ?same . }
    """ % uri
    #print(query)
    sparql.setQuery(query)
    sparql.setReturnFormat(SPARQLWrapper.JSON)
    results = sparql.query().convert()
    wikidata_entity = None
    for x in results['results']['bindings']:
        value = x['same']['value']
        if is_wikidata_entity_url(value):
            wikidata_entity = wikidata_entity_url_to_entity_id(value)
            break
    #print(uri, 'wikidata entity:', wikidata_entity)
    #print()
    dbpedia_to_wikidata_cache[uri] = wikidata_entity
    return wikidata_entity

