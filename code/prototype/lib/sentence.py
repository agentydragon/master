# from collections import namedtuple
import recordclass

k = recordclass.recordclass

SentenceToken = k("SentenceToken",
                           ["id", "start_offset", "end_offset", "lemma", "pos",
                           "word", "ner"])
Mention = k("Mention",
                     ["sentence_id", "start_word_id", "end_word_id", "text"])
Coreference = k("Coreference",
                         ["mentions", "wikidata_entity_id"])

class Document(k("Document", ["title", "text", # "corenlp_xml", "spotlight_json",
                              "sentences", "coreferences",
                              "spotlight_mentions"])):
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

SpotlightMention = k("SpotlightMention",
                              ["start_offset",
                              "end_offset",
                              "surface_form",
                              "uri"])
class DocumentSentence(k("DocumentSentence", ["id", "text", "tokens"])):
    def start_offset(self):
        return self.tokens[0].start_offset

    def end_offset(self):
        return self.tokens[-1].end_offset

    def find_token_by_id(self, token_id):
        for token in self.tokens:
            if token.id == token_id:
                return token
