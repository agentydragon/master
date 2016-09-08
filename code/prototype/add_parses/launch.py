from py import pbs_util
import argparse
import subprocess

def launch_job_for_slice(articles_slice):
    job_command = ['prototype/add_parses/add_parses'] + articles_slice
    job_id = pbs_util.launch_job(
        # TODO: calculate walltime; parallelize
        walltime="01:00:00",
        node_spec="nodes=1:brno:ppn=4,mem=8gb",
        job_name="add-parses",
        job_command=job_command
    )
    print("Launched add-parses:", job_id)

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--article_list_file', type=str, required=True)
    parser.add_argument('--max_articles', type=int)
    parser.add_argument('--articles_per_job', type=int)
    # TODO: add max_jobs
    args = parser.parse_args()

    with open(args.article_list_file) as f:
        article_names = list(map(lambda line: line.strip(), list(f)))

    if args.max_articles:
        article_names = article_names[:args.max_articles]

    if not args.articles_per_job:
        slices = [article_names]
    else:
        slices = []
        for i in range(0, len(article_names), args.articles_per_job):
            slices.append(article_names[i:i+args.articles_per_job])

    for articles_slice in slices:
        launch_job_for_slice(articles_slice)

if __name__ == '__main__':
    main()
