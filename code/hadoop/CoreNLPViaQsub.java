import java.io.IOException;
import java.util.StringTokenizer;

import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import org.apache.log4j.Logger;
import java.lang.Process;
import java.lang.ProcessBuilder;
import org.apache.commons.lang.RandomStringUtils;
import java.util.Properties;
import java.io.StringWriter;
import java.io.File;
import java.io.FileWriter;
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

// Input:
//   Key:   article name (Text)
//   Value: article plaintext (Text)
//
// Output:
//   Key:   article name (Text)
//   Value: article parse from CoreNLP as XML (Text)

public class CoreNLPViaQsub extends Configured implements Tool {
	public static class CoreNLPAnnotateViaQsubMapper extends Mapper<Text, Text, Text, Text>{
	    private Logger logger = Logger.getLogger(CoreNLPAnnotateViaQsubMapper.class);
		private boolean done = false;

		@Override
		public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
			/////////////////////////
			// (run just one row)
			if (done) {
				return;
			}
			done = true;
			/////////////////////////

			String articleTitle = key.toString();
			String articleText = value.toString();

			// TODO: queue this!

			String code = RandomStringUtils.randomAlphanumeric(8);
			String workDir = "/storage/brno7-cerit/home/prvak/corenlp-via-qsub-tmp";
			//String workDir = "/storage/brno7-cerit/home/prvak";
			String outputDir = workDir + "/output-" + code;
			String inputPath = workDir + "/in-" + code + ".txt";
			String outputPath = outputDir + "/in-" + code + ".txt.out";
			String binDir = "/storage/brno7-cerit/home/prvak/bin";

			String jobName = "corenlp-via-qsub-" + code;
			String jobscriptPath = workDir + "/" + jobName + ".sh";
			File jobscript = new File(jobscriptPath);
			FileWriter writer = new FileWriter(jobscript);
			writer.write(
				"#!/bin/bash\n" +
				"export LANG=en_US.UTF-8\n" +
				"export LANGUAGE=\n" +
				"export LC_CTYPE=en_US.UTF-8\n" +
				"export LC_NUMERIC=en_US.UTF-8\n" +
				"export LC_NAME=en_US.UTF-8\n" +
				"export LC_ALL=\n" +
				"# ^-- TODO HAX\n" +
				"\n" +
				"module add jdk-8\n" +
				"module add python34-modules-gcc\n" +
				"\n" +
				"cd $PBS_O_WORKDIR\n" +
				"cd " + binDir + "/launch_nlpize_articles_main.runfiles/__main__/\n" +
				"./nlpize_articles_main " +
					"--output_parse_xml_dirs " + outputDir + " " +
					"--parallel_runs 1 " +
					"--plaintext_files " + inputPath + "\n"
				);
			writer.close();

			ProcessBuilder pb = new ProcessBuilder(
					"qsub",
					"-l", "walltime=5:00",
					"-l", "nodes=1:ppn=2,mem=6gb",
					"-m", "abe",
					"-N", "corenlp-via-qsub-" + code,
					jobscriptPath);
			Process process = pb.start();
			int returnValue = process.waitFor();
			if (returnValue != 0) {
				logger.error("failed to process " + articleTitle + " " + code);
			} else {
				String text = new String(Files.readAllBytes(Paths.get(outputPath)), StandardCharsets.UTF_8);
				context.write(key, new Text(text));
			//	context.write(key, new Text(xmlOut.toString()));
			}
		}
	}

	public int run(String[] args) throws Exception {
		// Configuration processed by ToolRunner
		Configuration conf = getConf();

		// Create a JobConf using the processed conf
		Job job = Job.getInstance(conf, "corenlp-annotate-via-qsub");
		job.setJarByClass(CoreNLPViaQsub.class);

		job.setInputFormatClass(SequenceFileInputFormat.class);
		SequenceFileInputFormat.addInputPath(job, new Path(args[0]));

		job.setOutputFormatClass(SequenceFileOutputFormat.class);
		SequenceFileOutputFormat.setOutputPath(job, new Path(args[1]));

		job.setMapperClass(CoreNLPAnnotateViaQsubMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		// Submit the job, then poll for progress until the job is complete
		return job.waitForCompletion(true) ? 0 : 1;
	}

	public static void main(String[] args) throws Exception {
		// Let ToolRunner handle generic command-line options
		int res = ToolRunner.run(new Configuration(), new CoreNLPViaQsub(), args);
		System.exit(res);
	}
}
