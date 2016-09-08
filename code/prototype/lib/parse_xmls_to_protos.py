import sentence_pb2
from xml.etree import ElementTree
from py import dbpedia

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

    document.coreferences.add().mentions.add(
        sentence_id = sentence_id,
        start_word_id = start_token.id,
        end_word_id = end_token.id + 1,
        text = document.text[start_token.start_offset:end_token.end_offset]
    )

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
    for mention_json in spotlight_json['Resources']:
        if not mention_json['@surfaceForm']:
            # TODO HACK?
            continue
        mention = sentence_pb2.SpotlightMention(
            start_offset = int(mention_json['@offset']),
            uri = mention_json['@URI']
        )
        surface_form = mention_json['@surfaceForm']
        mention.end_offset = mention.start_offset + len(surface_form)
        mention.surface_form = surface_form
        mentions.append(mention)
    return mentions

def find_sentence_by_id(document, sentence_id):
    for sentence in document.sentences:
        if sentence.id == sentence_id:
            return sentence

def find_sentence_token(sentence, token_id):
    for token in sentence.tokens:
        if token.id == token_id:
            return token

def get_mention_start(document, mention):
    sentence = find_sentence_by_id(document, mention.sentence_id)
    token = find_sentence_token(sentence, mention.start_word_id)
    return token.start_offset

def get_mention_end(document, mention):
    sentence = find_sentence_by_id(document, mention.sentence_id)
    token = find_sentence_token(sentence, mention.end_word_id - 1)
    return token.end_offset

def find_resources_between(spotlight_mentions, start, end):
    return [mention for mention in spotlight_mentions
            if mention.start_offset >= start and mention.end_offset <= end]

def annotate_coreferences(document, spotlight_json):
    spotlight_mentions = spotlight_to_mentions(spotlight_json)
    for coreference in document.coreferences:
        full_matches = []

        for mention in coreference.mentions:
            mention_start = get_mention_start(document, mention)
            mention_end = get_mention_end(document, mention)
            # if mention_end == -1:
            #     # TODO HAX
            #     continue
            mention_text = mention.text
            mention_actual_text = document.text[mention_start:mention_end]
            # if mention_text != mention_actual_text:
            #     # TODO: check equality

            full_matches = []
            for resource in find_resources_between(spotlight_mentions,
                                                   mention_start,
                                                   mention_end):
                if resource.surface_form in [mention_text, mention_actual_text]:
                    full_matches.append(resource)
                else:
                    pass # TODO: ?

            uris = set(match.uri for match in full_matches)
            if len(uris) == 1:
                best_match = list(uris)[0]
                wikidata_id = dbpedia.dbpedia_uri_to_wikidata_id(best_match)
                if wikidata_id:
                    coreference.wikidata_entity_id = wikidata_id
            # TODO: else?

def document_to_proto(root, spotlight_json, plaintext):
    # TODO: Spotlight JSON
    """
    Args:
        root (xml.etree.Element)
        spotlight_json (dict) Spotlight's JSON response
        plaintext (str)
    """

    document = sentence_pb2.Document(
        text = plaintext
    )
    sentence_tags = root.find('document').find('sentences').findall('sentence')
    for sentence_tag in sentence_tags:
        sentence = document.sentences.add(
            id = int(sentence_tag.attrib['id'])
        )

        sentence_begin = None

        for token_tag in sentence_tag.find('tokens').findall('token'):
            token_start = int(token_tag.find('CharacterOffsetBegin').text)
            token_end = int(token_tag.find('CharacterOffsetEnd').text)

            sentence_end = token_end
            if sentence_begin is None:
                sentence_begin = token_start

            sentence.tokens.add(
                id = int(token_tag.attrib['id']),
                start_offset = token_start,
                end_offset = token_end,
                lemma = token_tag.find('lemma').text,
                word = token_tag.find('word').text,
                pos = token_tag.find('POS').text,
                ner = token_tag.find('NER').text
            )
        sentence.text = plaintext[sentence_begin:sentence_end]

    for coreference_tag in root.find('document').find('coreference').findall('coreference'):
        coreference = document.coreferences.add()

        for mention_tag in coreference_tag.findall('mention'):
            coreference.mentions.add(
                start_word_id = int(mention_tag.find('start').text),
                end_word_id = int(mention_tag.find('end').text),
                sentence_id = int(mention_tag.find('sentence').text),
                text = mention_tag.find('text').text
            )

    add_single_referenced_entities_to_coreferences(document)

    annotate_coreferences(document, spotlight_json)

    return document
