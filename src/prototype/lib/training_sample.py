from recordclass import recordclass

class TrainingSample(recordclass("TrainingSample",
                                 ["relation", "positive", "subject", "object",
                                  "sentence", "subject_token_indices",
                                  "object_token_indices"])):
    RELATION = 'relation'
    POSITIVE = 'positive'
    SENTENCE = 'sentence'
    SUBJECT = 'subject'
    OBJECT = 'object'
    SUBJECT_TOKEN_INDICES = 'subject_token_indices'
    OBJECT_TOKEN_INDICES = 'object_token_indices'

    def to_json(self):
        assert len(self.subject_token_indices) > 0
        assert len(self.object_token_indices) > 0

        return {
            self.RELATION: self.relation,
            self.POSITIVE: self.positive,
            self.SENTENCE: self.sentence.to_json(),
            self.SUBJECT: self.subject,
            self.OBJECT: self.object,
            self.SUBJECT_TOKEN_INDICES: self.subject_token_indices,
            self.OBJECT_TOKEN_INDICES: self.object_token_indices,
        }

    @classmethod
    def from_json(klass, json):
        self = klass(
            relation=json[klass.RELATION],
            positive=json[klass.POSITIVE],
            sentence=TrainingSampleParsedSentence.from_json(json[klass.SENTENCE]),
            subject=json[klass.SUBJECT],
            object=json[klass.OBJECT],
            subject_token_indices=json[klass.SUBJECT_TOKEN_INDICES],
            object_token_indices=json[klass.OBJECT_TOKEN_INDICES],
        )

        # Check that token indices look alright.
        assert len(self.subject_token_indices) > 0
        for index in self.subject_token_indices:
            if index not in range(len(self.sentence.tokens)):
                raise

        assert len(self.object_token_indices) > 0
        for index in self.object_token_indices:
            if index not in range(len(self.sentence.tokens)):
                raise

        return self

class TrainingSampleParsedSentence(recordclass("TrainingSampleParsedSentence",
                                               ["text", "tokens",
                                               "origin_article",
                                               "origin_sentence_id"])):
    TEXT = 'text'
    TOKENS = 'tokens'
    ORIGIN_ARTICLE = 'origin_article'
    ORIGIN_SENTENCE_ID = 'origin_sentence_id'

    def to_json(self):
        assert self.origin_article is not None

        return {
            self.TEXT: self.text,
            self.TOKENS: [token.to_json() for token in self.tokens],
            self.ORIGIN_ARTICLE: self.origin_article,
            self.ORIGIN_SENTENCE_ID: self.origin_sentence_id
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            text = json[klass.TEXT],
            tokens = list(map(TrainingSampleSentenceToken.from_json,
                              json[klass.TOKENS])),
            origin_article = json[klass.ORIGIN_ARTICLE],
            origin_sentence_id = json[klass.ORIGIN_SENTENCE_ID],
        )

class TrainingSampleSentenceToken(recordclass("TrainingSampleSentenceToken",
                                              ["start_offset", "end_offset",
                                               "lemma", "pos", "ner"])):
    START_OFFSET = 'start_offset'
    END_OFFSET = 'end_offset'
    LEMMA = 'lemma'
    POS = 'pos'
    NER = 'ner'

    def to_json(self):
        return {
            self.START_OFFSET: self.start_offset,
            self.END_OFFSET: self.end_offset,
            self.LEMMA: self.lemma,
            self.POS: self.pos,
            self.NER: self.ner,
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            start_offset = json[klass.START_OFFSET],
            end_offset = json[klass.END_OFFSET],
            lemma = json[klass.LEMMA],
            pos = json[klass.POS],
            ner = json[klass.NER],
        )
