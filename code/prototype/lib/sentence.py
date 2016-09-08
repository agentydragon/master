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
Document = k("Document",
                      ["title", "text",
                      # "corenlp_xml",
                      # "spotlight_json",
                      "sentences",
                      "coreferences",
                      "spotlight_mentions"])
SpotlightMention = k("SpotlightMention",
                              ["start_offset",
                              "end_offset",
                              "surface_form",
                              "uri"])
DocumentSentence = k("DocumentSentence", ["id", "text", "tokens"])
