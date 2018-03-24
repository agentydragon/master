# from collections import namedtuple
import recordclass
from xml.etree import ElementTree

k = recordclass.recordclass

class SentenceToken(k("SentenceToken",
                      ["id", "start_offset", "end_offset", "lemma", "pos",
                       "word", "ner"])):
    ID = 'id'
    START_OFFSET = 'start_offset'
    END_OFFSET = 'end_offset'
    LEMMA = 'lemma'
    POS = 'pos'
    WORD = 'word'
    NER = 'ner'

    def to_json(self):
        return {
            ID: self.id,
            START_OFFSET: self.start_offset,
            END_OFFSET: self.end_offset,
            LEMMA: self.lemma,
            POS: self.pos,
            WORD: self.word,
            NER: self.ner,
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            id = json[klass.ID],
            start_offset = json[klass.START_OFFSET],
            end_offset = json[klass.END_OFFSET],
            lemma = json[klass.LEMMA],
            pos = json[klass.POS],
            word = json[klass.WORD],
            ner = json[klass.NER],
        )

class Mention(k("Mention",
                ["sentence_id", "start_word_id", "end_word_id", "text"])):
    SENTENCE_ID = "sentence_id"
    START_WORD_ID = "start_word_id"
    END_WORD_ID = "end_word_id"
    TEXT = "text"

    def to_json(self):
        return {
            SENTENCE_ID: self.sentence_id,
            START_WORD_ID: self.start_word_id,
            END_WORD_ID: self.end_word_id,
            TEXT: self.text,
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            sentence_id = json[klass.SENTENCE_ID],
            start_word_id = json[klass.START_WORD_ID],
            end_word_id = json[klass.END_WORD_ID],
            text = json[klass.TEXT]
        )

class Coreference(k("Coreference",
                    ["mentions"])):
    MENTIONS = "mentions"

    def to_json(self):
        return {
            MENTIONS: list(map(Mention.to_json, self.mentions)),
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            mentions = list(map(Mention.from_json, json[klass.MENTIONS])),
        )

class SpotlightMention(k("SpotlightMention",
                         ["start_offset", "end_offset", "surface_form",
                          "uri",
                          "wikidata_id"])):
    START_OFFSET = "start_offset"
    END_OFFSET = "end_offset"
    SURFACE_FORM = "surface_form"
    URI = "uri"
    WIKIDATA_ID = "wikidata_id"

    def to_json(self):
        return {
            START_OFFSET: self.start_offset,
            END_OFFSET: self.end_offset,
            SURFACE_FORM: self.surface_form,
            URI: self.uri,
            WIKIDATA_ID: self.wikidata_id
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            start_offset = json[klass.START_OFFSET],
            end_offset = json[klass.END_OFFSET],
            surface_form = json[klass.SURFACE_FORM],
            uri = json[klass.URI],
            wikidata_id = (json[klass.WIKIDATA_ID] if klass.WIKIDATA_ID in json else None),
        )

    @classmethod
    def mentions_from_spotlight_json(klass, spotlight_json, dbpedia_client):
        mentions = []

        # TODO: fix?
        if 'Resources' not in spotlight_json:
            print("WARN: no resources returned by Spotlight")
            return []

        dbpedia_uris = set(mention_json['@URI']
                           for mention_json
                           in spotlight_json['Resources'])
        dbpedia_uri_to_wikidata_id = dbpedia_client.dbpedia_uris_to_wikidata_ids(dbpedia_uris)

        for mention_json in spotlight_json['Resources']:
            if not mention_json['@surfaceForm']:
                # TODO HACK?
                continue

            uri = mention_json['@URI']
            if uri in dbpedia_uri_to_wikidata_id:
                wikidata_id = dbpedia_uri_to_wikidata_id[uri]
            else:
                print('WARN: No translation:', uri)
                wikidata_id = None

            mention = klass(
                start_offset = int(mention_json['@offset']),
                uri = uri,
                end_offset = None,
                surface_form = None,
                wikidata_id = wikidata_id,
            )

            surface_form = mention_json['@surfaceForm']
            mention.end_offset = mention.start_offset + len(surface_form)
            mention.surface_form = surface_form
            mentions.append(mention)
        return mentions


class DocumentSentence(k("DocumentSentence", ["id", "text", "tokens"])):
    ID = 'id'
    TEXT = 'text'
    TOKENS = 'tokens'

    def to_json(self):
        return {
            ID: self.id,
            TEXT: self.text,
            TOKENS: list(map(SentenceToken.to_json, self.tokens)),
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            id = json[klass.ID],
            text = json[klass.TEXT],
            tokens = list(map(SentenceToken.from_json, json[klass.TOKENS])),
        )

    def start_offset(self):
        return self.tokens[0].start_offset

    def end_offset(self):
        return self.tokens[-1].end_offset

    def find_token_by_id(self, token_id):
        for token in self.tokens:
            if token.id == token_id:
                return token

