// Input: from DocumentProcessorMapper
// Output: Relation => Sentence expressing the relation

import java.io.IOException;
import org.xml.sax.SAXException;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.parsers.ParserConfigurationException;
import java.util.List;
import org.json.*;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.InputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;
import org.apache.log4j.Logger;

public class GenerateTrainingSamplesMapper extends Mapper<Text, Text, Text, Text> {
	static Logger log = Logger.getLogger(GetTrainingSamples.class);

	private WikidataClient wikidataClient;

	public void setWikidataClient(WikidataClient wikidataClient) {
		this.wikidataClient = wikidataClient;
	}

	public List<TrainingSamples.TrainingSample> makeTrainingSamples(String value) throws IOException {
		JSONObject inputJson = new JSONObject(value);

		String plaintext = (String) inputJson.get("text");
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

	@Override
	public void setup(Context context) {
		Configuration conf = context.getConfiguration();
		setWikidataClient(new WikidataClient(conf.get("wikidata_server")));
	}

	@Override
	public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
		String articleTitle = key.toString();
		List<TrainingSamples.TrainingSample> samples = makeTrainingSamples(value.toString());

		for (TrainingSamples.TrainingSample sample : samples) {
			String relation = sample.getRelation();
			JSONObject jo = new JSONObject()
				.put("sample", sample.toString());
			// TODO: output binary-serialized protocol buffers
			context.write(new Text(relation), new Text(jo.toString()));
		}
	}
}
