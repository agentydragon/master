from src.prototype.lib import pbs_util
from src.prototype.lib import flags
from src.prototype.lib import article_repo
from src import paths

def main():
    flags.add_argument('--max_articles', type=int)
    flags.add_argument('--wiki_plaintext_path', default=paths.WIKIPEDIA_PLAINTEXT)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    job_command = [
        'prototype/split_wiki/split_wiki_main',
        '--article_plaintexts_dir', article_repo.get_article_plaintexts_dir(),
        '--wiki_plaintext_path', args.wiki_plaintext_path
    ]
    if args.max_articles:
        job_command.extend(['--max_articles', str(args.max_articles)])

    job_id = pbs_util.launch_job(
        walltime="48:00:00",
        # (2016-10-06 prvak) 4 GB RAM not enough
        # (2016-10-07 prvak) 8 GB RAM not enough
        # (2016-10-10 prvak) took 13:44:00 hours
        node_spec="nodes=1:brno:ppn=2,mem=16gb",
        job_name="wiki-split",
        job_command=job_command
    )
    print("Launched wiki split:", job_id)

if __name__ == '__main__':
    main()
