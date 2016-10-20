from src.prototype.lib import mapper
from src.prototype.lib import flags
from src.prototype.lib import article_set
from src.prototype.lib import pbs_util

# job = pbs_util.launch(
#     walltime = "02:00:00",
#     node_spec = "nodes=1:brno:ppn=4,mem=4gb,scratch=200gb",
#     job_name = "local_fuseki",
#     script = "../cpulimit/cpulimit -l 400 local_fuseki/local_fuseki",
# )
# print(job.job_id)

# TODO: wait until it boots up

def main():
    CORES=4

    flags.add_argument('--articles_per_job', type=int)
    flags.make_parser(description='TODO')
    # TODO: add max_jobs
    args = flags.parse_args()

    def make_commandline(articles_slice):
        job_command = ['local_fuseki/local_fuseki']
        for article in articles_slice:
            job_command.extend(['--articles', article])
        print(job_command)
        return job_command

    def slice_to_walltime(articles_slice):
        article_count = len(articles_slice)
        walltime_estimate = round(
            (120 * article_count / float(CORES)) * 2 + 100
        ) # or default: "04:00:00"
        return walltime_estimate

    art_set = article_set.ArticleSet()

    mapper.launch_in_slices(
        'local-mts',
        art_set.article_names,
        args.articles_per_job,
        make_commandline,
        slice_to_walltime,
        cores=CORES,
        scratch='200gb',
        ram='4gb'
    )

if __name__ == '__main__':
    main()
