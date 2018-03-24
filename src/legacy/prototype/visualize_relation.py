from src.prototype.lib import sample_repo
from src.prototype.lib import flags
from src.prototype.lib import wikidata
import json

#def show_all_relations(client):
#    for relation in sample_repo.all_relations():
#        samples = sample_repo.load_samples(relation)
#        positive = list(filter(lambda sample: sample.positive, samples))
#        negative = list(filter(lambda sample: not sample.positive, samples))
#        print(relation,
#              client.get_name(relation), ":",
#              len(samples), "samples",
#              len(positive), "positive",
#              len(negative), "negative")
#
#def show_relation(client, relation):
#    samples = sample_repo.load_samples(relation)
#
#    html = ""
#    html += """
#    <style>
#    li.positive { color: darkgreen; }
#    li.negative { color: darkred; }
#    .token.subject { text-decoration: underline; color: #999; }
#    .token.object { text-style: italic; color: #999; }
#    </style>
#    """
#    html += "<h1>" + relation + ": " + client.get_name(relation) + "</h1>"
#
#    for sample in samples:
#        html += "<li class='%s'>" % ('positive' if sample.positive else
#                                     'negative')
#        html += sample.subject + " " + sample.object + " "
#        # html += sample.sentence.text
#        arry = sample.to_json()
#        del arry['sentence']['tokens']
#        del arry['sentence']['text']
#        del arry['subject_token_indices']
#        del arry['object_token_indices']
#        del arry['subject']
#        del arry['object']
#        del arry['relation']
#        html += str(arry)
#        html += "<div class='tokens'>"
#        for i, token in enumerate(sample.sentence.tokens):
#            classes = []
#            if i in sample.subject_token_indices:
#                classes.append('subject')
#            if i in sample.object_token_indices:
#                classes.append('object')
#
#            start = token.start_offset
#            end = token.end_offset
#            text = sample.sentence.text[start:end]
#            ary = token.to_json()
#            del ary['start_offset']
#            del ary['end_offset']
#            html += "<span class='token " + (" ".join(classes)) + "' data-json='" + json.dumps(ary) + "'>" + text + "</span>"
#            html += " "
#        html += "</div>"
#
#
#    print(html)
#
#def main():
#    flags.add_argument('--relation')
#    flags.make_parser(description='TODO')
#    args = flags.parse_args()
#
#    client = wikidata.WikidataClient()
#
#    if args.relation:
#        relation = args.relation
#        show_relation(client, relation)
#    else:
#        show_all_relations(client)

if __name__ == '__main__':
    main()
