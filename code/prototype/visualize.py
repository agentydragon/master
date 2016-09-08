from prototype.lib import article_repo
from prototype.lib import parse_xmls_to_protos
from xml.etree import ElementTree
from py import paths

def document_to_html(document):
    html = ""
    html += "<pre>"
    html += document.text
    html += "</pre>"
    html += ""

    for sentence in document.sentences:
        html += "<pre>"
        html += sentence.text
        html += "</pre>"

        for coreference in document.coreferences:
            for mention in coreference.mentions:
                if mention.sentence_id == sentence.id:
                    html += str(coreference.wikidata_entity_id) + ": " + str(mention) + "<br>"

    return html

article = article_repo.load_article(paths.WIKI_ARTICLES_PLAINTEXTS_DIR, "Douglas Adams")
proto = parse_xmls_to_protos.document_to_proto(
    root = ElementTree.fromstring(article['corenlp_xml']),
    spotlight_json = article['spotlight_json'],
    plaintext = article['plaintext'],
)
print(document_to_html(proto))
