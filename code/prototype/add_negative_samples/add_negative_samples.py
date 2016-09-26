from prototype.lib import sample_repo
from prototype.lib import sample_generation
from prototype.lib import training_sample
from prototype.lib import wikidata
from prototype.lib import flags
import random
import multiprocessing
import itertools

documents = None

###def generate_negatives_for_relation(relation, count):
###    wikidata_client = wikidata.WikidataClient()
###
###    samples = []
###    for i in range(count):
###        # print(i)
###        samples.append(sample_generation.sample_negative(
###            documents,
###            relation,
###            wikidata_client = wikidata_client,
###        ))
###    return samples
###
###def ll(x):
###    return generate_negatives_for_relation(*x)


###def add_negative_samples_from_other_relations(relation, wikidata_client):
###    negatives_from_other_relations = []
###
###    for other_relation in sample_repo.all_relations():
###        if other_relation == relation:
###            continue
###
###        negatives_from_relation = []
###
###        if other_relation not in all_positive_samples:
###            continue
###
###        other_samples = all_positive_samples[other_relation]
###        for sample in other_samples:
###            if wikidata_client.relation_exists(sample.subject,
###                                               relation,
###                                               sample.object):
###                continue
###            else:
###                negatives_from_relation.append(sample)
###        print(other_relation, 'produced', len(negatives_from_relation),
###              'negatives for', relation)
###        negatives_from_other_relations.extend(negatives_from_relation)
###
###    return negatives_from_other_relations

def process_relation(pool, relation, count_per_relation,
                     parallelism):
    wikidata_client = wikidata.WikidataClient()

    ## try:
    ##     samples = sample_repo.load_samples(relation)
    ##     negatives = list(filter(lambda s: not s.positive, samples))
    ##     if len(negatives) >= count_per_relation:
    ##         print(relation, wikidata_client.get_name(relation), "all done already")
    ##         return
    ## except AssertionError:
    ##     # TODO: horrible!
    ##     pass

    from_others = negative_samples[relation]
    #from_others = add_negative_samples_from_other_relations(relation,
    #                                                        wikidata_client)

    #indexes = list(range(count_per_relation))
    #pool_parts = []
    #per_pool = count_per_relation // parallelism
    #for i in range(0, count_per_relation, per_pool):
    #    pool_part = indexes[i:i+per_pool]
    #    pool_parts.append(pool_part)

    #pool_parts = list(map(
    #    lambda pool_part: (
    #        relation, len(pool_part)
    #    ),
    #    pool_parts
    #))

    #parts = pool.map(ll, pool_parts)
    #all_samples = list(itertools.chain(*parts)) + from_others
    all_samples = from_others + complete_negatives
    sample_repo.write_negative_samples(relation, all_samples)
    print("Produced", len(all_samples), "negatives for", relation)

def main():
    flags.add_argument('--count_per_relation', default=10, type=int)
    flags.add_argument('--relation', action='append')
    flags.add_argument('--parallelism', default=1, type=int)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    N_ARTICLES = 100
    N_COMPLETE_NEGATIVES = 1000
    N_CROSSUSED_POSITIVES = 1000

    art_set = article_set.ArticleSet()

    if not args.relation:
        relations = sample_repo.all_relations()
    else:
        relations = args.relation

    # Load all documents.
    global documents
    documents = []
    article_names = art_set.article_names[:]
    random.shuffle(article_names)
    article_names = article_names[:N_ARTICLES]
    for i, article_title in enumerate(article_names):
        print('loading article (', i, '/', len(article_names), ')')
        document = sample_generation.try_load_document(article_title)
        if not document:
            continue
        documents.append(document)

    wikidata_client = wikidata.WikidataClient()
    all_relations = sample_repo.all_relations()
    all_positive_samples = []
    for i, r in enumerate(all_relations):
        print('loading positives for', r, '(', i, '/', len(all_relations), ')')
        try:
            all_positive_samples.extend(sample_repo.load_positive_samples(r))
        except AssertionError as e:
            print(e)
            pass

    global complete_negatives
    complete_negatives = []
    print('Generating', N_COMPLETE_NEGATIVES, 'complete negatives...')
    for i in range(N_COMPLETE_NEGATIVES):
        if i % 100 == 0:
            print(i, '/', N_COMPLETE_NEGATIVES)
        sample = sample_generation.sample_complete_negative(
            documents,
            wikidata_client = wikidata_client,
        )
        complete_negatives.append(sample)

    global negative_samples
    negative_samples = {relation: [] for relation in relations}
    random.shuffle(all_positive_samples)

    for i, positive_sample in enumerate(all_positive_samples[:N_CROSSUSED_POSITIVES]):
        if i % 1000 == 0:
            print(i, '/', len(all_positive_samples))
        # TODO: we care only about sentence ID and mentions in it.
        holding_relations = wikidata_client.get_holding_relations_between(
            positive_sample.subject, positive_sample.object)

        for negative_relation in set(relations) - set(holding_relations):
            # TODO
            negated = training_sample.TrainingSample.from_json(positive_sample.to_json())
            negated.positive = False
            negated.relation = negative_relation
            negative_samples[negative_relation].append(negated)

    pool = multiprocessing.Pool(args.parallelism)

    for relation in relations:
        process_relation(pool, relation,
                         args.count_per_relation, args.parallelism)

if __name__ == '__main__':
    main()
