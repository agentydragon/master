import java.lang.System;
import java.util.List;
import org.junit.Test;
import org.apache.log4j.BasicConfigurator;

public class GenerateTrainingSamplesMapperTest {
	@Test
	public void testSampleFile() throws Exception {
		BasicConfigurator.configure();
//		GetTrainingSamples.setLevel(Level.INFO);

		//DocumentProcessorMapper dpm = new DocumentProcessorMapper();
		//dpm.setSpotlightServer("http://spotlight.sztaki.hu:2222/rest/annotate");
		//dpm.setNLPPipeline();

		//String text = "Barack Obama is the president of the United States. " +
		//		"His wife is named Michelle Obama. " +
		//		"Barack was born on Hawaii.";
		//String json = dpm.articleToJson("Barack Obama", text);

		GenerateTrainingSamplesMapper gsm = new GenerateTrainingSamplesMapper();
		WikidataClient client = WikidataClient.newPublicEndpointClient();
		gsm.setWikidataClient(client);

//		String json = ParseXmlsToProtos.readFile("testdata/tharde.json");
		String json = ParseXmlsToProtos.readFile("testdata/obama-short.json");
		List<TrainingSamples.TrainingSample> samples = gsm.makeTrainingSamples(json);
		for (TrainingSamples.TrainingSample sample : samples) {
			System.out.println(sample.toString());
		}
	}
}
