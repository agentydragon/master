// Input: from DocumentProcessorMapper
// Output: Relation => Sentence expressing the relation

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.json.*;

public class GenerateTrainingSamplesMapper extends Mapper<Text, Text, Text, Text> {
	@Override
	public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
		String articleTitle = key.toString();
		JSONObject inputJson = new JSONObject(value.toString());

		String plaintext = (String) inputJson.get("text")
		String corenlpXml = (String) inputJson.get("corenlp_xml");

		var corenlpParse = TODO parse;

		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		DocumentBuilder db = dbf.newDocumentBuilder();
		org.w3c.dom.Document corenlpParse = db.parse(new InputSource(new StringReader(corenlpXml)));
		Sentence.Document documentProto = ParseXmlsToProtos.documentToProto(corenlpParse, plaintext);
		JSONObject spotlightJson = new JSONObject((String) inputJson.get("spotlight_json"));
		List<AnnotateCoreferences.SpotlightMention> spotlightMentions = AnnotateCoreferences.SpotlightToMentions(spotlightJson);
		documentProto = AnnotateCoreferences.PropagateEntities(documentProto, spotlightMentions);
		var sentences = GetTrainingSamples.loadDocument(documentProto);
		var documentTrainingData = GetTrainingSamples.joinSentencesEntities(sentences);

		for relation, samples in documentTrainingData.trainingData.items():
			for sample in samples:
				sample_json = json.dumps({"sample": text_format.MessageToString(sample)})
				context.write(relation, sample_json)
	}
}
