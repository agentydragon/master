from recordclass import recordclass

class TrainingSample(recordclass("TrainingSample",
                                 ["relation", "positive", "subject", "object",
                                  "sentence", "subject_token_indices",
                                  "object_token_indices"])):
    def to_json(self):
        return {
            'relation': self.relation,
            'positive': self.positive,
            'sentence': self.sentence.to_json(),
            'subject': self.subject,
            'object': self.object,
            'subject_token_indices': self.subject_token_indices,
            'object_token_indices': self.object_token_indices,
        }

    @classmethod
    def from_json(klass, json):
        self = klass(
            relation=json['relation'],
            positive=json['positive'],
            sentence=TrainingSampleParsedSentence.from_json(json['sentence']),
            subject=json['subject'],
            object=json['object'],
            subject_token_indices=json['subject_token_indices'],
            object_token_indices=json['object_token_indices'],
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
                                               ["text", "tokens"])):
    def to_json(self):
        return {
            'text': self.text,
            'tokens': [token.to_json() for token in self.tokens]
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            text=json['text'],
            tokens=list(map(TrainingSampleSentenceToken.from_json, json['tokens']))
        )

class TrainingSampleSentenceToken(recordclass("TrainingSampleSentenceToken",
                                              ["start_offset", "end_offset",
                                               "lemma", "pos", "ner"])):
    def to_json(self):
        return {
            'start_offset': self.start_offset,
            'end_offset': self.end_offset,
            'lemma': self.lemma,
            'pos': self.pos,
            'ner': self.ner,
        }

    @classmethod
    def from_json(klass, json):
        return klass(
            start_offset = json['start_offset'],
            end_offset = json['end_offset'],
            lemma = json['lemma'],
            pos = json['pos'],
            ner = json['ner'],
        )
