from prototype.lib import sample_repo
from prototype.lib import flags
import progressbar

def main():
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    bar = progressbar.ProgressBar(redirect_stdout=True)
    for relation in bar(sample_repo.all_relations()):
        samples = sample_repo.load_positive_samples_by_articles(relation)
        sample_repo.write_positive_samples(relation, samples)
        print(relation, 'positives joined', len(samples))

        samples = sample_repo.load_negative_samples_by_articles(relation)
        sample_repo.write_negative_samples(relation, samples)
        print(relation, 'negatives joined', len(samples))

if __name__ == '__main__':
    main()
