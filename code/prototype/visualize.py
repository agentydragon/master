from prototype.lib import article_repo
from prototype.lib import parse_xmls_to_protos
from xml.etree import ElementTree

article = article_repo.load_article("Douglas Adams")
proto = parse_xmls_to_protos.document_to_proto(
    root = ElementTree.fromstring(article['corenlp_xml']),
    spotlight_json = article['spotlight_json'],
    plaintext = article['plaintext'],
)

print(str(proto))
