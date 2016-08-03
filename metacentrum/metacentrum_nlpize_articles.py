#!/usr/bin/python3

"""
TODO

Usage:
    TODO
"""

import argparse
import subprocess
import os.path

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--plaintexts_dir')
parser.add_argument('--output_parse_xmls_dir')
args = parser.parse_args()

if not os.path.isdir(args.output_parse_xmls_dir):
    os.makedirs(args.output_parse_xmls_dir)

plaintext_paths = []
for root, subdirs, files in os.walk(args.plaintexts_dir):
    for filename in files:
        plaintext_path = os.path.join(root, filename)

        article_sanename = '.'.join(filename.split('.')[:-1])
        output_file = args.output_parse_xmls_dir + '/' + article_sanename + '.txt.out'

        if os.path.isfile(output_file):
            # done, skip
            continue

        plaintext_paths.append(plaintext_path)

for i in range(0, len(plaintext_paths), 10):
    path_slice = plaintext_paths[i:i+10]
    commandline = ['./metacentrum_corenlp.sh',
                   '-outputDirectory', args.output_parse_xmls_dir,
                   '-annotators', 'tokenize,ssplit,parse,lemma,ner,dcoref']
    for path in path_slice:
        commandline.extend(['-file', path])
    subprocess.check_call(commandline)
