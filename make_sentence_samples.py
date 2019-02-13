import sys
import json
import requests
import urllib.parse
import os.path
import glob

d = 'individual-articles'

from SPARQLWrapper import SPARQLWrapper, JSON


class NoWikidataEquivalent(Exception):
    pass


def get_wikidata(uri):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
#    sparql.setQuery("""
#        PREFIX : <http://dbpedia.org/resource/>
#        PREFIX owl: <http://www.w3.org/2002/07/owl#>
#        SELECT ?same WHERE { :%s owl:sameAs ?same }
#    """ % uri)
    sparql.setQuery("""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?same WHERE { <http://dbpedia.org/resource/%s> owl:sameAs ?same }
    """ % uri)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for row in results['results']['bindings']:
        value = row['same']['value']
        if value.startswith('http://www.wikidata.org/entity/'):
            return value  # Q218005
    raise NoWikidataEquivalent(f'No WikiData equivalent: {uri}')


def relations_between(a, b):
    sparql = SPARQLWrapper(
        "https://query.wikidata.org/bigdata/namespace/wdq/sparql")
    sparql.setQuery("""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?pred WHERE { <%s> ?pred <%s> }
    """ % (a, b))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    preds = []
    for row in results['results']['bindings']:
        preds.append(row['pred']['value'])
    return preds


def find_all_relations(entity_set):
    triples = []
    entities = list(sorted(entity_set))
    for i, a in enumerate(entities):
        for j, b in enumerate(entities):
            if i >= j:
                continue
            # We now have a pair of entities.
            # {A} UNION {B}  -->   that could become quite a long query...
            relations = relations_between(a, b)
            if not relations:
                continue
            #raise Exception('yep found a true relation: %s %s %s' % (a, b,
            #                                                         relations))
            for relation in relations:
                triples.append((a, relation, b))
    return triples


with open('sentences', 'w') as sf:
    for file in glob.glob(os.path.join(d, '*', '*', '*.plaintext')):
        corenlp_file = file + ".corenlpjson"
        spotlight_file = file + ".spotlightjson"
        if not os.path.isfile(corenlp_file) or not os.path.isfile(spotlight_file):
            continue

        with open(file) as f:
            content = f.read()
        try:
            with open(corenlp_file) as f:
                corenlp = json.load(f)
            with open(spotlight_file) as f:
                spotlight = json.load(f)
        except Exception as e:
            print(e)
            continue
        #if "Resources" not in spotlight:
        #    continue
        if 'annotation' not in spotlight:
            continue
        print(file)

        # if len(content) > 200 or len(content) < 100:
        #     continue

        for sentence in corenlp["sentences"]:
            try:
                start = sentence["tokens"][0]["characterOffsetBegin"]
                end = sentence["tokens"][-1]["characterOffsetEnd"]
                sentence_content = content[start:end]

                sf.write(sentence_content + '\n')
                print(sentence_content)

                all_wikidata_uris = set()

                for surfaceForm in spotlight["annotation"]["surfaceForm"]:
                    offset = int(surfaceForm["@offset"])
                    if not (offset >= start and offset < end):
                        continue
                    sform = surfaceForm["@name"]
                    print(sform)

                    # Check that the surface for checks out.
                    assert content[offset:offset+len(sform)] == sform

                    sf.write('%d %s\n' % (offset, sform))

                    resource2 = surfaceForm["resource"]
                    if not isinstance(resource2, list):
                        resource2 = [resource2]
                    for resource in resource2:
                        uri = resource["@uri"]
                        wikidata_uri = get_wikidata(uri)
                        final_score = float(resource["@finalScore"])
                        print(uri, wikidata_uri, final_score)
                        sf.write('%s %s %f\n' %
                                 (uri, wikidata_uri, final_score))
                        all_wikidata_uris.add(wikidata_uri)

                relations = find_all_relations(all_wikidata_uris)
                if relations:
                    print('Truth: %s' % relations)

                # The URI is <http://dbpedia.org/resource/> plus uri

                #for resource in surfaceForm["resource"]:
                # TODO(prvak): No idea whether the 'uri' parameter is useful at all.

                # This is for the "annotate" Spotlight API: for resource in spotlight["Resources"]:
                # This is for the "annotate" Spotlight API:     offset = int(
                # This is for the "annotate" Spotlight API:         resource["@offset"])
                # This is for the "annotate" Spotlight API:     if offset >= start and offset < end:
                # This is for the "annotate" Spotlight API:         print(resource["@URI"], resource["@surfaceForm"],
                # This is for the "annotate" Spotlight API:               resource["@similarityScore"],
                # This is for the "annotate" Spotlight API:               resource["@support"],
                # This is for the "annotate" Spotlight API:               resource["@percentageOfSecondRank"])
                # This is for the "annotate" Spotlight API:         sf.write('%d %d %s %s\n' % (offset - start,
                # This is for the "annotate" Spotlight API:                                     offset - start +
                # This is for the "annotate" Spotlight API:                                     len(
                # This is for the "annotate" Spotlight API:                                         resource["@surfaceForm"]),
                # This is for the "annotate" Spotlight API:                                     resource["@URI"],
                # This is for the "annotate" Spotlight API:                                     resource["@surfaceForm"]
                # This is for the "annotate" Spotlight API:                                     ))
                sf.write('\n')
                print()
            except NoWikidataEquivalent as e:
                print(e)
                print('Skipping sentence')

            # sys.exit(0)

# TODO(prvak): Now, what about 'confidence'? That's used for disambiguation.
