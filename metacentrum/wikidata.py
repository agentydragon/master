import json_cache
import wikidata_util
import sparql_client

wikidata_relations_cache = json_cache.JsonCache(cache_dir + '/wikidata_cache.json')
name_cache = JsonCache(cache_dir + '/name_cache.json')

def load_cache():
    wikidata_relations_cache.load()
    name_cache.load()

def save_cache():
    wikidata_relations_cache.save()
    name_cache.save()

def collect_forward_properties(wikidata_id):
    print('forward for', wikidata_id)
    results = sparql_client.get_results("""
        SELECT ?rel ?other
        WHERE { wd:%s ?rel ?other . }
    """ % wikidata_id)

    properties=[]
    for x in results['results']['bindings']:
        subject = wikidata_util.wikidata_entity_prefix + wikidata_id
        rel = x['rel']['value']
        other = x['other']['value']

        triple = transform_relation(subject, rel, other)
        if triple:
            print(triple)
            properties.append(triple)
    return properties

# TODO DRY
def collect_backward_properties(wikidata_id):
    print('backward for', wikidata_id)
    results = sparql_client.get_results("""
        SELECT ?rel ?other
        WHERE { ?other ?rel wd:%s . }
    """ % wikidata_id)

    properties=[]
    for x in results['results']['bindings']:
        rel = x['rel']['value']
        other = x['other']['value']
        subject = wikidata_util.wikidata_entity_prefix + wikidata_id

        triple = transform_relation(other, rel, subject)
        if triple:
            print(triple)
            properties.append(triple)
    return properties

def get_all_triples_of_entity(wikidata_id):
    load_cache()

    if wikidata_id in wikidata_relations_cache:
        return wikidata_relations_cache[wikidata_id]

    properties = []
    properties.extend(collect_forward_properties(wikidata_id))
    properties.extend(collect_backward_properties(wikidata_id))

    wikidata_relations_cache[wikidata_id] = properties

    # TODO HAX
    save_cache()

def fetch_label(entity_id):
    results = sparql_client.get_results("""
        SELECT ?label
        WHERE { wd:%s rdfs:label ?label . FILTER (langMatches(lang(?label),"en")) }
    """ % entity_id)
    if len(results['results']['bindings']) == 0:
        return None
    else:
        return results['results']['bindings'][0]['label']['value']

def get_name(property_id):
    load_cache()
    if property_id in name_cache:
        return name_cache[property_id]
    name = fetch_label(property_id)
    name_cache[property_id] = name
    save_cache()
    return name
