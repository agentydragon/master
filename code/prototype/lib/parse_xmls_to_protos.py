from prototype.lib import sentence

from xml.etree import ElementTree
from prototype.lib import dbpedia

BANNED_NERS = ['O', 'ORDINAL', 'DATE', 'NUMBER', 'DURATION']

# TODO: add protobuf wrapper objects

def flush_named_entity(document, ner, start_token, end_token, sentence_id):
    if ner in BANNED_NERS:
        return

    found = False
    for coreference in document.coreferences:
        for mention in coreference.mentions:
            if mention.sentence_id == sentence_id and mention.start_word_id >= start_token.id and (mention.end_word_id - 1) <= end_token.id:
                found = True
    if found:
        return

    coreference = sentence.Coreference(
        mentions = [
            sentence.Mention(
                sentence_id = sentence_id,
                start_word_id = start_token.id,
                end_word_id = end_token.id + 1,
                text = document.text[start_token.start_offset:end_token.end_offset]
            )
        ],
        wikidata_entity_id = None
    )
    document.coreferences.append(coreference)
    #document.coreferences.add().mentions.add(

def add_single_referenced_entities_to_coreferences(document):
    """
    Args:
        document (sentence_pb.Document)
    """
    for sentence in document.sentences:
        last_ner = None
        last_ne_tokens = []

        for token in sentence.tokens:
            if token.ner == last_ner:
                last_ne_tokens.append(token)
            else:
                if last_ner is not None:
                    flush_named_entity(document, last_ner, last_ne_tokens[0],
                                       last_ne_tokens[-1], sentence.id)
                last_ner = token.ner
                last_ne_tokens = [token]
        if last_ner is not None:
            flush_named_entity(document, last_ner, last_ne_tokens[0],
                               last_ne_tokens[-1], sentence.id)

def spotlight_to_mentions(spotlight_json):
    mentions = []

    # TODO: fix?
    if 'Resources' not in spotlight_json:
        print("WARN: no resources returned by Spotlight")
        return []

    for mention_json in spotlight_json['Resources']:
        if not mention_json['@surfaceForm']:
            # TODO HACK?
            continue
        mention = sentence.SpotlightMention(
            start_offset = int(mention_json['@offset']),
            uri = mention_json['@URI'],
            end_offset = None,
            surface_form = None
        )
        surface_form = mention_json['@surfaceForm']
        mention.end_offset = mention.start_offset + len(surface_form)
        mention.surface_form = surface_form
        mentions.append(mention)
    return mentions

# def annotate_coreferences(document):
#     for coreference in document.coreferences:
#         full_matches = []
# 
#         for mention in coreference.mentions:
#             mention_start = get_mention_start(document, mention)
#             mention_end = get_mention_end(document, mention)
#             # if mention_end == -1:
#             #     # TODO HAX
#             #     continue
#             mention_text = mention.text
#             mention_actual_text = document.text[mention_start:mention_end]
#             # if mention_text != mention_actual_text:
#             #     # TODO: check equality
# 
#             full_matches = []
#             for resource in document.find_spotlight_mentions_between(
#                     mention_start, mention_end):
#                 if resource.surface_form in [mention_text, mention_actual_text]:
#                     full_matches.append(resource)
#                 else:
#                     pass # TODO: ?
# 
#             uris = set(match.uri for match in full_matches)
#             if len(uris) == 1:
#                 best_match = list(uris)[0]
#                 wikidata_id = dbpedia.dbpedia_uri_to_wikidata_id(best_match)
#                 if wikidata_id:
#                     coreference.wikidata_entity_id = wikidata_id
#             # TODO: else?

def document_to_proto(title, document):
    # TODO: Spotlight JSON
    """
    Args:
        root (xml.etree.Element)
        spotlight_json (dict) Spotlight's JSON response
        plaintext (str)
    """

    root = ElementTree.fromstring(document.corenlp_xml)
    plaintext = document.plaintext
    spotlight_json = document.spotlight_json

    document = sentence.DocumentProto(
        title = title,
        text = plaintext,
        sentences = [],
        coreferences = [],
        spotlight_mentions = spotlight_to_mentions(spotlight_json)
    )
    sentence_tags = root.find('document').find('sentences').findall('sentence')
    for sentence_tag in sentence_tags:
        # this_sentence = document.sentences.add(
        this_sentence = sentence.DocumentSentence(
            text = None,
            tokens = [],
            id = int(sentence_tag.attrib['id'])
        )
        document.sentences.append(this_sentence)

        sentence_begin = None

        for token_tag in sentence_tag.find('tokens').findall('token'):
            token_start = int(token_tag.find('CharacterOffsetBegin').text)
            token_end = int(token_tag.find('CharacterOffsetEnd').text)

            sentence_end = token_end
            if sentence_begin is None:
                sentence_begin = token_start

            # this_sentence.tokens.add(
            this_token = sentence.SentenceToken(
                id = int(token_tag.attrib['id']),
                start_offset = token_start,
                end_offset = token_end,
                lemma = token_tag.find('lemma').text,
                word = token_tag.find('word').text,
                pos = token_tag.find('POS').text,
                ner = token_tag.find('NER').text
            )
            this_sentence.tokens.append(this_token)
        this_sentence.text = plaintext[sentence_begin:sentence_end]

    coreferences_tag = root.find('document').find('coreference')
    # Coreference tag may be missing.
    if coreferences_tag:
        coreference_tags = coreferences_tag.findall('coreference')
    else:
        coreference_tags = []
    for coreference_tag in coreference_tags:
        # coreference = document.coreferences.add()
        coreference = sentence.Coreference(
            mentions = [],
            wikidata_entity_id = None
        )
        document.coreferences.append(coreference)

        for mention_tag in coreference_tag.findall('mention'):
            # coreference.mentions.add(
            mention = sentence.Mention(
                start_word_id = int(mention_tag.find('start').text),
                end_word_id = int(mention_tag.find('end').text),
                sentence_id = int(mention_tag.find('sentence').text),
                text = mention_tag.find('text').text
            )
            coreference.mentions.append(mention)

    # add_single_referenced_entities_to_coreferences(document)
    # annotate_coreferences(document)

    return document
