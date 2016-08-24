// Input:
//   Key: article title (Text)
//   Value: JSON from DocumentProcessorMapper (Text)
// Output:
//   Key: Wikidata relation ID (Text)
//   Value: TrainingSample proto (BytesWritable)
//
// Finds sentences that are positive samples for some relation.

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;

public class SentenceSampleExtractorMapper extends Mapper<Text, Text, Text, BytesWritable> {
	@Override
	public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
		String articleTitle = key.toString();

		JSONObject json = new JSONObject(value.toString());
		String corenlpXml = json.getString("corenlp_xml");
		JSONObject spotlightJson = new JSONObject(json.getString("spotlight_json"));
		String articleText = json.getString("text");

		// for every sentence:
		//   for every pair of entities mentioned in the sentence:
		//     if this pair of entities has a link:
		//       emit the sentence as a sample for that relation

		InputStream xmlStream = new ByteArrayInputStream(corenlpXml.getBytes(StandardCharsets.UTF_8));
		var dbFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder documentBuilder = dbFactory.newDocumentBuilder();
		Document doc = documentBuilder.parse(xmlStream);

		XPathFactory xPathFactory = XPathFactory.newInstance();
		XPath xPath = xPathFactory.newXPath();
		NodeList sentenceNodes = xPath.evaluate("/sentences/sentence", doc.getDocumentElement(), XPathConstants.NODESET);
		for (int i = 0; i < sentenceNodes.getLength(); i++) {
			Element e = (Element) sentenceNodes.item(i);
			// TODO process sentence

			TODO
		}
	}
}
