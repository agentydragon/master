from prototype.lib import article_repo
from prototype.lib import flags
import paths

def document_to_html(document):
    html = ""

    # html += "<pre>"
    # html += document.plaintext
    # html += "</pre>"
    # html += ""

    colors = ['red', 'blue', 'black', 'orange']
    while len(colors) < len(document.coreferences):
        colors.append('black')

    html += """
<style>
.sentence {
    border: 1px solid gray;
    background: lightgray;
    margin: 1em;
}
.coreference-within-sentence {
    border-bottom: 1px solid black;
}
"""
    for i, color in enumerate(colors):
        html += """
.coreference_%d {
    border-bottom: 1px solid %s;
    padding-bottom: 1px;
}""" % (i, color)

    html += """</style>
"""

    for sentence in document.sentences:
        html += "<div class='sentence'>"
        # html += "<pre>"
        # html += sentence.text
        # html += "</pre>"
        for token in sentence.tokens:
            token_text = document.plaintext[token.start_offset:token.end_offset]

            coreference_ids = set()
            for i, coreference in enumerate(document.coreferences):
                for mention in coreference.mentions:
                    if ((mention.sentence_id == sentence.id) and
                            (token.id in range(mention.start_word_id, mention.end_word_id))):
                        coreference_ids.add(i)
            coreference_ids = list(sorted(coreference_ids))

            for i in coreference_ids:
                html += '<span class="coreference_%d">' % i
                html += '<a href="#coreference_%d">' % i
            html += token_text
            for i in coreference_ids:
                html += '</a>'
                html += '</span>'
            html += " "

        #for coreference in document.coreferences:
        #    mentions_in_sentence = [mention for mention in coreference.mentions
        #                            if mention.sentence_id == sentence.id]
        #    if mentions_in_sentence:
        #        html += "<ul class='coreference-within-sentence'>"
        #        for mention in mentions_in_sentence:
        #            html += "<li>" + str(mention) + ""
        #        html += "</ul>"

        #for mention in document.get_spotlight_mentions_in_sentence(sentence):
        #    html += "<b>" + str(mention.wikidata_id) + "</b> "
        #    html += str(mention) + "<br>"

        #for token in sentence.tokens:
        #    html += str(token) + "<br>"
        html += "</div>\n"

    html += "<h2>Coreferences</h2>"
    for i, coreference in enumerate(document.coreferences):
        html += "<h3><a name='coreference_%d'>Coreference %d</a></h3>" % (i, i)
        for mention in coreference.mentions:
            html += "<i>" + str(mention) + "</i>: "
            mention_start = document.get_mention_start(mention)
            mention_end = document.get_mention_end(mention)
            for resource in document.find_spotlight_mentions_between(mention_start, mention_end):
                html += str(resource)
            html += "<br>"

        html += "<hr>"

    return html

def main():
    flags.add_argument('--output_html', required=True)
    article_repository = article_repo.ArticleRepo()
    document = article_repository.load_article("Douglas Adams")

    with open(flags.parse_args().output_html, 'w') as f:
        f.write(document_to_html(document))

if __name__ == '__main__':
    main()
