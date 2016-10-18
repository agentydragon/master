from prototype.lib import wikidata
from prototype.lib import wikidata_util
from prototype.lib import file_util
from prototype.lib import flags
import paths
import random

INFORMATIVE_RELATIONS = [
    'P21', # sex or gender
    'P22', # father
    'P25', # mother
    'P7', # brother
    'P9', # sister
    'P26', # spouse
    'P451', # partner
    'P40', # child

    'P27', # country of citizenship
    'P103', # native language

    # 43, # stepfather
    # 44, # stepmother
    # 1038, # relative
    # 69, # educated at
    # 172, # ethnic group
    # 106, # occupation
    # 101, # field of work
    # 108, # employer
    # 140, # religion
    # 91, # sexual orientation
    # 1066, # student of
    # 802, # student
    # 185, # doctoral student
    # 53, # noble family
    # 512, # academic degree
    # 552, # handedness
    # 734, # family name
    # 1037, # manager/director
    # 1344, # participant of; inverse of P710 or P1923
    # 1340, # eye color
    # 1303, # instrument
    # 1399, # convicted of
    # 1416, # affiliation
    # 54, # member of sports team
    # 413, # position played on team/speciality
    # 1532, # country for sport
    # 241, # military branch
    # 410, # military rank
    # 598, # commander of
    # 607, # conflict

    # 452, # industry
    # 159, # headquarters location
    # 807, # separated from
    # 31, # instance of
    # 112, # founder
    # 740, # location of formation
    # 1387, # political alignment
    # 1313, # office held by head of government
    # 1290 # godparent
]

EXPORTED_RELATIONS = INFORMATIVE_RELATIONS

# (P21, P22, P25, P27, P7, P9, P26, P451, P40) ==> 5 500 823 lines

# def get_relation_triples(wikidata_client, relation, limit=None):
#     query = """
#         SELECT ?a ?c
#         WHERE { ?a wdp:P%s ?c }
#     """ % relation
#     if limit:
#         query += "LIMIT " + str(limit)
# 
#     results = wikidata_client.wikidata_client.get_results(query)
#     triples = []
#     for row in results['results']['bindings']:
#         subject, object = row['a']['value'], row['c']['value']
#         r = relation
#         triple = wikidata_util.transform_relation(subject, r, object)
#         if not triple:
#             continue
# 
#         subject, r, object = triple
#         triples.append((subject, r, object))
#     return triples

def get_relations_triples(wikidata_client, relations, limit=None):
    propparts = []
    for property in relations:
        propparts.append('wdp:%s' % property)
    query = """
        SELECT ?a ?b ?c
        WHERE {
            VALUES ?b { %s } .
            ?a ?b ?c
        }
    """ % (' '.join(propparts))

    if limit:
        query += "LIMIT " + str(limit)

    results = wikidata_client.wikidata_client.get_results(query)
    triples = []
    for row in results['results']['bindings']:
        subject, relation, object = row['a']['value'], row['b']['value'], row['c']['value']
        triple = wikidata_util.transform_relation(subject, relation, object)
        if not triple:
            continue

        subject, relation, object = triple
        triples.append((subject, relation, object))
    return triples

def main():
    flags.add_argument('--limit', type=int, default=None)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

#    for property in properties:
#        # propparts.append('wdp:P%s' % property)
#        propparts.append('{ ?a wdp:P%s ?b }' % property)
#
#    query = """
#        SELECT ?a ?b ?c
#        WHERE {
#            %s .
#            ?a ?b ?c
#        }
#    """ % (' UNION '.join(propparts))
    wikidata_client = wikidata.WikidataClient()
    triples = get_relations_triples(wikidata_client, INFORMATIVE_RELATIONS, limit=args.limit)

    PRA_ROOT = paths.WORK_DIR + '/pra'

    all_relations_file = PRA_ROOT + '/triples-all'
    with open(all_relations_file, 'w') as f:
        for subject, relation, object in triples:
            f.write("%s\t%s\t%s\n" % (subject, relation, object))

    for relation in EXPORTED_RELATIONS:
        print('Splitting out', relation, '...')

        directory = PRA_ROOT + '/prvak/relation_metadata/no-such-file/relations/'
        file_util.ensure_dir(directory)
        f = open(directory + relation, 'w')

        relation_triples = [(subject, r, object)
                            for subject, r, object in triples
                            if r == relation]
        assert len(relation_triples) > 0
        for subject, r, object in relation_triples:
            if r != relation:
                continue
            # f.write("%s %s %s\n" % (subject, relation, object))
            f.write("%s\t%s\t1\n" % (subject, object))
        f.close()

    random.shuffle(triples)

    directory = PRA_ROOT + '/prvak/experiment_specs'
    file_util.ensure_dir(directory)
    with open(directory + '/prv1.json', 'w') as f:
        property_string = ', '.join(map(lambda r: '"' + r + '"',
                                        INFORMATIVE_RELATIONS))
        f.write("""
    {
        "graph": {
            "name": "minified wikidata",
            "relation sets": [
                {
                    "relation file": "%s",
                    "is kb": false
                }
            ]
        },
        "split": {
            "name": "prv1splitauto",
            "relations": [%s],
            "percent training": 0.8,
            "relation metadata": "no-such-file",
            "graph": "minified wikidata",
        }
    }
    """ % (all_relations_file, property_string))

    N_BACKGROUND = 5000000

    print('Writing background...')
    with open(PRA_ROOT + '/triples-random-background', 'w') as f:
        for subject, relation, object in triples[:N_BACKGROUND]:
            f.write("%s\t%s\t%s\n" % (subject, relation, object))

    print('Writing traintest...')
    with open(PRA_ROOT + '/triples-random-traintest', 'w') as f:
        for subject, relation, object in triples[N_BACKGROUND:]:
            f.write("%s\t%s\t%s\n" % (subject, relation, object))

if __name__ == '__main__':
    main()
