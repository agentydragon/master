import org.json.*;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Result;
import java.util.*;
import java.util.stream.*;
import java.util.function.*;

public class SavedDocument {
	public static class JSONUtils {
		public static <T> List<T> arrayMap(JSONArray array, Function<JSONObject, T> convert) {
			List<T> r = new ArrayList<>();
			for (int i = 0; i < array.length(); i++) {
				r.add(convert.apply((JSONObject) array.get(i)));
			}
			return r;
		}

		public static <T> JSONArray toArray(List<T> array, Function<T, JSONObject> convert) {
			return new JSONArray(array.stream().map(convert).collect(Collectors.toList()));
		}
	}

	public static class SentenceToken {
		public int id;
		public int startOffset;
		public int endOffset;
		public String lemma;
		public String pos;
		public String word;
		public String ner;

		private static String ID = "id";
		private static String START_OFFSET = "start_offset";
		private static String END_OFFSET = "end_offset";
		private static String LEMMA = "lemma";
		private static String POS = "pos";
		private static String WORD = "word";
		private static String NER = "ner";

		public JSONObject toJSON() {
			return new JSONObject()
				.put(ID, id)
				.put(START_OFFSET, startOffset)
				.put(END_OFFSET, endOffset)
				.put(LEMMA, lemma)
				.put(POS, pos)
				.put(WORD, word)
				.put(NER, ner);
		}

		public static SentenceToken fromJSON(JSONObject o) {
			SentenceToken token = new SentenceToken();
			token.id = o.getInt(ID);
			token.startOffset = o.getInt(START_OFFSET);
			token.endOffset = o.getInt(END_OFFSET);
			token.lemma = (String) o.get(LEMMA);
			token.pos = (String) o.get(POS);
			token.word = (String) o.get(WORD);
			token.ner = (String) o.get(NER);
			return token;
		}
	}

	public static class Mention {
		public int sentenceId;
		public int startWordId;
		public int endWordId;
		public String text;

		private static String SENTENCE_ID = "sentence_id";
		private static String START_WORD_ID = "start_word_id";
		private static String END_WORD_ID = "end_word_id";
		private static String TEXT = "text";

		public JSONObject toJSON() {
			return new JSONObject()
				.put(SENTENCE_ID, sentenceId)
				.put(START_WORD_ID, startWordId)
				.put(END_WORD_ID, endWordId)
				.put(TEXT, text);
		}

		public static Mention fromJSON(JSONObject o) {
			Mention m = new Mention();
			m.sentenceId = o.getInt(SENTENCE_ID);
			m.startWordId = o.getInt(START_WORD_ID);
			m.endWordId = o.getInt(END_WORD_ID);
			m.text = (String) o.get(TEXT);
			return m;
		}
	}

	public static class Coreference {
		public List<Mention> mentions;

		private static String MENTIONS = "mentions";

		public JSONObject toJSON() {
			return new JSONObject()
				.put(MENTIONS, JSONUtils.toArray(mentions, Mention::toJSON));
		}

		public static Coreference fromJSON(JSONObject o) {
			Coreference coreference = new Coreference();
			coreference.mentions = JSONUtils.arrayMap((JSONArray) o.get(MENTIONS), Mention::fromJSON);
			return coreference;
		}
	}

	public static class SpotlightMention {
		public int startOffset;
		public int endOffset;
		public String surfaceForm;
		public String uri;
		public String wikidataId;

		private static String START_OFFSET = "start_offset";
		private static String END_OFFSET = "end_offset";
		private static String SURFACE_FORM = "surface_form";
		private static String URI = "uri";
		private static String WIKIDATA_ID = "wikidata_id";

		public JSONObject toJSON() {
			return new JSONObject()
				.put(START_OFFSET, startOffset)
				.put(END_OFFSET, endOffset)
				.put(SURFACE_FORM, surfaceForm)
				.put(URI, uri)
				.put(WIKIDATA_ID, wikidataId);
		}

		public static SpotlightMention fromJSON(JSONObject o) {
			SpotlightMention m = new SpotlightMention();
			m.startOffset = o.getInt(START_OFFSET);
			m.endOffset = o.getInt(END_OFFSET);
			m.surfaceForm = (String) o.get(SURFACE_FORM);
			m.uri = (String) o.get(URI);
			m.wikidataId = (String) o.get(WIKIDATA_ID);
			return m;
		}

		public static List<SpotlightMention> mentionsFromSpotlightJSON(JSONObject spotlightJSON, DBpediaClient dbpediaClient) {
			List<SpotlightMention> mentions = new ArrayList<>();

			// TODO: fix?
			if (!spotlightJSON.has("Resources")) {
				System.out.println("WARN: no resources returned by Spotlight");
				return mentions;
			}

			JSONArray resources = (JSONArray) spotlightJSON.get("Resources");
			Set<String> dbpediaUris = new HashSet<>();
			for (int i = 0; i < resources.length(); i++) {
				dbpediaUris.add((String) ((JSONObject) resources.get(i)).get("@URI"));
			}
			Map<String, String> dbpediaUriToWikidataId = dbpediaClient.dbpediaUrisToWikidataIds(new ArrayList<>(dbpediaUris));

			for (int i = 0; i < resources.length(); i++) {
				JSONObject mention_json = (JSONObject) resources.get(i);
				if (!mention_json.has("@surfaceForm") || mention_json.get("@surfaceForm") == "" || mention_json.get("@surfaceForm") == null) {
					// TODO HACK?
					continue;
				}

				String uri = (String) mention_json.get("@URI");
				String wikidataId;
				if (dbpediaUriToWikidataId.containsKey(uri)) {
					wikidataId = dbpediaUriToWikidataId.get(uri);
				} else {
					System.out.println("WARN: No translation: " + uri);
					wikidataId = null;
				}

				SpotlightMention m = new SpotlightMention();
				m.startOffset = mention_json.getInt("@offset");
				m.uri = uri;
				m.wikidataId = wikidataId;

				String surfaceForm = (String) mention_json.get("@surfaceForm");
				m.endOffset = m.startOffset + surfaceForm.length();
				m.surfaceForm = surfaceForm;
				mentions.add(m);
			}

			return mentions;
		}
	}

