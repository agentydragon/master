import org.json.*;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Result;
import java.util.*;
import java.util.stream.*;
import java.util.function.*;
import java.io.*;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.ParserConfigurationException;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.w3c.dom.*;
import javax.xml.xpath.*;

public class SavedDocument {
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
			if (o.has(WIKIDATA_ID)) {
				m.wikidataId = (String) o.get(WIKIDATA_ID);
			}
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
				JSONObject mention_json = (JSONObject) resources.get(i);
				dbpediaUris.add((String) mention_json.get("@URI"));
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
	public List<DocumentSentence> sentences = null;
	public List<Coreference> coreferences = null;
	public List<SpotlightMention> spotlightMentions = null;

	public static Get getGet(String title) {
		Get get = new Get(Bytes.toBytes(title));
		get.addColumn(ArticlesTable.WIKI, ArticlesTable.PLAINTEXT);
		get.addColumn(ArticlesTable.WIKI, ArticlesTable.CORENLP_XML);
		get.addColumn(ArticlesTable.WIKI, ArticlesTable.SPOTLIGHT_JSON);
		get.addColumn(ArticlesTable.WIKI, ArticlesTable.SENTENCES);
		get.addColumn(ArticlesTable.WIKI, ArticlesTable.COREFERENCES);
		get.addColumn(ArticlesTable.WIKI, ArticlesTable.SPOTLIGHT_MENTIONS);
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

	private static XPathFactory xPathFactory = XPathFactory.newInstance();
	private static XPath xPath = xPathFactory.newXPath();

	private static org.w3c.dom.Document parseXmlFromString(String str) throws SAXException, ParserConfigurationException, IOException {
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		DocumentBuilder db = dbf.newDocumentBuilder();
		return db.parse(new InputSource(new StringReader(str)));
	}

	private static Map<String, XPathExpression> tagContentXpaths = new HashMap<>();

	private static int getAttributeAsInt(Node tag, String attribute) {
		return Integer.parseInt(tag.getAttributes().getNamedItem(attribute).getNodeValue());
	}

	private static NodeList queryXPathNodes(String xPathstr, Object tag) throws XPathExpressionException {
		if (!tagContentXpaths.containsKey(xPathstr)) {
			tagContentXpaths.put(xPathstr, xPath.compile(xPathstr));
		}
		XPathExpression e2 = tagContentXpaths.get(xPathstr);
		return (NodeList) e2.evaluate(tag, XPathConstants.NODESET);
	}

	// TODO: handle those as literals!

	private static Map<String, String> getTagTexts(Node node) {
		Map<String, String> result = new HashMap<>();
		NodeList children = node.getChildNodes();
		for (int k = 0; k < children.getLength(); k++) {
			Node child = children.item(k);
			result.put(child.getNodeName(), child.getTextContent());
		}
		return result;
	}

	public void addProtoToDocument(DBpediaClient dbpediaClient) throws XPathExpressionException, SAXException, ParserConfigurationException, IOException {
		spotlightMentions = SpotlightMention.mentionsFromSpotlightJSON(spotlightJson, dbpediaClient);

		org.w3c.dom.Document root = parseXmlFromString(corenlpXml);

		sentences = new ArrayList<>();
		NodeList nodes = queryXPathNodes("/root/document/sentences/sentence", root);
		for (int i = 0; i < nodes.getLength(); i++) {
			Node sentenceTag = nodes.item(i);

			DocumentSentence sentence = new DocumentSentence();
			sentence.id = getAttributeAsInt(sentenceTag, "id");
			sentence.tokens = new ArrayList<>();

			int sentenceBegin = -1;
			int sentenceEnd = -1;

			NodeList tokens = queryXPathNodes("tokens/token", sentenceTag);
			for (int j = 0; j < tokens.getLength(); j++) {
				Node tokenTag = tokens.item(j);

				Map<String, String> texts = getTagTexts(tokenTag);

				int tokenStart = Integer.parseInt(texts.get("CharacterOffsetBegin"));
				int tokenEnd = Integer.parseInt(texts.get("CharacterOffsetEnd"));

				sentenceEnd = tokenEnd;
				if (sentenceBegin == -1) {
					sentenceBegin = tokenStart;
				}

				SentenceToken token = new SentenceToken();
				token.id = getAttributeAsInt(tokenTag, "id");
				token.startOffset = tokenStart;
				token.endOffset = tokenEnd;
				token.lemma = texts.get("lemma");
				token.word = texts.get("word");
				token.pos = texts.get("POS");
				token.ner = texts.get("NER");
				sentence.tokens.add(token);
			}

			sentence.text = plaintext.substring(sentenceBegin, sentenceEnd);
			sentences.add(sentence);
		}

		coreferences = new ArrayList<>();
		nodes = queryXPathNodes("/root/document/coreference/coreference", root);
		for (int i = 0; i < nodes.getLength(); i++) {
			Node corefNode = nodes.item(i);
			Coreference coreference = new Coreference();
			coreference.mentions = new ArrayList<>();

			NodeList mentionTags = queryXPathNodes("mention", corefNode);
			for (int j = 0; j < mentionTags.getLength(); j++) {
				Node mentionNode = mentionTags.item(j);

				Map<String, String> texts = getTagTexts(mentionNode);

				Mention mention = new Mention();
				mention.startWordId = Integer.parseInt(texts.get("start"));
				mention.endWordId = Integer.parseInt(texts.get("end"));
				mention.sentenceId = Integer.parseInt(texts.get("sentence"));
				mention.text = texts.get("text");
				coreference.mentions.add(mention);
			}
			coreferences.add(coreference);
		}
	}

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
