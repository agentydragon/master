// export HADOOP_CLASSPATH=`hbase mapredcp`:/storage/brno7-cerit/home/prvak/master/code/bazel-bin/hadoop/WikiSplit_deploy.jar
// hadoop jar (...)

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.hbase.HBaseConfiguration;
import java.lang.System;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
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
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.hbase.mapreduce.TableOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;

public class WikiSplit extends Configured implements Tool {
	// implement custom InputFormat that processes entire file in blocks
	public static class MyFIF extends TextInputFormat {
		@Override
		protected boolean isSplitable(JobContext ctx, Path file) {
			// Never split up individual files.
			return false;
		}
	}

	public enum Counters { PROCESSED_ARTICLES };

	//public static class ArticleSplitterMapper extends Mapper<LongWritable, Text, Text, Text>{
	public static class ArticleSplitterMapper<K> extends Mapper<LongWritable, Text, K, /*Writable*/Put>{
		private Text word = new Text();
		private String articleName = null;
		private String articleText = "";

		private void flushArticle(Context context) throws IOException, InterruptedException {
			// flush article
			if (articleName != null) {
				/*
				context.write(new Text(articleName),
						new Text(articleText));
				*/
				byte[] rowkey = articleName.getBytes();
				Put put = new Put(rowkey);
				put.add("wiki".getBytes(), "plaintext".getBytes(), articleText.getBytes());
				// (key ignored)
				context.write(null, put);

				//context.getCounter(Counters.PROCESSED_ARTICLES).increment(1);
			}
			articleText = "";
		}

		private String titleFromLine(String line) {
			if (line.length() > 4 && line.charAt(0) == '=' && line.charAt(1) == ' ' &&
					line.charAt(line.length() - 1) == '=' && line.charAt(line.length() - 2) == ' ') {
					/*line.substring(0, 2) == "= "*//* &&
					line.substring(line.length() - 2, line.length()) == " ="*///) {
				return line.substring(2, line.length() - 2);
			} else {
				return null;
			}
		}

		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

			String line = value.toString();
			String title = titleFromLine(line);
			if (title != null) {
				flushArticle(context);
				articleName = title;
			} else {
				articleText += line + "\n";
			}
	       }

	       public void cleanup(Context context) throws IOException, InterruptedException {
		       flushArticle(context);
	       }
	}

	public int run(String[] args) throws Exception {
		Configuration conf = getConf();
		Job job = Job.getInstance(conf, "wiki split");
		job.setJarByClass(WikiSplit.class);

		// Set input.
		job.setInputFormatClass(MyFIF.class);
		MyFIF.addInputPath(job, new Path(args[0]));

		// Set mapper and input/output classes.
		job.setMapperClass(ArticleSplitterMapper.class);
		//job.setMapOutputKeyClass(ImmutableBytesWritable.class);
		//job.setMapOutputValueClass(Put.class);
		job.setNumReduceTasks(0);

		//job.setOutputKeyClass(Text.class);
		//job.setOutputValueClass(Text.class);
		//job.setOutputKeyClass(ImmutableBytesWritable.class);
		//job.setOutputValueClass(Put.class);

		//job.setNumReduceTasks(0);

		// Set output.
		//job.setOutputFormatClass(SequenceFileOutputFormat.class);
		//TextOutputFormat.setOutputPath(job, new Path(args[1]));
		job.getConfiguration().set(TableOutputFormat.OUTPUT_TABLE, "prvak:wiki_articles");
		job.setOutputFormatClass(TableOutputFormat.class);

		return job.waitForCompletion(true) ? 0 : 1;
	}

	public static void main(String[] args) throws Exception {
		int res = ToolRunner.run(HBaseConfiguration.create(), new WikiSplit(), args);
		System.exit(res);
	}
}
