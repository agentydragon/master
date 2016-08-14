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
import edu.stanford.nlp.io.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.util.*;
import edu.stanford.nlp.ling.*;

// Input:
//   Key:   article name (Text)
//   Value: article plaintext (Text)
//
// Output:
//   Key:   article name (Text)
//   Value: article parse from CoreNLP as XML (Text)

public class CoreNLP extends Configured implements Tool {
	public static class CoreNLPAnnotateMapper extends Mapper<Text, Text, Text, Text>{
		private StanfordCoreNLP pipeline;

		@Override
		public void setup(Context context) {
			Properties props = new Properties();
			// TODO: MODEL
			props.put("annotators",
					"tokenize,ssplit,parse," +
					"lemma,ner,dcoref");
			pipeline = new StanfordCoreNLP(props);
		}

		@Override
		public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
			String articleTitle = key.toString();
			String articleText = value.toString();

			// Reduce the length of the text.
			// XXX: HAX
			int length = articleText.length();
			if (length > 1000) {
				length = 1000;
			}
			articleText = articleText.substring(0, length);

			StringWriter xmlOut = new StringWriter();

			Annotation annotation = new Annotation(articleText);
			pipeline.annotate(annotation);
			pipeline.xmlPrint(annotation, xmlOut);

			context.write(key, new Text(xmlOut.toString()));
	       }
	}

	public int run(String[] args) throws Exception {
		// Configuration processed by ToolRunner
		Configuration conf = getConf();

		// Create a JobConf using the processed conf
		Job job = Job.getInstance(conf, "corenlp-annotate");
		job.setJarByClass(CoreNLP.class);

		// Specify various job-specific parameters
		job.setJobName("corenlp-annotate");

		job.setInputFormatClass(SequenceFileInputFormat.class);
		SequenceFileInputFormat.addInputPath(job, new Path(args[0]));

		job.setOutputFormatClass(SequenceFileOutputFormat.class);
		SequenceFileOutputFormat.setOutputPath(job, new Path(args[1]));

		job.setMapperClass(CoreNLPAnnotateMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		// Submit the job, then poll for progress until the job is complete
		return job.waitForCompletion(true) ? 0 : 1;
	}

	public static void main(String[] args) throws Exception {
		// Let ToolRunner handle generic command-line options
		int res = ToolRunner.run(new Configuration(), new CoreNLP(), args);
		System.exit(res);
	}

	/*
	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "corenlp annotate");
		job.setJarByClass(CoreNLP.class);

		// Set input.
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
	*/
}
