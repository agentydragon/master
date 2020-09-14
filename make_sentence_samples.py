import sys
import json
import requests
import urllib.parse
import os.path
import glob

d = 'individual-articles'

from SPARQLWrapper import SPARQLWrapper, JSON

married = """0e/a3/La_Malinche.xml.plaintext
0e/ac/Czechoslovakia.xml.plaintext
0e/5a/Aristide_Maillol.xml.plaintext
b7/da/Haggai.xml.plaintext
b7/bc/Emma_Abbott.xml.plaintext
6b/5f/James_Blaylock.xml.plaintext
6b/00/Douglas_Adams.xml.plaintext
6b/19/Hedwig_of_Silesia.xml.plaintext
6b/71/Greece.xml.plaintext
55/8f/Marshall_McLuhan.xml.plaintext
55/b8/Old_Catholic_Church.xml.plaintext
55/4f/Elagabalus.xml.plaintext
5f/9d/Gary_Coleman.xml.plaintext
5f/a4/Mel_Brooks.xml.plaintext
5f/fb/George_Benson.xml.plaintext
5f/eb/Russia.xml.plaintext
6f/a4/Musical_theatre.xml.plaintext
6f/a3/Mehmed_the_Conqueror.xml.plaintext
6f/e5/Karlheinz_Stockhausen.xml.plaintext
6f/c1/Nostradamus.xml.plaintext
6f/74/Hugh_Hefner.xml.plaintext
f3/c9/%60Abdu%27l-Bah%C3%A1.xml.plaintext
f3/a6/Jakarta.xml.plaintext
f3/ac/Bethlehem.xml.plaintext
f3/25/Herman_Melville.xml.plaintext
2f/99/Scott_Adams.xml.plaintext
2f/e9/Hugh_Binning.xml.plaintext
2f/e3/Jorge_Luis_Borges.xml.plaintext
2f/25/Hezekiah.xml.plaintext
2f/3f/Bob_Jones_University.xml.plaintext
64/2c/Liberia.xml.plaintext
64/2c/Kurt_Vonnegut.xml.plaintext
64/79/Eleanor_of_Aquitaine.xml.plaintext
9b/88/Bill_Holbrook.xml.plaintext
9b/f1/Julio-Claudian_dynasty.xml.plaintext
f7/2f/Mike_Moore_%28New_Zealand_politician%29.xml.plaintext
f7/1f/Bohdan_Khmelnytsky.xml.plaintext
17/e1/History_of_modern_Greece.xml.plaintext
17/b7/Condom.xml.plaintext
17/cd/Hecate.xml.plaintext
17/ba/Ottonian_dynasty.xml.plaintext
67/d6/Felix_Bloch.xml.plaintext
67/bb/George_Whipple.xml.plaintext
67/6e/Empress_Gensh%C5%8D.xml.plaintext
67/c7/Nastassja_Kinski.xml.plaintext
db/fd/Jefferson_Davis.xml.plaintext
db/4f/Barry_Goldwater.xml.plaintext
db/bf/Agnosticism.xml.plaintext
62/2e/Satires_%28Juvenal%29.xml.plaintext
62/08/John_Hanson.xml.plaintext
62/b9/Ken_Kesey.xml.plaintext
69/f4/Stephen_Bachiler.xml.plaintext
69/02/Society_for_Creative_Anachronism.xml.plaintext
69/12/Henry_Bruce%2C_1st_Baron_Aberdare.xml.plaintext
69/56/Richard_III_of_England.xml.plaintext
69/bd/Heracles.xml.plaintext
a1/90/Shah_Jahan.xml.plaintext
e7/a8/Pope_Urban_III.xml.plaintext
e7/81/History_of_Lithuania.xml.plaintext
e7/11/Giovanni_Boccaccio.xml.plaintext
0b/d3/Bing_Crosby.xml.plaintext
0b/8c/Charles_Evers.xml.plaintext
0b/85/Nj%C3%B6r%C3%B0r.xml.plaintext
36/ea/American_Civil_Liberties_Union.xml.plaintext
36/ce/T._S._Eliot.xml.plaintext
36/6e/Robert_Byrd.xml.plaintext
f8/44/Neville_Chamberlain.xml.plaintext
f8/1b/Marquette%2C_Michigan.xml.plaintext
f8/ae/Miss_Marple.xml.plaintext
c4/ad/Anthony_of_Saxony.xml.plaintext
31/60/Oswald_Spengler.xml.plaintext
31/3c/Falstaff.xml.plaintext
31/1b/Li_Bai.xml.plaintext
31/12/Andromeda_%28mythology%29.xml.plaintext
9d/a2/Colin_Dexter.xml.plaintext
9d/96/Claude_Auchinleck.xml.plaintext
9d/0f/Stephen_King.xml.plaintext
b2/69/Amalasuntha.xml.plaintext
b2/ce/Reno%2C_Nevada.xml.plaintext
32/62/Roger_Penrose.xml.plaintext
32/f6/Murray_Rothbard.xml.plaintext
32/88/Jerome_Kern.xml.plaintext""".split('\n')
married = map(lambda x: os.path.join(d, x), married)


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
    # for file in glob.glob(os.path.join(d, '*', '*', '*.plaintext')):
    for file in married:
        corenlp_file = file + ".corenlpjson"
        spotlight_file = file + ".spotlightjson"
        if not os.path.isfile(corenlp_file):
            print(file, 'not corenlpd')
            continue
        if not os.path.isfile(spotlight_file):
            print(file, 'not spotlighted')
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
                    sf.write('%s\n' % json.dumps(relations))

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
