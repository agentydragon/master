from prototype.lib import wikidata_util
from prototype.lib import sparql_client

wikidata_url = 'https://query.wikidata.org/sparql'

class WikidataClient(object):
    def __init__(self, endpoint=None):
        self.wikidata_relations_cache = {}
        if endpoint is None:
            endpoint = wikidata_url
        self.wikidata_client = sparql_client.SPARQLClient(endpoint)

    def collect_forward_properties(self, wikidata_id):
        # print('forward for', wikidata_id)
        results = self.wikidata_client.get_results("""
            SELECT ?rel ?other
            WHERE { wd:%s ?rel ?other . }
        """ % wikidata_id)

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
        return properties

    # TODO DRY
    def collect_backward_properties(self, wikidata_id):
        #print('backward for', wikidata_id)
        results = self.wikidata_client.get_results("""
            SELECT ?rel ?other
            WHERE { ?other ?rel wd:%s . }
            LIMIT 500
        """ % wikidata_id)
        # TODO: remove limit 500

        properties=[]
        for x in results['results']['bindings']:
            rel = x['rel']['value']
            other = x['other']['value']
            subject = wikidata_util.wikidata_entity_prefix + wikidata_id

            triple = wikidata_util.transform_relation(other, rel, subject)
            if triple:
                # print(triple)
                properties.append(triple)
        return properties

    def get_holding_relations_between(self, s, o):
        results = self.wikidata_client.get_results("""
            SELECT ?rel
            WHERE { wd:%s ?rel wd:%s . }
            LIMIT 500
        """ % (s, o))
        # TODO: remove limit 500

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

    def get_triples_between_entities(self, wikidata_ids):
        # TODO: optimize
        all_triples = []
        # TODO: optimize: can collect forward-only and do it in one query
        for entity in wikidata_ids:
            all_triples.extend(self.get_all_triples_of_entity(entity))
        return list(sorted(set(triple for triple in all_triples
                        if (triple[0] in wikidata_ids) and (triple[2] in wikidata_ids))))


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
