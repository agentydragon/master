wikidata_entity_prefix = 'http://www.wikidata.org/entity/'
wikidata_property_prefix = 'http://www.wikidata.org/wiki/Property:'

def is_wikidata_entity_url(url):
    return url.startswith(wikidata_entity_prefix)

def wikidata_entity_url_to_entity_id(url):
    assert url.startswith(wikidata_entity_prefix)
    return url[len(wikidata_entity_prefix):]

def wikidata_property_url_to_property_id(url):
    assert url.startswith(wikidata_property_prefix)
    return url[len(wikidata_property_prefix):]

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

def relation_interesting(relation):
    if relation in ['http://schema.org/description',
                    'http://www.w3.org/2004/02/skos/core#altLabel',
                    'http://www.w3.org/2000/01/rdf-schema#label']:
        return False
    if 'wikidata' not in relation:
        return False
    return True

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

def transform_relation(subject, rel, other):
    if not relation_interesting(rel):
        return None
    rel = normalize_relation(rel)
    if is_statement(other):
        return None
    if is_statement(subject):
        return None
    if '/Q' not in subject:
        return None
    if '/Q' not in other:
        return None
    if '/P' not in rel:
        return None
    if not is_wikidata_entity_url(other):
        return None
    if not is_wikidata_entity_url(subject):
        return None
    subject = wikidata_entity_url_to_entity_id(subject)
    other = wikidata_entity_url_to_entity_id(other)
    rel = wikidata_property_url_to_property_id(rel)

    return (subject, rel, other)
