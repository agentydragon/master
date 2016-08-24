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

public class GenerateTrainingSamplesMapper extends Mapper<Text, Text, Text, Text> {
	@Override
	public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
		String articleTitle = key.toString();
		JSONObject inputJson = new JSONObject(value.toString());

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
		JSONObject spotlightJson = new JSONObject((String) inputJson.get("spotlight_json"));
		List<Sentence.SpotlightMention> spotlightMentions = AnnotateCoreferences.SpotlightToMentions(spotlightJson);
		documentProto = AnnotateCoreferences.PropagateEntities(documentProto, spotlightMentions);
		List<TrainingSamples.TrainingSample> samples = GetTrainingSamples.documentToSamples(documentProto);

		for (TrainingSamples.TrainingSample sample : samples) {
			String relation = sample.getRelation();
			JSONObject jo = new JSONObject()
				.put("sample", sample.toString());
			// TODO: output binary-serialized protocol buffers
			context.write(new Text(relation), new Text(jo.toString()));
		}
	}
}