	public static class DocumentSentence {
		public int id;
		public String text;
		public List<SentenceToken> tokens;

		private static String ID = "id";
		private static String TEXT = "text";
		private static String TOKENS = "tokens";

		public JSONObject toJSON() {
			return new JSONObject()
				.put(ID, id)
				.put(TEXT, text)
				.put(TOKENS, JSONUtils.toArray(tokens, SentenceToken::toJSON));
		}

		public static DocumentSentence fromJSON(JSONObject o) {
			DocumentSentence s = new DocumentSentence();
			s.id = o.getInt(ID);
			s.text = (String) o.get(TEXT);
			s.tokens = JSONUtils.arrayMap((JSONArray) o.get(TOKENS), SentenceToken::fromJSON);
			return s;
		}
	}

	public String title = null;
	public String plaintext = null;
	public String corenlpXml = null;
	public JSONObject spotlightJson = null;

	// Generated by add_join.
	private List<DocumentSentence> sentences = null;
	private List<Coreference> coreferences = null;
	private List<SpotlightMention> spotlightMentions = null;

	public static Get getGet(String title) {
		Get get = new Get(Bytes.toBytes(title));
		get.addColumn(ArticlesTable.WIKI, ArticlesTable.PLAINTEXT);
		get.addColumn(ArticlesTable.WIKI, ArticlesTable.CORENLP_XML);
		get.addColumn(ArticlesTable.WIKI, ArticlesTable.SPOTLIGHT_JSON);
		// TODO: sentences, coreferences, spotlight mentions
		return get;
	}

	public SavedDocument(Result result) {
//		if (result.getRow() == null) {
//			throw new InvalidArgumentException("Null rowkey");
//		}

		title = new String(result.getRow());

		byte[] plaintextBytes = result.getValue(ArticlesTable.WIKI, ArticlesTable.PLAINTEXT);
		if (plaintextBytes != null) {
			plaintext = new String(plaintextBytes);
		}

		byte[] corenlpXmlBytes = result.getValue(ArticlesTable.WIKI, ArticlesTable.CORENLP_XML);
		if (corenlpXmlBytes != null) {
			corenlpXml = new String(corenlpXmlBytes);
		}

		byte[] spotlightJsonBytes = result.getValue(ArticlesTable.WIKI, ArticlesTable.SPOTLIGHT_JSON);
		if (spotlightJsonBytes != null) {
			spotlightJson = new JSONObject(new String(spotlightJsonBytes));
		}

		byte[] sentencesJsonBytes = result.getValue(ArticlesTable.WIKI, ArticlesTable.SENTENCES);
		if (sentencesJsonBytes != null) {
			sentences = JSONUtils.arrayMap(new JSONArray(new String(sentencesJsonBytes)), DocumentSentence::fromJSON);
		}

		byte[] coreferencesJSONBytes = result.getValue(ArticlesTable.WIKI, ArticlesTable.COREFERENCES);
		if (coreferencesJSONBytes != null) {
			coreferences = JSONUtils.arrayMap(new JSONArray(new String(coreferencesJSONBytes)), Coreference::fromJSON);
		}

		byte[] spotlightMentionsJSONBytes = result.getValue(ArticlesTable.WIKI, ArticlesTable.SPOTLIGHT_MENTIONS);
		if (spotlightMentionsJSONBytes != null) {
			spotlightMentions = JSONUtils.arrayMap(new JSONArray(new String(spotlightMentionsJSONBytes)), SpotlightMention::fromJSON);
		}
	}

	public JSONObject toJSON() {
		JSONObject json = new JSONObject();
		json.put("title", title);
		if (plaintext != null) {
			json.put("plaintext", plaintext);
		}
		if (corenlpXml != null) {
			json.put("corenlp_xml", corenlpXml);
		}
		if (spotlightJson != null) {
			json.put("spotlight_json", spotlightJson);
		}
		if (sentences != null) {
			json.put("sentences", JSONUtils.toArray(sentences, DocumentSentence::toJSON));
		}
		if (coreferences != null) {
			json.put("coreferences", JSONUtils.toArray(coreferences, Coreference::toJSON));
		}
		if (spotlightMentions != null) {
			json.put("spotlight_mentions", JSONUtils.toArray(spotlightMentions, SpotlightMention::toJSON));
		}
		return json;
	}

	/*
	public void addProtoToDocument(DBpediaClient dbpediaClient) {
		TODO
	}
	*/

	public byte[] getSentencesSerialization() {
		return Bytes.toBytes(JSONUtils.toArray(sentences, DocumentSentence::toJSON).toString());
	}

	public byte[] getCoreferencesSerialization() {
		return Bytes.toBytes(JSONUtils.toArray(coreferences, Coreference::toJSON).toString());
	}

	public byte[] getSpotlightMentionsSerialization() {
		return Bytes.toBytes(JSONUtils.toArray(spotlightMentions, SpotlightMention::toJSON).toString());
	}
}
