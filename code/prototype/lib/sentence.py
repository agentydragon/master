# from collections import namedtuple
import recordclass

k = recordclass.recordclass

class SentenceToken(k("SentenceToken",
                      ["id", "start_offset", "end_offset", "lemma", "pos",
                       "word", "ner"])):
    def to_json(self):
        return {
            'id': self.id,
            'start_offset': self.start_offset,
            'end_offset': self.end_offset,
            'lemma': self.lemma,
            'pos': self.pos,
            'word': self.word,
            'ner': self.ner,
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            id = json['id'],
            start_offset = json['start_offset'],
            end_offset = json['end_offset'],
            lemma = json['lemma'],
            pos = json['pos'],
            word = json['word'],
            ner = json['ner'],
        )


class Mention(k("Mention",
                ["sentence_id", "start_word_id", "end_word_id", "text"])):
    def to_json(self):
        return {
            'sentence_id': self.sentence_id,
            'start_word_id': self.start_word_id,
            'end_word_id': self.end_word_id,
            'text': self.text,
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            sentence_id = json['sentence_id'],
            start_word_id = json['start_word_id'],
            end_word_id = json['end_word_id'],
            text = json['text']
        )

class Coreference(k("Coreference",
                    ["mentions", "wikidata_entity_id"])):
    def to_json(self):
        return {
            'mentions': map(Mention.to_json, self.mentions),
            'wikidata_entity_id': self.wikidata_entity_id,
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            mentions = map(Mention.from_json, self.mentions),
            wikidata_entity_id = json['wikidata_entity_id']
        )

class SavedDocument(k("SavedDocument", ["plaintext", "corenlp_xml",
                                        "spotlight_json",
                                        "proto",
                                        "title"])):
    def to_json(self):
        return {
            'title': self.title,
            'plaintext': self.plaintext,
            'corenlp_xml': self.corenlp_xml,
            'spotlight_json': self.spotlight_json,
            'proto': (self.proto.to_json() if self.proto else None),
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            title = (json['title'] if 'title' in json else None),
            plaintext = json['plaintext'],
            corenlp_xml = (json['corenlp_xml']
                           if ('corenlp_xml' in json and json['corenlp_xml'])
                           else None),
            spotlight_json = (json['spotlight_json']
                              if ('spotlight_json' in json and json['spotlight_json'])
                              else None),
            proto = (DocumentProto.from_json(json['proto'])
                     if ('proto' in json and json['proto'])
                     else None)
        )

class DocumentProto(k("DocumentProto", ["title", "text",
                                        "sentences", "coreferences",
                                        "spotlight_mentions"])):
    def to_json(self):
        return {
            'title': self.title,
            'text': self.text,
            'sentences': map(DocumentSentence.to_json, self.sentences),
            'coreferences': map(Coreference.to_json, self.coreferences),
            'spotlight_mentions': map(SpotlightMention.to_json,
                                      self.spotlight_mentions),
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            title = json['title'],
            text = json['text'],
            sentences = map(DocumentSentence.from_json, json['sentences']),
            coreferences = map(Coreference.from_json, json['coreferences']),
            spotlight_mentions = map(SpotlightMention.from_json,
                                     json['spotlight_mentions']),
        )

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

class SpotlightMention(k("SpotlightMention",
                         ["start_offset", "end_offset", "surface_form",
                          "uri"])):
    def to_json(self):
        return {
            'start_offset': self.start_offset,
            'end_offset': self.end_offset,
            'surface_form': self.surface_form,
            'uri': self.uri
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            start_offset = json['start_offset'],
            end_offset = json['end_offset'],
            surface_form = json['surface_form'],
            uri = json['uri'],
        )

class DocumentSentence(k("DocumentSentence", ["id", "text", "tokens"])):
    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
            'tokens': map(SentenceToken.to_json, self.tokens),
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            id = json['id'],
            text = json['text'],
            tokens = map(SentenceToken.from_json, json['tokens']),
        )

    def start_offset(self):
        return self.tokens[0].start_offset

    def end_offset(self):
        return self.tokens[-1].end_offset

    def find_token_by_id(self, token_id):
        for token in self.tokens:
            if token.id == token_id:
                return token
