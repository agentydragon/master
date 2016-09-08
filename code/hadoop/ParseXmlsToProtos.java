import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import javax.xml.parsers.ParserConfigurationException;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.w3c.dom.*;
import java.io.*;
import javax.xml.xpath.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Map;
import java.util.HashMap;

// TODO: This is slow. Why?

public class ParseXmlsToProtos {
	private static XPathFactory xPathFactory = XPathFactory.newInstance();
	private static XPath xPath = xPathFactory.newXPath();

	public static String readFile(String path) throws IOException, UnsupportedEncodingException {
		return new String(Files.readAllBytes(Paths.get(path)), "UTF-8");
	}

	public static org.w3c.dom.Document parseXmlFromString(String str) throws SAXException, ParserConfigurationException, IOException {
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
	private final static List<String> bannedNers = Arrays.asList("O", "ORDINAL", "DATE", "NUMBER", "DURATION");

	private static void flushNamedEntity(Sentence.Document.Builder document, String ner, Sentence.SentenceToken startToken, Sentence.SentenceToken endToken, int sentenceId) {
		if (bannedNers.contains(ner)) {
			return;
		}

		boolean found = false;
		for (Sentence.Coreference coreference : document.getCoreferencesList()) {
			for (Sentence.Mention mention : coreference.getMentionsList()) {
				if (mention.getSentenceId() == sentenceId &&
						mention.getStartWordId() >= startToken.getId() &&
						(mention.getEndWordId() - 1) <= endToken.getId()) {
					found = true;
					break;
				}
			}
		}

		if (found) {
			return;
		}

		String mentionText = document.getText().substring(startToken.getStartOffset(), endToken.getEndOffset());
		document.addCoreferencesBuilder()
			.addMentionsBuilder()
				.setSentenceId(sentenceId)
				.setStartWordId(startToken.getId())
				.setEndWordId(endToken.getId() + 1)
				.setText(mentionText);
	}

	private static void addSingleReferencedEntitiesToCoreferences(Sentence.Document.Builder document) {
		for (Sentence.DocumentSentence sentence : document.getSentencesList()) {
			String lastNer = null;
			List<Sentence.SentenceToken> lastNeTokens = new ArrayList<>();

			for (Sentence.SentenceToken token : sentence.getTokensList()) {
				if (token.getNer().equals(lastNer)) {
					lastNeTokens.add(token);
				} else {
					if (lastNer != null) {
						flushNamedEntity(document, lastNer, lastNeTokens.get(0), lastNeTokens.get(lastNeTokens.size() - 1), sentence.getId());
					}
					lastNer = token.getNer();
					lastNeTokens = new ArrayList<>();
					lastNeTokens.add(token);
				}
			}
			if (lastNer != null) {
				flushNamedEntity(document, lastNer, lastNeTokens.get(0), lastNeTokens.get(lastNeTokens.size() - 1), sentence.getId());
			}
		}
	}

	private static Map<String, String> getTagTexts(Node node) {
		Map<String, String> result = new HashMap<>();
		NodeList children = node.getChildNodes();
		for (int k = 0; k < children.getLength(); k++) {
			Node child = children.item(k);
			result.put(child.getNodeName(), child.getTextContent());
		}
		return result;
	}

	public static Sentence.Document documentToProto(org.w3c.dom.Document root, String plaintext) throws XPathExpressionException {
		Sentence.Document.Builder builder = Sentence.Document.newBuilder()
			.setText(plaintext);
		// TODO: set title

		NodeList nodes = queryXPathNodes("/root/document/sentences/sentence", root);
		for (int i = 0; i < nodes.getLength(); i++) {
			Node sentenceTag = nodes.item(i);

			Sentence.DocumentSentence.Builder sentenceBuilder = builder.addSentencesBuilder()
				.setId(getAttributeAsInt(sentenceTag, "id"));

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

				sentenceBuilder.addTokensBuilder()
					.setId(getAttributeAsInt(tokenTag, "id"))
					.setStartOffset(tokenStart)
					.setEndOffset(tokenEnd)
					.setLemma(texts.get("lemma"))
					.setWord(texts.get("word"))
					.setPos(texts.get("POS"))
					.setNer(texts.get("NER"));
			}

			System.out.println("Sentence: [" + sentenceBegin + ";" + sentenceEnd + "]");
			sentenceBuilder.setText(plaintext.substring(sentenceBegin, sentenceEnd));
		}

		nodes = queryXPathNodes("/root/document/coreference/coreference", root);
		for (int i = 0; i < nodes.getLength(); i++) {
			Node corefNode = nodes.item(i);
			Sentence.Coreference.Builder corefBuilder = builder.addCoreferencesBuilder();

			NodeList mentionTags = queryXPathNodes("mention", corefNode);
			for (int j = 0; j < mentionTags.getLength(); j++) {
				Node mentionNode = mentionTags.item(j);

				Map<String, String> texts = getTagTexts(mentionNode);

				corefBuilder.addMentionsBuilder()
					.setStartWordId(Integer.parseInt(texts.get("start")))
					.setEndWordId(Integer.parseInt(texts.get("end")))
					.setSentenceId(Integer.parseInt(texts.get("sentence")))
					.setText(texts.get("text"));
			}
		}
		addSingleReferencedEntitiesToCoreferences(builder);
		return builder.build();
	}
}
