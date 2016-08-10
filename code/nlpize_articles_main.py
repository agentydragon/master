#!/usr/bin/python3

"""
TODO

Usage:
    TODO
"""

import argparse
import subprocess
import file_util
import os.path
import paths

parser = argparse.ArgumentParser(description='TODO')
# parser.add_argument('--plaintexts_dir')
# parser.add_argument('--plaintexts', action='append')
parser.add_argument('--plaintext_files', action='append')
parser.add_argument('--output_parse_xmls_dir')
parser.add_argument('--parallel_runs', type=int)
args = parser.parse_args()

file_util.ensure_dir(args.output_parse_xmls_dir)

plaintext_paths = []
#for root, subdirs, files in os.walk(args.plaintexts_dir):
#    for filename in files:
#        plaintext_path = os.path.join(root, filename)
for plaintext_path in args.plaintext_files:
    filename = plaintext_path.split('/')[-1]
    article_sanename = '.'.join(filename.split('.')[:-1])
    output_file = args.output_parse_xmls_dir + '/' + article_sanename + '.txt.out'

    if os.path.isfile(output_file):
        # done, skip
        continue

    plaintext_paths.append(plaintext_path)

plaintext_paths.sort()

minibatch_size = 3
# batch_size = 10
batch_size = (minibatch_size * args.parallel_runs)

parallelize = True

def make_commandline(file_paths):
    commandline = [paths.CORENLP_RUNNER_SH,
                   '-outputDirectory', args.output_parse_xmls_dir,
                   '-annotators', 'tokenize,ssplit,parse,lemma,ner,dcoref']
    for path in file_paths:
        commandline.extend(['-file', path])
    print(commandline)
    return commandline

def run_batch(path_slice):
    if parallelize:

        popens = []
        for i in range(0, len(path_slice), minibatch_size):
            minibatch = path_slice[i:i+minibatch_size]
            commandline = make_commandline(minibatch)
            popens.append(subprocess.Popen(commandline))

        for popen in popens:
            popen.wait()

        for popen in popens:
            if popen.returncode != 0:
                print("error processing slice:", path_slice,
                      "exit code:", popen.returncode)
            # assert popen.returncode == 0

    else:
        commandline = make_commandline(path_slice)
        print(commandline)
        subprocess.check_call(commandline)

for i in range(0, len(plaintext_paths), batch_size):
    path_slice = plaintext_paths[i:i+batch_size]
    print(path_slice)
    run_batch(path_slice)
