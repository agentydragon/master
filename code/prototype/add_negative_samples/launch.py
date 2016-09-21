from prototype.lib import sample_repo
from prototype.lib import mapper
import argparse

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--relations_per_job', type=int)
    parser.add_argument('--wikidata_endpoint')
    parser.add_argument('--article_list_file', required=True)
    parser.add_argument('--count_per_relation', type=int, default=1000)
    args = parser.parse_args()

    def make_commandline(relations_slice):
        job_command = ['prototype/add_negative_samples/add_negative_samples',
                       '--article_list_file', args.article_list_file,
                       '--count_per_relation', args.count_per_relation]
        if args.wikidata_endpoint:
            job_command.extend(['--wikidata_endpoint', args.wikidata_endpoint])
        for relation in relations_slice:
            job_command.extend(['--relation', relation])
        return job_command

    mapper.launch_in_slices('add-negative-samples',
                            sample_repo.all_relations(),
                            args.relations_per_job,
                            make_commandline)

if __name__ == '__main__':
    main()
