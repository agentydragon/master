from prototype.lib import wikidata_util
from prototype.lib import sparql_client
from prototype.lib import zk
from prototype.lib import flags

# TODO: somehow remove limit
LIMIT = 100

flags.add_argument('--wikidata_endpoint',
                   help=('Wikidata SPARQL endpoint. Example: '
                         'https://query.wikidata.org/sparql, '
                         'http://hador:3030/wikidata/query. '
                         'Specify "PUBLIC" to use public endpoint.'))

def join_entities(entities):
    return ' '.join([('wd:%s' % wikidata_id) for wikidata_id in sorted(entities)])

PUBLIC_WIKIDATA_ENDPOINT = 'https://query.wikidata.org/sparql'

def get_default_endpoint_url():
    endpoint = flags.parse_args().wikidata_endpoint

    if endpoint == 'PUBLIC':
        endpoint = PUBLIC_WIKIDATA_ENDPOINT

    if endpoint:
        return endpoint


    zk_endpoint = zk.get_wikidata_endpoint()
    if zk_endpoint:
        print("Grabbed Wikidata endpoint from ZK:", zk_endpoint)
        return ('http://%s/wikidata/query' % zk_endpoint)

    raise Exception('No Wikidata endpoint available.')

    # print("WARN: Falling back to Wikimedia Foundation's Wikidata")
    # return default_wikidata_url

class WikidataClient(object):
    def __init__(self, endpoint=None):
        self.wikidata_relations_cache = {}
        self.forward_cache = {}
        self.backward_cache = {}

        if not endpoint:
            endpoint = get_default_endpoint_url()

        self.wikidata_client = sparql_client.SPARQLClient(endpoint)

    def collect_forward_properties(self, wikidata_id):
        if wikidata_id in self.forward_cache:
            return self.forward_cache[wikidata_id]

        # print('forward for', wikidata_id)
        results = self.wikidata_client.get_results("""
            SELECT ?rel ?other
            WHERE { wd:%s ?rel ?other . }
            LIMIT %d
        """ % (wikidata_id, LIMIT))

        properties=[]
        for x in results['results']['bindings']:
            # print(x)
            subject = wikidata_util.wikidata_entity_prefix + wikidata_id
            rel = x['rel']['value']
            other = x['other']['value']

            triple = wikidata_util.transform_relation(subject, rel, other)
            if triple:
                # print(triple)
                properties.append(triple)

        self.forward_cache[wikidata_id] = properties

        return properties

    # TODO DRY
    def collect_backward_properties(self, wikidata_id):
        if wikidata_id in self.backward_cache:
            return self.backward_cache[wikidata_id]

        #print('backward for', wikidata_id)
        results = self.wikidata_client.get_results("""
            SELECT ?rel ?other
            WHERE { ?other ?rel wd:%s . }
            LIMIT %d
        """ % (wikidata_id, LIMIT))

        properties=[]
        for x in results['results']['bindings']:
            rel = x['rel']['value']
            other = x['other']['value']
            subject = wikidata_util.wikidata_entity_prefix + wikidata_id

            triple = wikidata_util.transform_relation(other, rel, subject)
            if triple:
                # print(triple)
                properties.append(triple)

        self.backward_cache[wikidata_id] = properties

        return properties

    def get_holding_relations_between(self, s, o):
        results = self.wikidata_client.get_results("""
            SELECT ?rel
            WHERE { wd:%s ?rel wd:%s . }
            LIMIT %s
        """ % (s, o, LIMIT))

        # TODO: cache?

        rels = []
        for x in results['results']['bindings']:
            rel = x['rel']['value']
            rel = wikidata_util.normalize_relation(rel)
            if rel is not None:
                rels.append(rel)
        return rels

    def get_all_triples_of_entity(self, wikidata_id):
#        self.load_cache()

        if wikidata_id in self.wikidata_relations_cache:
            return self.wikidata_relations_cache[wikidata_id]

        properties = []
        properties.extend(self.collect_forward_properties(wikidata_id))
        properties.extend(self.collect_backward_properties(wikidata_id))

        self.wikidata_relations_cache[wikidata_id] = properties
