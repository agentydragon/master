import org.json.*;
import java.io.IOException;
import java.util.StringTokenizer;

import java.util.Properties;
import java.io.StringWriter;
import java.lang.System;
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

// Input: Article title (Text) => Article text (Text)
// Output: Article title (Text) => JSON:
//	{"plaintext": "...", "corenlp_xml": "<...>", "spotlight_json": "..."}

public class DocumentProcessorMapper extends Mapper<Text, Text, Text, Text> {
	private CoreNLPInterface corenlpInterface = new CoreNLPInterface();
	// TODO: load-balance
	private SpotlightConnection spotlightConnection;
	// private int prefixLength;

	@Override
	public void setup(Context context) {
		Configuration conf = context.getConfiguration();
		setSpotlightServer(conf.get("spotlight_server"));
		setNLPPipeline();
	}

	public void setSpotlightServer(String server) {
		String[] servers = SpotlightPooledConnection.splitEndpointList(server);
		spotlightConnection = new SpotlightPooledConnection(servers);
	}

	public void setNLPPipeline() {
		corenlpInterface.setup();
	}

	public String articleToJson(String articleTitle, String articleText) throws IOException {
		// Reduce the length of the text.
		// XXX: HAX
		/*
		int length = articleText.length();
		if (length > prefixLength) {
			length = prefixLength;
		}
		articleText = articleText.substring(0, length);
		*/

		String spotlightJsonOut;
		spotlightJsonOut = spotlightConnection.getAnnotationJSON(articleText);
		// nothing -- TODO (response code 400 sometimes)

		//	context.write(key, new Text(jsonOut.toString()));

		String jsonOut = new JSONObject()
			.put("corenlp_xml", corenlpInterface.getXML(articleText))
			.put("spotlight_json", spotlightJsonOut)
			.put("plaintext", articleText)
			.put("title", articleTitle).toString();
		return jsonOut;
	}

	@Override
	public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
		String articleTitle = key.toString();
		String articleText = value.toString();

		String jsonOut = null;
		try {
			jsonOut = articleToJson(articleTitle, articleText);
		} catch (IOException e) {
			// TODO
			return;
		}
		context.write(key, new Text(jsonOut));
	}
}
