import json
from xml.etree import ElementTree
from prototype.lib import parse_xmls_to_protos

with open('testdata/Obama.txt.out') as f:
    corenlp_xml = ElementTree.fromstring(f.read())
with open('testdata/Obama.txt') as f:
    plaintext = f.read()
with open('testdata/Obama.spotlight.json') as f:
    spotlight_json = json.load(f)

document_proto = parse_xmls_to_protos.document_to_proto(
    root = corenlp_xml,
    plaintext = plaintext,
    spotlight_json = spotlight_json
)

print(str(document_proto))

expected_proto_str = """text: "Barack Obama was born on Hawaii and he is the president of the United States.\\nHis stepfather is Lolo Soetoro.\\nAfter his second term, Barack will not be president again.\\nBarack married Michelle Obama.\\n"
sentences {
  text: "Barack Obama was born on Hawaii and he is the president of the United States."
  tokens {
    start_offset: 0
    end_offset: 6
    lemma: "Barack"
    pos: "NNP"
    ner: "PERSON"
    id: 1
    word: "Barack"
  }
  tokens {
    start_offset: 7
    end_offset: 12
    lemma: "Obama"
    pos: "NNP"
    ner: "PERSON"
    id: 2
    word: "Obama"
  }
  tokens {
    start_offset: 13
    end_offset: 16
    lemma: "be"
    pos: "VBD"
    ner: "O"
    id: 3
    word: "was"
  }
  tokens {
    start_offset: 17
    end_offset: 21
    lemma: "bear"
    pos: "VBN"
    ner: "O"
    id: 4
    word: "born"
  }
  tokens {
    start_offset: 22
    end_offset: 24
    lemma: "on"
    pos: "IN"
    ner: "O"
    id: 5
    word: "on"
  }
  tokens {
    start_offset: 25
    end_offset: 31
    lemma: "Hawaii"
    pos: "NNP"
    ner: "LOCATION"
    id: 6
    word: "Hawaii"
  }
  tokens {
    start_offset: 32
    end_offset: 35
    lemma: "and"
    pos: "CC"
    ner: "O"
    id: 7
    word: "and"
  }
  tokens {
    start_offset: 36
    end_offset: 38
    lemma: "he"
    pos: "PRP"
    ner: "O"
    id: 8
    word: "he"
  }
  tokens {
    start_offset: 39
    end_offset: 41
    lemma: "be"
    pos: "VBZ"
    ner: "O"
    id: 9
    word: "is"
  }
  tokens {
    start_offset: 42
    end_offset: 45
    lemma: "the"
    pos: "DT"
    ner: "O"
    id: 10
    word: "the"
  }
  tokens {
    start_offset: 46
    end_offset: 55
    lemma: "president"
    pos: "NN"
    ner: "O"
    id: 11
    word: "president"
  }
  tokens {
    start_offset: 56
    end_offset: 58
    lemma: "of"
    pos: "IN"
    ner: "O"
    id: 12
    word: "of"
  }
  tokens {
    start_offset: 59
    end_offset: 62
    lemma: "the"
    pos: "DT"
    ner: "O"
    id: 13
    word: "the"
  }
  tokens {
    start_offset: 63
    end_offset: 69
    lemma: "United"
    pos: "NNP"
    ner: "LOCATION"
    id: 14
    word: "United"
  }
  tokens {
    start_offset: 70
    end_offset: 76
    lemma: "States"
    pos: "NNPS"
    ner: "LOCATION"
    id: 15
    word: "States"
  }
  tokens {
    start_offset: 76
    end_offset: 77
    lemma: "."
    pos: "."
    ner: "O"
    id: 16
    word: "."
  }
  id: 1
}
sentences {
  text: "His stepfather is Lolo Soetoro."
  tokens {
    start_offset: 78
    end_offset: 81
    lemma: "he"
    pos: "PRP$"
    ner: "O"
    id: 1
    word: "His"
  }
  tokens {
    start_offset: 82
    end_offset: 92
    lemma: "stepfather"
    pos: "NN"
    ner: "O"
    id: 2
    word: "stepfather"
  }
  tokens {
    start_offset: 93
    end_offset: 95
    lemma: "be"
    pos: "VBZ"
    ner: "O"
    id: 3
    word: "is"
  }
  tokens {
    start_offset: 96
    end_offset: 100
    lemma: "Lolo"
    pos: "NNP"
    ner: "PERSON"
    id: 4
    word: "Lolo"
  }
  tokens {
    start_offset: 101
    end_offset: 108
    lemma: "Soetoro"
    pos: "NNP"
    ner: "PERSON"
    id: 5
    word: "Soetoro"
  }
  tokens {
    start_offset: 108
    end_offset: 109
    lemma: "."
    pos: "."
    ner: "O"
    id: 6
    word: "."
  }
  id: 2
}
sentences {
  text: "After his second term, Barack will not be president again."
  tokens {
    start_offset: 110
    end_offset: 115
    lemma: "after"
    pos: "IN"
    ner: "O"
    id: 1
    word: "After"
  }
  tokens {
    start_offset: 116
    end_offset: 119
    lemma: "he"
    pos: "PRP$"
    ner: "O"
    id: 2
    word: "his"
  }
  tokens {
    start_offset: 120
    end_offset: 126
    lemma: "second"
    pos: "JJ"
    ner: "ORDINAL"
    id: 3
    word: "second"
  }
  tokens {
    start_offset: 127
    end_offset: 131
    lemma: "term"
    pos: "NN"
    ner: "O"
    id: 4
    word: "term"
  }
  tokens {
    start_offset: 131
    end_offset: 132
    lemma: ","
    pos: ","
    ner: "O"
    id: 5
    word: ","
  }
  tokens {
    start_offset: 133
    end_offset: 139
    lemma: "Barack"
    pos: "NNP"
    ner: "PERSON"
    id: 6
    word: "Barack"
  }
  tokens {
    start_offset: 140
    end_offset: 144
    lemma: "will"
    pos: "MD"
    ner: "O"
    id: 7
    word: "will"
  }
  tokens {
    start_offset: 145
    end_offset: 148
    lemma: "not"
    pos: "RB"
    ner: "O"
    id: 8
    word: "not"
  }
  tokens {
    start_offset: 149
    end_offset: 151
    lemma: "be"
    pos: "VB"
    ner: "O"
    id: 9
    word: "be"
  }
  tokens {
    start_offset: 152
    end_offset: 161
    lemma: "president"
    pos: "NN"
    ner: "O"
    id: 10
    word: "president"
  }
  tokens {
    start_offset: 162
    end_offset: 167
    lemma: "again"
    pos: "RB"
    ner: "O"
    id: 11
    word: "again"
  }
  tokens {
    start_offset: 167
    end_offset: 168
    lemma: "."
    pos: "."
    ner: "O"
    id: 12
    word: "."
  }
  id: 3
}
sentences {
  text: "Barack married Michelle Obama."
  tokens {
    start_offset: 169
    end_offset: 175
    lemma: "Barack"
    pos: "NNP"
    ner: "PERSON"
    id: 1
    word: "Barack"
  }
  tokens {
    start_offset: 176
    end_offset: 183
    lemma: "marry"
    pos: "VBD"
    ner: "O"
    id: 2
    word: "married"
  }
  tokens {
    start_offset: 184
    end_offset: 192
    lemma: "Michelle"
    pos: "NNP"
    ner: "PERSON"
    id: 3
    word: "Michelle"
  }
  tokens {
    start_offset: 193
    end_offset: 198
    lemma: "Obama"
    pos: "NNP"
    ner: "PERSON"
    id: 4
    word: "Obama"
  }
  tokens {
    start_offset: 198
    end_offset: 199
    lemma: "."
    pos: "."
    ner: "O"
    id: 5
    word: "."
  }
  id: 4
}
coreferences {
  mentions {
    sentence_id: 1
    start_word_id: 1
    end_word_id: 3
    text: "Barack Obama"
  }
  mentions {
    sentence_id: 1
    start_word_id: 8
    end_word_id: 9
    text: "he"
  }
  mentions {
    sentence_id: 1
    start_word_id: 10
    end_word_id: 16
    text: "the president of the United States"
  }
  mentions {
    sentence_id: 2
    start_word_id: 1
    end_word_id: 2
    text: "His"
  }
  mentions {
    sentence_id: 3
    start_word_id: 6
    end_word_id: 7
    text: "Barack"
  }
  mentions {
    sentence_id: 4
    start_word_id: 1
    end_word_id: 2
    text: "Barack"
  }
  wikidata_entity_id: "Q76"
}
coreferences {
  mentions {
    sentence_id: 2
    start_word_id: 4
    end_word_id: 6
    text: "Lolo Soetoro"
  }
  mentions {
    sentence_id: 2
    start_word_id: 1
    end_word_id: 3
    text: "His stepfather"
  }
  mentions {
    sentence_id: 3
    start_word_id: 2
    end_word_id: 3
    text: "his"
  }
  wikidata_entity_id: "Q4115068"
}
coreferences {
  mentions {
    sentence_id: 1
    start_word_id: 6
    end_word_id: 7
    text: "Hawaii"
  }
  wikidata_entity_id: "Q782"
}
coreferences {
  mentions {
    sentence_id: 1
    start_word_id: 14
    end_word_id: 16
    text: "United States"
  }
  wikidata_entity_id: "Q30"
}
coreferences {
  mentions {
    sentence_id: 4
    start_word_id: 3
    end_word_id: 5
    text: "Michelle Obama"
  }
  wikidata_entity_id: "Q13133"
}
"""

assert str(document_proto) == expected_proto_str
