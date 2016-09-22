from prototype.lib import sample_repo
from prototype.lib import wikidata
import argparse
import json

client = wikidata.WikidataClient()

def show_all_relations():
    for relation in sample_repo.all_relations():
        samples = sample_repo.load_samples(relation)
        positive = list(filter(lambda sample: sample.positive, samples))
        negative = list(filter(lambda sample: not sample.positive, samples))
        print(relation,
              client.get_name(relation), ":",
              len(samples), "samples",
              len(positive), "positive",
              len(negative), "negative")

def show_relation(relation):
    samples = sample_repo.load_samples(relation)

    html = ""
    html += """
    <style>
    li.positive { color: darkgreen; }
    li.negative { color: darkred; }
    .token.subject { text-decoration: underline; color: #999; }
    .token.object { text-style: italic; color: #999; }
    </style>
    """
    html += "<h1>" + relation + ": " + client.get_name(relation) + "</h1>"

    for sample in samples:
        html += "<li class='%s'>" % ('positive' if sample.positive else
                                     'negative')
        html += sample.subject + " " + sample.object + " "
        # html += sample.sentence.text
        arry = sample.to_json()
        del arry['sentence']['tokens']
        del arry['sentence']['text']
        del arry['subject_token_indices']
        del arry['object_token_indices']
        del arry['subject']
        del arry['object']
        del arry['relation']
        html += str(arry)
        html += "<div class='tokens'>"
        for i, token in enumerate(sample.sentence.tokens):
            classes = []
            if i in sample.subject_token_indices:
                classes.append('subject')
            if i in sample.object_token_indices:
                classes.append('object')

            start = token.start_offset
            end = token.end_offset
            text = sample.sentence.text[start:end]
            ary = token.to_json()
            del ary['start_offset']
            del ary['end_offset']
            html += "<span class='token " + (" ".join(classes)) + "' data-json='" + json.dumps(ary) + "'>" + text + "</span>"
            html += " "
        html += "</div>"


    print(html)

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--relation')
    args = parser.parse_args()

    if args.relation:
        relation = args.relation
        show_relation(relation)
    else:
        show_all_relations()

if __name__ == '__main__':
    main()
