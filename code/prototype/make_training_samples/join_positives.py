from prototype.lib import sample_repo
from prototype.lib import flags

def main():
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    for relation in sample_repo.all_relations():
        samples = sample_repo.load_samples_by_articles(relation)
        sample_repo.write_positive_samples(relation, samples)
        print(relation, 'positives joined')

if __name__ == '__main__':
    main()
