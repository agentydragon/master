import parse_xmls_to_protos
import argparse
import file_util

def main():
    parser = argparse.ArgumentParser(description='todo')
    parser.add_argument('--plaintexts_dir')
    parser.add_argument('--parse_xmls_dir')
    parser.add_argument('--outputs_dir')
    args = parser.parse_args()

    file_util.ensure_dir(outputs_dir)

    for root, subdirs, files in os.walk(args.plaintexts_dir):
        for filename in files:
            plaintext_path = os.path.join(root, filename)
            article_sanename = '.'.join(filename.split('.')[:-1])

            # (parse_xmls_dir)/Anarchism_in_France.txt.out
            parse_path = os.path.join(args.parse_xmls_dir, article_sanename + ".txt.out")
            if not os.path.isfile(parse_path):
                print(article_sanename, "skipped, not parsed")
                continue

            output_path = os.path.join(args.outputs_dir, article_sanename + ".parse.pb")
            if os.path.isfile(output_path):
                print(article_sanename, "already processed")
                continue

            print(article_sanename, "processing")

            output_document = parse_xml_to_proto(plaintext_path, parse_path)
            output_document.article_sanename = article_sanename

            print(text_format.MessageToString(output_document))
            with open(output_path, 'wb') as f:
                f.write(output_document.SerializeToString())


if __name__ == '__main__':
    main()
