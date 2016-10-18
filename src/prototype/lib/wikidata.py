from prototype.lib import wikidata_util
from prototype.lib import sparql_client
from prototype.lib import zk
from prototype.lib import flags

import progressbar

# TODO: somehow remove limit
LIMIT = 100

flags.add_argument('--wikidata_endpoint',
                   help=('Wikidata SPARQL endpoint. Example: '
                         'https://query.wikidata.org/sparql, '
                         'http://hador:3030/wikidata/query. '
                         'Specify "PUBLIC" to use public endpoint.'))

def join_entities(entities):
    return ' '.join([('wd:%s' % wikidata_id) for wikidata_id in sorted(entities)])

def join_relations(relations):
    return ' '.join([('wdp:%s' % relation_id) for relation_id in sorted(relations)])

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
        return zk_endpoint

    raise Exception('No Wikidata endpoint available.')

    # print("WARN: Falling back to Wikimedia Foundation's Wikidata")
    # return default_wikidata_url

class WikidataClient(object):
    def __init__(self, endpoint=None):
        self.wikidata_relations_cache = {}
        self.forward_cache = {}
        self.backward_cache = {}
        self.name_cache = {}

        if not endpoint:
            endpoint = get_default_endpoint_url()

        self.wikidata_client = sparql_client.SPARQLClient(endpoint)

    def collect_forward_properties(self, wikidata_id):
        if wikidata_id in self.forward_cache:
            return self.forward_cache[wikidata_id]

        results = self.wikidata_client.get_result_values("""
            SELECT ?rel ?other
            WHERE { wd:%s ?rel ?other . }
            LIMIT %d
        """ % (wikidata_id, LIMIT))

        properties=[]
        for row in results:
            subject = wikidata_util.wikidata_entity_prefix + wikidata_id
            rel = row['rel']
            other = row['other']

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
        results = self.wikidata_client.get_result_values("""
            SELECT ?rel ?other
            WHERE { ?other ?rel wd:%s . }
            LIMIT %d
        """ % (wikidata_id, LIMIT))

        properties=[]
        for row in results:
            rel = row['rel']
            other = row['other']
            subject = wikidata_util.wikidata_entity_prefix + wikidata_id

            triple = wikidata_util.transform_relation(other, rel, subject)
            if triple:
                # print(triple)
                properties.append(triple)

        self.backward_cache[wikidata_id] = properties

        return properties

    def get_holding_relations_between(self, s, o):
        results = self.wikidata_client.get_result_values("""
            SELECT ?rel
            WHERE { wd:%s ?rel wd:%s . }
            LIMIT %s
        """ % (s, o, LIMIT))

        # TODO: cache?

        rels = []
        for row in results:
            rel = row['rel']
            rel = wikidata_util.normalize_relation(rel)
            if rel is not None:
                rels.append(rel)
        return rels

    def get_all_triples_of_entity(self, wikidata_id):
        if wikidata_id in self.wikidata_relations_cache:
            return self.wikidata_relations_cache[wikidata_id]

        properties = []
        properties.extend(self.collect_forward_properties(wikidata_id))
        properties.extend(self.collect_backward_properties(wikidata_id))

        self.wikidata_relations_cache[wikidata_id] = properties
        return properties

    def find_relation_subjects(self, entities, relation):
        query = """
            SELECT DISTINCT ?subject
            WHERE {
                VALUES ?subject { %s }
                ?subject wdp:%s ?object
            }
        """ % (join_entities(entities), relation)
        results = self.wikidata_client.get_result_values(query)
        subjects = set()
        for x in results:
            subject = x['subject']
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
        results = self.wikidata_client.get_result_values(query)
        objects = set()
        for row in results:
            obj = row['object']
            objects.add(wikidata_util.wikidata_entity_url_to_entity_id(obj))
        return objects

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

    def get_object_relation_pairs(self, wikidata_ids, relations):
        """
        Returns:
            list((Object, Relation)) such that there exists a Subject
            such that (Subject, Relation, Object) is a true triple.
        """
        if len(wikidata_ids) == 0:
            return []

        rels = set()

        query = """
            SELECT ?o ?p
            WHERE {
                VALUES ?o { %s }
                VALUES ?p { %s }
                ?s ?p ?o
            }
        """ % (join_entities(wikidata_ids), join_relations(relations))
        results = self.wikidata_client.get_result_values(query)
        pairs = set()
        for row in results:
            rel = row['p']
            rel = wikidata_util.normalize_relation(rel)
            if not rel:
                continue
            object = row['o']
            if not wikidata_util.is_wikidata_entity_url(object):
                continue
            object = wikidata_util.wikidata_entity_url_to_entity_id(object)
            pairs.add((object, rel))
        return list(sorted(pairs))

    def get_subject_relation_pairs(self, wikidata_ids, relations):
        """
        Returns:
            list((Subject, Relation)) such that there exists an Object
            such that (Subject, Relation, Object) is a true triple.
        """
        if len(wikidata_ids) == 0:
            return []

        rels = set()

        query = """
            SELECT ?s ?p
            WHERE {
                VALUES ?s { %s }
                VALUES ?p { %s }
                ?s ?p ?o
            }
        """ % (join_entities(wikidata_ids), join_relations(relations))
        results = self.wikidata_client.get_result_values(query)
        pairs = set()
        for row in results:
            rel = row['p']
            rel = wikidata_util.normalize_relation(rel)
            if not rel:
                continue
            subject = row['s']
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
        results = self.wikidata_client.get_result_values(query)
        for row in results:
            rel = row['p']
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
        results = self.wikidata_client.get_result_values(query)
        for row in results:
            rel = row['p']
            rel = wikidata_util.normalize_relation(rel)
            if rel:
                rels.add(rel)

        return rels

    def get_triples_between_entities(self, wikidata_ids, relations):
        if len(wikidata_ids) == 0:
            return []

        x = join_entities(wikidata_ids)
        query = """
            SELECT ?s ?p ?o
            WHERE {
                VALUES ?s { %s }
                VALUES ?o { %s }
                VALUES ?p { %s }
                ?s ?p ?o
            }
        """ % (x, x, join_relations(relations))
        results = self.wikidata_client.get_result_values(query)
        triples = []
        for x in results:
            subject = x['s']
            rel = x['p']
            other = x['o']
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
        results = self.wikidata_client.get_result_values("""
            SELECT ?label
            WHERE { wd:%s rdfs:label ?label . FILTER (langMatches(lang(?label),"en")) }
        """ % entity_id)
        if len(results) == 0:
            return None
        else:
            return results[0]['label']

    def get_entity_name(self, entity_id):
        if entity_id in self.name_cache:
            return self.name_cache[entity_id]
        name = self.fetch_label(entity_id)
        self.name_cache[entity_id] = name
        return name

    def get_true_subset(self, triples):
        triples = list(sorted(triples))
        BATCH_SIZE = 800
        true_triples = set()

        r = range(0, len(triples), BATCH_SIZE)
        bar = progressbar.ProgressBar()
        for i in bar(r):
            batch_triples = triples[i:i+BATCH_SIZE]
            batch_entities = set()
            batch_relations = set()

            for subject, relation, object in batch_triples:
                batch_entities.add(subject)
                batch_relations.add(relation)
                batch_entities.add(object)

            # TODO: split left and right side (might be important)
            true_batch_triples = self.get_triples_between_entities(batch_entities, batch_relations)
            true_triples = true_triples.union(true_batch_triples)

        return list(sorted(true_triples))

    def get_names(self, ids):
        labels = {}
        bar = progressbar.ProgressBar()

        # for x in bar(ids):
        #     label = self.get_name(x)
        #     if label:
        #         labels[x] = label
        # return label

        ids = list(sorted(ids))

        batch_size = 50

        for i in bar(range(0, len(ids), batch_size)):
            ids_batch = ids[i:i+batch_size]

            ids_string = join_entities(ids_batch)
            results = self.wikidata_client.get_result_values("""
                SELECT ?x ?label
                WHERE {
                    VALUES ?x { %s }
                    ?x rdfs:label ?label .
                    FILTER (langMatches(lang(?label),"en"))
                }
            """ % ids_string)
            for row in results:
                entity = wikidata_util.wikidata_entity_url_to_entity_id(row['x'])
                label = row['label']
                labels[entity] = label
                self.name_cache[entity] = label
        return labels

    def get_name(self, property_id):
        if property_id in self.name_cache:
            return self.name_cache[property_id]
        name = self.fetch_label(property_id)
        self.name_cache[property_id] = name
        return name

    def relation_exists(self, s, p, o):
        query = """
            ASK { wd:%s wdp:%s wd:%s }
        """ % (s, p, o)
        return self.wikidata_client.get_results(query)['boolean']
