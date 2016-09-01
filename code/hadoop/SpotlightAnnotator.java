// Can't run both DBpedia Spotlight and Hadoop MR in one subprocess
// because of clash in log4j.

import java.io.IOException;
import java.util.StringTokenizer;

import java.util.Properties;
import java.io.StringWriter;
import java.lang.System;
import org.apache.log4j.Logger;
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

// Input:
//   Key:   article name (Text)
//   Value: article plaintext (Text)
//
// Output:
//   Key:   article name (Text)
//   Value: article spotting from Spotlight as JSON (Text)
//
// Arguments: (input) (output)

public class SpotlightAnnotator extends Configured implements Tool {
	public static class SpotlightAnnotatorMapper extends Mapper<Text, Text, Text, Text>{
		private Logger logger = Logger.getLogger(SpotlightAnnotatorMapper.class);
		// private SpotlightServer server;
		private SpotlightConnection connection;

		// public static boolean startOwnSpotlight = true;

		@Override
		public void setup(Context context) {
			logger.info("mapper setup");
			Configuration conf = context.getConfiguration();

			/*
			if (startOwnSpotlight) {
				try {
					server.start();
				} catch (IOException e) {
					logger.error("failed to start Spotlight server", e);
					System.exit(1);
				}
				connection = new SpotlightConnection("http://localhost:2222/rest/annotate");
			} else {
			*/
				connection = new SpotlightConnection(conf.get("spotlight_server"));
			//}
		}

		@Override
		public void cleanup(Context context) {
			/*
			if (startOwnSpotlight) {
				server.stop();
			}
			*/
		}

		@Override
		public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
			String articleTitle = key.toString();
			String articleText = value.toString();

			try {
				String jsonOut = connection.getAnnotationJSON(articleText);
				context.write(key, new Text(jsonOut.toString()));
			} catch (IOException e) {
				// nothing -- TODO (response code 400 sometimes)
			}
		}
	}

	public int run(String[] args) throws Exception {
		// Configuration processed by ToolRunner
		Configuration conf = getConf();
		for (int i = 0; i < args.length; i++) {
			System.out.println("args[" + i + "]=" + args[i]);
		}
		/*
		if (!SpotlightAnnotatorMapper.startOwnSpotlight) {
			if (conf.get("spotlight_server") == null) {
				System.out.println("No spotlight_server given");
				return 1;
			}
		}
		*/

		// Create a JobConf using the processed conf
		Job job = Job.getInstance(conf, "spotlight-annotate");
		job.setJarByClass(SpotlightAnnotator.class);

		job.setInputFormatClass(SequenceFileInputFormat.class);
		SequenceFileInputFormat.addInputPath(job, new Path(args[0]));

		job.setOutputFormatClass(SequenceFileOutputFormat.class);
		SequenceFileOutputFormat.setOutputPath(job, new Path(args[1]));

		job.setMapperClass(SpotlightAnnotatorMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		// Submit the job, then poll for progress until the job is complete
		return job.waitForCompletion(true) ? 0 : 1;
	}

	public static void main(String[] args) throws Exception {
		int res = ToolRunner.run(null, new SpotlightAnnotator(), args);
		System.exit(res);
	}
}
