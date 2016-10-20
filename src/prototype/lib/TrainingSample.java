import org.json.*;
import java.util.*;
import java.util.stream.*;
import java.util.function.*;
import java.io.*;

public class TrainingSample {
	public String relation;
	public boolean positive;
	public TrainingSampleParsedSentence sentence;
	public String subject;
	public String object;
	public List<Integer> subjectTokenIndices;
	public List<Integer> objectTokenIndices;

	private static String RELATION = "relation";
	private static String POSITIVE = "positive";
	private static String SENTENCE = "sentence";
	private static String SUBJECT = "subject";
	private static String OBJECT = "object";
	private static String SUBJECT_TOKEN_INDICES = "subject_token_indices";
	private static String OBJECT_TOKEN_INDICES = "object_token_indices";

	public JSONObject toJSON() {
		return new JSONObject()
			.put(RELATION, relation)
			.put(POSITIVE, positive)
			.put(SENTENCE, sentence.toJSON())
			.put(SUBJECT, subject)
			.put(OBJECT, object)
			.put(SUBJECT_TOKEN_INDICES, JSONUtils.toIntArray(subjectTokenIndices))
			.put(OBJECT_TOKEN_INDICES, JSONUtils.toIntArray(objectTokenIndices));
	}

	public static TrainingSample fromJSON(JSONObject o) {
		TrainingSample sample = new TrainingSample();
		sample.relation = (String) o.get(RELATION);
		sample.positive = o.getBoolean(POSITIVE);
		sample.sentence = TrainingSampleParsedSentence.fromJSON((JSONObject) o.get(SENTENCE));
		sample.subject = (String) o.get(SUBJECT);
		sample.object = (String) o.get(OBJECT);
		sample.subjectTokenIndices = JSONUtils.arrayToIntList((JSONArray) o.get(SUBJECT_TOKEN_INDICES));
		sample.objectTokenIndices = JSONUtils.arrayToIntList((JSONArray) o.get(OBJECT_TOKEN_INDICES));
		return sample;
	}

	public static class TrainingSampleParsedSentence {
		public String text;
		public List<TrainingSampleSentenceToken> tokens;
		public String originArticle;
		public int originSentenceId;

		private static String TEXT = "text";
		private static String TOKENS = "tokens";
		private static String ORIGIN_ARTICLE = "origin_article";
		private static String ORIGIN_SENTENCE_ID = "origin_sentence_id";

		public JSONObject toJSON() {
			return new JSONObject()
				.put(TEXT, text)
				.put(TOKENS, JSONUtils.toArray(tokens, TrainingSampleSentenceToken::toJSON))
				.put(ORIGIN_ARTICLE, originArticle)
				.put(ORIGIN_SENTENCE_ID, originSentenceId);
		}

		public static TrainingSampleParsedSentence fromJSON(JSONObject o) {
			TrainingSampleParsedSentence s = new TrainingSampleParsedSentence();
			s.text = (String) o.get(TEXT);
			s.tokens = JSONUtils.arrayMap((JSONArray) o.get(TOKENS), TrainingSampleSentenceToken::fromJSON);
			s.originArticle = (String) o.get(ORIGIN_ARTICLE);
			s.originSentenceId = o.getInt(ORIGIN_SENTENCE_ID);
			return s;
		}
	}

	public static class TrainingSampleSentenceToken {
		public int startOffset;
		public int endOffset;
		public String lemma;
		public String pos;
		public String ner;

		private static String START_OFFSET = "start_offset";
		private static String END_OFFSET = "end_offset";
		private static String LEMMA = "lemma";
		private static String POS = "pos";
		private static String NER = "ner";

		public JSONObject toJSON() {
			return new JSONObject()
				.put(START_OFFSET, startOffset)
				.put(END_OFFSET, endOffset)
				.put(LEMMA, lemma)
				.put(POS, pos)
				.put(NER, ner);
		}

		public static TrainingSampleSentenceToken fromJSON(JSONObject o) {
			TrainingSampleSentenceToken t = new TrainingSampleSentenceToken();
			t.startOffset = o.getInt(START_OFFSET);
			t.endOffset = o.getInt(END_OFFSET);
			t.lemma = (String) o.get(LEMMA);
			t.pos = (String) o.get(POS);
			t.ner = (String) o.get(NER);
			return t;
		}
	}
}