#
#        # TODO HAX
#        self.save_cache()
        return properties

    def find_relation_subjects(self, entities, relation):
        query = """
            SELECT DISTINCT ?subject
            WHERE {
                VALUES ?subject { %s }
                ?subject wdp:%s ?object
            }
        """ % (join_entities(entities), relation)
        results = self.wikidata_client.get_results(query)
        subjects = set()
        for x in results['results']['bindings']:
            subject = x['subject']['value']
            subjects.add(wikidata_util.wikidata_entity_url_to_entity_id(subject))
        return subjects

    def find_relation_objects(self, entities, relation):
        query = """
            SELECT DISTINCT ?object
            WHERE {
                VALUES ?object { %s }
                ?subject wdp:%s ?object
            }
        """ % (join_entities(entities), relation)
        results = self.wikidata_client.get_results(query)
        objects = set()
        for x in results['results']['bindings']:
            obj = x['object']['value']
            objects.add(wikidata_util.wikidata_entity_url_to_entity_id(obj))
        return objects

    # subject_wikidata_ids = set()
    # object_wikidata_ids = set()
    # for wikidata_id in all_wikidata_ids:
    #     if wikidata_client.entity_is_relation_subject(wikidata_id, relation):
    #         subject_wikidata_ids.add(wikidata_id)
    #     if wikidata_client.entity_is_relation_object(wikidata_id, relation):
    #         object_wikidata_ids.add(wikidata_id)

    def entity_is_relation_subject(self, entity, relation):
        query = """
            ASK { wd:%s wdp:%s ?other }
        """ % (entity, relation)
        return self.wikidata_client.get_results(query)['boolean']

    def entity_is_relation_object(self, entity, relation):
        query = """
            ASK { ?other wdp:%s wd:%s }
        """ % (relation, entity)
        return self.wikidata_client.get_results(query)['boolean']

    def get_object_relation_pairs(self, wikidata_ids):
        if len(wikidata_ids) == 0:
            return []

        rels = set()

        query = """
            SELECT ?o ?p
            WHERE {
                VALUES ?o { %s }
                ?s ?p ?o
            }
        """ % (join_entities(wikidata_ids))
        results = self.wikidata_client.get_results(query)
        pairs = set()
        for row in results['results']['bindings']:
            rel = row['p']['value']
            rel = wikidata_util.normalize_relation(rel)
            if not rel:
                continue
            object = row['o']['value']
            if not wikidata_util.is_wikidata_entity_url(object):
                continue
            object = wikidata_util.wikidata_entity_url_to_entity_id(object)
            pairs.add((object, rel))
        return list(sorted(pairs))

    def get_subject_relation_pairs(self, wikidata_ids):
        if len(wikidata_ids) == 0:
            return []

        rels = set()

        query = """
            SELECT ?s ?p
            WHERE {
                VALUES ?s { %s }
                ?s ?p ?o
            }
        """ % (join_entities(wikidata_ids))
        results = self.wikidata_client.get_results(query)
        pairs = set()
        for row in results['results']['bindings']:
            rel = row['p']['value']
            rel = wikidata_util.normalize_relation(rel)
            if not rel:
                continue
            subject = row['s']['value']
            if not wikidata_util.is_wikidata_entity_url(subject):
                continue
            subject = wikidata_util.wikidata_entity_url_to_entity_id(subject)
            pairs.add((subject, rel))
        return list(sorted(pairs))

    def get_all_relations_of_entities(self, wikidata_ids):
        if len(wikidata_ids) == 0:
            return []

        rels = set()

        query = """
            SELECT DISTINCT ?p
            WHERE {
                VALUES ?s { %s }
                ?s ?p ?o
            }
        """ % (join_entities(wikidata_ids))
        results = self.wikidata_client.get_results(query)
        for row in results['results']['bindings']:
            rel = row['p']['value']
            rel = wikidata_util.normalize_relation(rel)
            if rel:
                rels.add(rel)

        query = """
            SELECT DISTINCT ?p
            WHERE {
                VALUES ?o { %s }
                ?s ?p ?o
            }
        """ % (x)
        results = self.wikidata_client.get_results(query)
        for row in results['results']['bindings']:
            rel = row['p']['value']
            rel = wikidata_util.normalize_relation(rel)
            if rel:
                rels.add(rel)

        return rels

    def get_triples_between_entities(self, wikidata_ids):
        if len(wikidata_ids) == 0:
            return []

        x = join_entities(wikidata_ids)
        query = """
            SELECT ?s ?p ?o
            WHERE {
                VALUES ?s { %s }
                VALUES ?o { %s }
                ?s ?p ?o
            }
        """ % (x, x)
        results = self.wikidata_client.get_results(query)
        triples = []
        for x in results['results']['bindings']:
            subject = x['s']['value']
            rel = x['p']['value']
            other = x['o']['value']
            triple = wikidata_util.transform_relation(subject, rel, other)
            if triple:
                # print(triple)
                triples.append(triple)
        return triples

        # # TODO: optimize
        # all_triples = []
        # # Optimize: can collect forward-only.
        # # TODO: And do it in one query.
        # for entity in wikidata_ids:
        #     # all_triples.extend(self.get_all_triples_of_entity(entity))
        #     all_triples.extend(self.collect_forward_properties(entity))
        # all_triples = set(
        #     triple for triple in all_triples
        #     if (triple[0] in wikidata_ids) and (triple[2] in wikidata_ids)
        # )
        # return list(sorted(all_triples))


    def fetch_label(self, entity_id):
        results = self.wikidata_client.get_results("""
            SELECT ?label
            WHERE { wd:%s rdfs:label ?label . FILTER (langMatches(lang(?label),"en")) }
        """ % entity_id)
        if len(results['results']['bindings']) == 0:
            return None
        else:
            return results['results']['bindings'][0]['label']['value']

    def get_entity_name(self, entity_id):
#        self.load_cache()
#        if entity_id in self.name_cache:
#            return self.name_cache[entity_id]
        name = self.fetch_label(entity_id)
#        self.name_cache[entity_id] = name
#        self.save_cache()
        return name

    def get_name(self, property_id):
#        self.load_cache()
#        if property_id in self.name_cache:
#            return self.name_cache[property_id]
        name = self.fetch_label(property_id)
#        self.name_cache[property_id] = name
#        self.save_cache()
        return name

    def relation_exists(self, s, p, o):
        query = """
            ASK { wd:%s wdp:%s wd:%s }
        """ % (s, p, o)
        return self.wikidata_client.get_results(query)['boolean']
