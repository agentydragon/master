import org.json.*;
import org.apache.log4j.Logger;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.parsers.ParserConfigurationException;
import java.util.List;
import org.xml.sax.SAXException;
import java.io.IOException;

public class GenerateTrainingSamples {
	static Logger log = Logger.getLogger(GetTrainingSamples.class);

	private WikidataClient wikidataClient;

	public void setWikidataClient(WikidataClient wikidataClient) {
		this.wikidataClient = wikidataClient;
	}

	public List<TrainingSamples.TrainingSample> makeTrainingSamples(String value) throws IOException {
		JSONObject inputJson = new JSONObject(value);

		String plaintext = (String) inputJson.get("plaintext");
		String corenlpXml = (String) inputJson.get("corenlp_xml");

		Sentence.Document documentProto = null;
		try {
			org.w3c.dom.Document corenlpParse = ParseXmlsToProtos.parseXmlFromString(corenlpXml);
			documentProto = ParseXmlsToProtos.documentToProto(corenlpParse, plaintext);
		} catch (ParserConfigurationException e) {
			// TODO
			System.exit(1);
		} catch (SAXException e) {
			// TODO
			System.exit(1);
		} catch (XPathExpressionException e) {
			// TODO
			System.exit(1);
		}
		// log.info(documentProto.toString());

		JSONObject spotlightJson = new JSONObject((String) inputJson.get("spotlight_json"));
		List<Sentence.SpotlightMention> spotlightMentions = AnnotateCoreferences.SpotlightToMentions(spotlightJson);
		documentProto = AnnotateCoreferences.PropagateEntities(documentProto, spotlightMentions);
		// log.info(documentProto.toString());

		GetTrainingSamples getTrainingSamples = new GetTrainingSamples(wikidataClient);
		return getTrainingSamples.documentToSamples(documentProto);
	}
}
