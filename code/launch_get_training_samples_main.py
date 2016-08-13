#!/usr/bin/python3

import argparse
import pbs_util
import paths

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--max_documents', type=int, required=True)
    args = parser.parse_args()
    job_command = [
        './get_training_samples_main',
        '--annotated_documents_dir',
        paths.ANNOTATED_DOCUMENTS_DIR,
        '--output_file',
        paths.TRAINING_SAMPLES_FILE,
        '--intermediate_dir',
        paths.TRAINING_SAMPLES_INTERMEDIATE_DIR,
        '--max_documents',
        str(args.max_documents)
    ]
    pbs_util.launch_job(
        walltime="1:00:00",
        node_spec="nodes=1:brno:ppn=1,mem=4gb",
        job_name="get-training-samples",
        job_command=job_command
    )

if __name__ == '__main__':
    main()
