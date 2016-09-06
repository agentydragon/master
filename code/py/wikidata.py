from py import json_cache
from py import wikidata_util
from py import sparql_client

wikidata_url = 'https://query.wikidata.org/sparql'

class WikidataClient(object):
    def __init__(self):
        self.wikidata_relations_cache = json_cache.JsonCache('wikidata_cache')
        self.name_cache = json_cache.JsonCache('name_cache')
        self.wikidata_client = sparql_client.SPARQLClient(wikidata_url)
        self.persist_caches = True

    def load_cache(self):
        if self.persist_caches:
            self.wikidata_relations_cache.load()
            self.name_cache.load()

    def save_cache(self):
        if self.persist_caches:
            self.wikidata_relations_cache.save()
            self.name_cache.save()

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

    def get_all_triples_of_entity(self, wikidata_id):
        self.load_cache()

        if wikidata_id in self.wikidata_relations_cache:
            return self.wikidata_relations_cache[wikidata_id]

        properties = []
        properties.extend(self.collect_forward_properties(wikidata_id))
        properties.extend(self.collect_backward_properties(wikidata_id))

        self.wikidata_relations_cache[wikidata_id] = properties

        # TODO HAX
        self.save_cache()
        return properties

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
        self.load_cache()
        if entity_id in self.name_cache:
            return self.name_cache[entity_id]
        name = self.fetch_label(entity_id)
        self.name_cache[entity_id] = name
        self.save_cache()
        return name

    def get_name(self, property_id):
        self.load_cache()
        if property_id in self.name_cache:
            return self.name_cache[property_id]
        name = self.fetch_label(property_id)
        self.name_cache[property_id] = name
        self.save_cache()
        return name
