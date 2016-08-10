#!/usr/bin/python3

"""
TODO

Usage:
    TODO
"""

import argparse
import annotate_coreferences
import file_util
from google.protobuf import text_format
import os.path
import paths

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--input_protos_dir',
                        default=paths.PARSE_PROTOS_DIR)
    parser.add_argument('--spotlight_dir',
                        default=paths.SPOTLIGHT_ANNOTATIONS_DIR)
    parser.add_argument('--output_protos_dir',
                        default=paths.ANNOTATED_DOCUMENTS_DIR)
    args = parser.parse_args()

    file_util.ensure_dir(args.output_protos_dir)

    for root, subdirs, files in os.walk(args.input_protos_dir):
        for filename in files:
            input_proto_path = os.path.join(root, filename)
            document = annotate_coreferences.load_document(input_proto_path)

            article_sanename = document.article_sanename
            spotlight_path = os.path.join(args.spotlight_dir, article_sanename + ".spotlight.json")
            if not os.path.isfile(spotlight_path):
                print(article_sanename, "skipped, parsed but not spotlighted")
                continue

            output_path = os.path.join(args.output_protos_dir, article_sanename + ".propagated.pb")
            if os.path.isfile(output_path):
                print(article_sanename, "already processed")
                continue

            print(article_sanename, "processing")

            spotlight = annotate_coreferences.load_spotlight(spotlight_path)
            annotate_coreferences.propagate_entities(document, spotlight)

            #print(text_format.MessageToString(document))
            with open(output_path, 'wb') as f:
                f.write(document.SerializeToString())

if __name__ == '__main__':
    main()
