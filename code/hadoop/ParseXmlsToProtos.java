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

public class ParseXmlsToProtos {
	private static XPathFactory xPathFactory = XPathFactory.newInstance();

	public static String readFile(String path) throws IOException, UnsupportedEncodingException {
		return new String(Files.readAllBytes(Paths.get(path)), "UTF-8");
	}

	public static org.w3c.dom.Document parseXmlFromString(String str) throws SAXException, ParserConfigurationException, IOException {
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		DocumentBuilder db = dbf.newDocumentBuilder();
		return db.parse(new InputSource(new StringReader(str)));
	}

	private static String findTagContent(Node parent, String tag) throws XPathExpressionException {
		XPath xPath = xPathFactory.newXPath();
		XPathExpression expr = xPath.compile("string(" + tag + ")");
		return expr.evaluate(parent);
	}

	private static int findTagContentAsInt(Node parent, String tag) throws XPathExpressionException {
		return Integer.parseInt(findTagContent(parent, tag));
	}

	private static int getAttributeAsInt(Node tag, String attribute) {
		return Integer.parseInt(tag.getAttributes().getNamedItem(attribute).getNodeValue());
	}

	private static NodeList queryXPathNodes(String xPathstr, Object tag) throws XPathExpressionException {
		XPath xPath = xPathFactory.newXPath();
		XPathExpression e2 = xPath.compile(xPathstr);
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
		Sentence.Coreference.Builder corefBuilder = Sentence.Coreference.newBuilder();
		Sentence.Mention.Builder mentionBuilder = Sentence.Mention.newBuilder()
			.setSentenceId(sentenceId)
			.setStartWordId(startToken.getId())
			.setEndWordId(endToken.getId() + 1)
			.setText(mentionText);
		corefBuilder.addMentions(mentionBuilder);
		document.addCoreferences(corefBuilder);
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

	public static Sentence.Document documentToProto(org.w3c.dom.Document root, String plaintext) throws XPathExpressionException {
		Sentence.Document.Builder builder = Sentence.Document.newBuilder()
			.setText(plaintext);
		// TODO: set title

		NodeList nodes = queryXPathNodes("/root/document/sentences/sentence", root);
		for (int i = 0; i < nodes.getLength(); i++) {
			Node sentenceTag = nodes.item(i);

			Sentence.DocumentSentence.Builder sentenceBuilder = Sentence.DocumentSentence.newBuilder()
				.setId(getAttributeAsInt(sentenceTag, "id"));

			int sentenceBegin = 0;
			int sentenceEnd = 0;

			NodeList tokens = queryXPathNodes("tokens/token", sentenceTag);
			for (int j = 0; j < tokens.getLength(); j++) {
				Node tokenTag = tokens.item(j);

				int tokenStart = findTagContentAsInt(tokenTag, "CharacterOffsetBegin");
				int tokenEnd = findTagContentAsInt(tokenTag, "CharacterOffsetEnd");

				sentenceEnd = tokenEnd;
				if (sentenceBegin == 0) {
					sentenceBegin = tokenStart;
				}

				Sentence.SentenceToken.Builder tokenBuilder = Sentence.SentenceToken.newBuilder()
					.setId(getAttributeAsInt(tokenTag, "id"))
					.setStartOffset(tokenStart)
					.setEndOffset(tokenEnd)
					.setLemma(findTagContent(tokenTag, "lemma"))
					.setWord(findTagContent(tokenTag, "word"))
					.setPos(findTagContent(tokenTag, "POS"))
					.setNer(findTagContent(tokenTag, "NER"));

				sentenceBuilder.addTokens(tokenBuilder);
			}

			System.out.println("Sentence: [" + sentenceBegin + ";" + sentenceEnd + "]");
			sentenceBuilder.setText(plaintext.substring(sentenceBegin, sentenceEnd));

			builder.addSentences(sentenceBuilder);
		}

		nodes = queryXPathNodes("/root/document/coreference/coreference", root);
		for (int i = 0; i < nodes.getLength(); i++) {
			Node corefNode = nodes.item(i);
			Sentence.Coreference.Builder corefBuilder = Sentence.Coreference.newBuilder();

			NodeList mentionTags = queryXPathNodes("mention", corefNode);
			for (int j = 0; j < mentionTags.getLength(); j++) {
				Node mentionNode = mentionTags.item(j);

				Sentence.Mention.Builder mentionBuilder = Sentence.Mention.newBuilder()
					.setStartWordId(findTagContentAsInt(mentionNode, "start"))
					.setEndWordId(findTagContentAsInt(mentionNode, "end"))
					.setSentenceId(findTagContentAsInt(mentionNode, "sentence"))
					.setText(findTagContent(mentionNode, "text"));
				corefBuilder.addMentions(mentionBuilder);
			}
			builder.addCoreferences(corefBuilder);
		}
		addSingleReferencedEntitiesToCoreferences(builder);
		return builder.build();
	}
}
