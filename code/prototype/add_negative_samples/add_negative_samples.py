from prototype.lib import sample_repo
from prototype.lib import sample_generation
from py import wikidata
import argparse
import multiprocessing
import itertools

def generate_negatives_for_relation(article_names, relation, count,
                                    wikidata_endpoint):
    wikidata_client = wikidata.WikidataClient(wikidata_endpoint or None)

    samples = []
    for i in range(count):
        print(i)
        samples.append(sample_generation.sample_negative(article_names,
                                                         relation,
                                                         wikidata_client).to_json())
    return samples

def ll(x):
    return generate_negatives_for_relation(*x)

def process_relation(pool, relation, article_names, count_per_relation,
                     parallelism, wikidata_endpoint):
    indexes = list(range(count_per_relation))
    pool_parts = []
    per_pool = count_per_relation // parallelism
    for i in range(0, count_per_relation, per_pool):
        pool_part = indexes[i:i+per_pool]
        pool_parts.append(pool_part)
        print('pool part', i, len(pool_part))

    pool_parts = list(map(
        lambda pool_part: (
            article_names, relation, len(pool_part), wikidata_endpoint
        ),
        pool_parts
    ))

    parts = pool.map(ll, pool_parts)
    all_samples = list(itertools.chain(*parts))
    print(len(all_samples))
    sample_repo.write_negative_samples(relation, all_samples)
    print("Produced negatives for", relation)

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--article_list_file', required=True)
    parser.add_argument('--wikidata_endpoint')
    parser.add_argument('--count_per_relation', default=10, type=int)
    parser.add_argument('--relation', action='append')
    parser.add_argument('--parallelism', default=1, type=int)
    args = parser.parse_args()

    with open(args.article_list_file) as f:
        article_names = list(map(lambda line: line.strip(), list(f)))

    if not args.relation:
        relations = sample_repo.all_relations()
    else:
        relations = args.relation

    pool = multiprocessing.Pool(parallelism)

    for relation in relations:
        process_relation(pool, relation, article_names,
                         args.count_per_relation, args.parallelism,
                         args.wikidata_endpoint)

if __name__ == '__main__':
    main()
