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
        #if "Resources" not in spotlight:
        #    continue
        if 'annotation' not in spotlight:
            continue
        print(file)

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

            for surfaceForm in spotlight["annotation"]["surfaceForm"]:
                offset = int(surfaceForm["@offset"])
                if not (offset >= start and offset < end):
                    continue
                sform = surfaceForm["@name"]
                print(sform)

                # Check that the surface for checks out.
                assert content[offset:offset+len(sform)] == sform

                sf.write('%d %s\n' % (offset, sform))

                resource2 = surfaceForm["resource"]
                if not isinstance(resource2, list):
                    resource2 = [resource2]
                for resource in resource2:
                    uri = resource["@uri"]
                    final_score = float(resource["@finalScore"])
                    print(uri, final_score)
                    sf.write('%s %f\n' % (uri, final_score))
                #for resource in surfaceForm["resource"]:
                # TODO(prvak): No idea whether the 'uri' parameter is useful at all.

                # This is for the "annotate" Spotlight API: for resource in spotlight["Resources"]:
                # This is for the "annotate" Spotlight API:     offset = int(
                # This is for the "annotate" Spotlight API:         resource["@offset"])
                # This is for the "annotate" Spotlight API:     if offset >= start and offset < end:
                # This is for the "annotate" Spotlight API:         print(resource["@URI"], resource["@surfaceForm"],
                # This is for the "annotate" Spotlight API:               resource["@similarityScore"],
                # This is for the "annotate" Spotlight API:               resource["@support"],
                # This is for the "annotate" Spotlight API:               resource["@percentageOfSecondRank"])
                # This is for the "annotate" Spotlight API:         sf.write('%d %d %s %s\n' % (offset - start,
                # This is for the "annotate" Spotlight API:                                     offset - start +
                # This is for the "annotate" Spotlight API:                                     len(
                # This is for the "annotate" Spotlight API:                                         resource["@surfaceForm"]),
                # This is for the "annotate" Spotlight API:                                     resource["@URI"],
                # This is for the "annotate" Spotlight API:                                     resource["@surfaceForm"]
                # This is for the "annotate" Spotlight API:                                     ))
            sf.write('\n')
            print()

            # sys.exit(0)

# TODO(prvak): Now, what about 'confidence'? That's used for disambiguation.
