from prototype.lib import sample_repo
import argparse

def main():
    parser = argparse.ArgumentParser(description='TODO')
    args = parser.parse_args()

    for relation in sample_repo.all_relations():
        samples = sample_repo.load_samples_by_articles(relation)
        sample_repo.write_positive_samples(relation, samples)
        print(relation, 'positives joined')

if __name__ == '__main__':
    main()
