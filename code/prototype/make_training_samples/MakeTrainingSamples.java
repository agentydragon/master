import java.util.*;
import org.json.*;
import java.io.*;
import java.lang.*;
import org.apache.log4j.BasicConfigurator;

public class MakeTrainingSamples {
	private GenerateTrainingSamples generateTrainingSamples = new GenerateTrainingSamples();

	private void processArticle(String title) {
		try {
			System.out.println(title);

			JSONObject json = ArticleRepository.readArticle(title);
			String str = json.toString();
			List<TrainingSamples.TrainingSample> samples = generateTrainingSamples.makeTrainingSamples(str);

			SampleRepository.writeArticle(title, samples);
		} catch (IOException e) {
			System.out.println("Failed: " + title);
			System.out.println(e);
		}
	}

	public void run(String[] args) {
		// TODO: non-public endpoint
		generateTrainingSamples.setWikidataClient(WikidataClient.newPublicEndpointClient());

		for (String title : args) {
			processArticle(title);
		}
	}

	public static void main(String[] args) {
		BasicConfigurator.configure();
		new MakeTrainingSamples().run(args);
	}
}
