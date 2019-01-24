import sys
import json
import requests
import urllib.parse
import os.path
import glob

d = 'individual-articles'

with open('sentences', 'w') as sf:
    for file in glob.glob(os.path.join(d, '*', '*', '*.plaintext')):
        corenlp_file = file + ".corenlpjson"
        spotlight_file = file + ".spotlightjson"
        if not os.path.isfile(corenlp_file) or not os.path.isfile(spotlight_file):
            continue
        print(file)

        with open(file) as f:
            content = f.read()
        try:
            with open(corenlp_file) as f:
                corenlp = json.load(f)
            with open(spotlight_file) as f:
                spotlight = json.load(f)
        except Exception as e:
            print(e)
            continue
        if "Resources" not in spotlight:
            continue

        # if len(content) > 200 or len(content) < 100:
        #     continue

        # print(content)
        # print(corenlp)
        # print(spotlight)

        for sentence in corenlp["sentences"]:
            start = sentence["tokens"][0]["characterOffsetBegin"]
            end = sentence["tokens"][-1]["characterOffsetEnd"]
            sentence_content = content[start:end]
            #print(sentence_content)

            sf.write(sentence_content + '\n')
            print(sentence_content)
            for resource in spotlight["Resources"]:
                offset = int(
                    resource["@offset"])
                if offset >= start and offset < end:
                    print(resource["@URI"], resource["@surfaceForm"],
                          resource["@similarityScore"],
                          resource["@support"],
                          resource["@percentageOfSecondRank"])
                    sf.write('%d %d %s %s\n' % (offset - start,
                                                offset - start +
                                                len(
                                                    resource["@surfaceForm"]),
                                                resource["@URI"],
                                                resource["@surfaceForm"]
                                                ))
            sf.write('\n')
            print()

            # sys.exit(0)

# TODO(prvak): Now, what about 'confidence'? That's used for disambiguation.