class SavedDocument(k("SavedDocument", [
        "title",
        "plaintext",
        "corenlp_xml",
        "spotlight_json",

        # Generated by add_join.
        "sentences",
        "coreferences",
        "spotlight_mentions",
])):
    def to_json(self):
        json = {
            'title': self.title,
            'plaintext': self.plaintext,
            'corenlp_xml': self.corenlp_xml,
            'spotlight_json': self.spotlight_json,
        }

        if self.sentences is not None:
            json['sentences'] = list(map(DocumentSentence.to_json, self.sentences))
        if self.coreferences is not None:
            json['coreferences'] = list(map(Coreference.to_json, self.coreferences))
        if self.spotlight_mentions is not None:
            json['spotlight_mentions'] = list(map(SpotlightMention.to_json, self.spotlight_mentions))

        return json

    @classmethod
    def from_json(klass, json):
        data = dict(
            title = (json['title'] if 'title' in json else None),
            plaintext = json['plaintext'],
            corenlp_xml = (json['corenlp_xml']
                           if ('corenlp_xml' in json and json['corenlp_xml'])
                           else None),
            spotlight_json = (json['spotlight_json']
                              if ('spotlight_json' in json and json['spotlight_json'])
                              else None),
        )

        if 'sentences' in json:
            data['sentences'] = list(map(DocumentSentence.from_json, json['sentences']))
        else:
            data['sentences'] = None

        if 'coreferences' in json:
            data['coreferences'] = list(map(Coreference.from_json, json['coreferences']))
        else:
            data['coreferences'] = None

        if 'spotlight_mentions' in json:
            data['spotlight_mentions'] = list(map(SpotlightMention.from_json, json['spotlight_mentions']))
        else:
            data['spotlight_mentions'] = None

        return klass(**data)

    # Works when document is processed.
    def find_spotlight_mentions_between(self, start, end):
        return [mention for mention in self.spotlight_mentions
                if mention.start_offset >= start and mention.end_offset <= end]

    def find_sentence_by_id(self, sentence_id):
        for sentence in self.sentences:
            if sentence.id == sentence_id:
                return sentence

    def get_mention_start(self, mention):
        sentence = self.find_sentence_by_id(mention.sentence_id)
        token = sentence.find_token_by_id(mention.start_word_id)
        return token.start_offset

    def get_mention_end(self, mention):
        sentence = self.find_sentence_by_id(mention.sentence_id)
        token = sentence.find_token_by_id(mention.end_word_id - 1)
        return token.end_offset

    def get_spotlight_mentions_in_sentence(self, sentence):
        return self.find_spotlight_mentions_between(sentence.start_offset(),
                                                    sentence.end_offset())

    def add_proto_to_document(self, dbpedia_client):
        self.spotlight_mentions = SpotlightMention.mentions_from_spotlight_json(
            self.spotlight_json,
            dbpedia_client
        )

        root = ElementTree.fromstring(self.corenlp_xml)

        # Add sentences.
        self.sentences = []
        sentence_tags = root.find('document').find('sentences').findall('sentence')
        for sentence_tag in sentence_tags:
            this_sentence = DocumentSentence(
                text = None,
                tokens = [],
                id = int(sentence_tag.attrib['id'])
            )
            self.sentences.append(this_sentence)

            sentence_begin = None

            for token_tag in sentence_tag.find('tokens').findall('token'):
                token_start = int(token_tag.find('CharacterOffsetBegin').text)
                token_end = int(token_tag.find('CharacterOffsetEnd').text)

                sentence_end = token_end
                if sentence_begin is None:
                    sentence_begin = token_start

                this_token = SentenceToken(
                    id = int(token_tag.attrib['id']),
                    start_offset = token_start,
                    end_offset = token_end,
                    lemma = token_tag.find('lemma').text,
                    word = token_tag.find('word').text,
                    pos = token_tag.find('POS').text,
                    ner = token_tag.find('NER').text
                )
                this_sentence.tokens.append(this_token)
            this_sentence.text = self.plaintext[sentence_begin:sentence_end]

        self.coreferences = []
        coreferences_tag = root.find('document').find('coreference')
        # Coreference tag may be missing.
        if coreferences_tag:
            coreference_tags = coreferences_tag.findall('coreference')
        else:
            coreference_tags = []
        for coreference_tag in coreference_tags:
            coreference = Coreference(
                mentions = [],
            )
            self.coreferences.append(coreference)

            for mention_tag in coreference_tag.findall('mention'):
                mention = Mention(
                    start_word_id = int(mention_tag.find('start').text),
                    end_word_id = int(mention_tag.find('end').text),
                    sentence_id = int(mention_tag.find('sentence').text),
                    text = mention_tag.find('text').text
                )
                coreference.mentions.append(mention)

        # add_single_referenced_entities_to_coreferences(proto)
        # annotate_coreferences(proto)

