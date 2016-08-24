import java.lang.System;
import java.util.List;
import org.junit.Test;

public class GenerateTrainingSamplesMapperTest {
	@Test
	public void testSampleFile() throws Exception {
		String json = ParseXmlsToProtos.readFile("testdata/tharde.json");
		List<TrainingSamples.TrainingSample> samples = GenerateTrainingSamplesMapper.makeTrainingSamples(json);
		for (TrainingSamples.TrainingSample sample : samples) {
			System.out.println(sample.toString());
		}
	}
}
