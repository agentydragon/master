import java.io.IOException;
import java.util.StringTokenizer;

import java.lang.System;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapred.lib.IdentityMapper;
import org.apache.hadoop.mapreduce.InputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class WikiSplit {
	// implement custom InputFormat that processes entire file in blocks
	public static class MyFIF extends TextInputFormat {
		@Override
		protected boolean isSplitable(JobContext ctx, Path file) {
			// Never split up individual files.
			return false;
		}
	}

	/*
	public static class ArticleSplitterMapper extends Mapper<LongWritable, Text, LongWritable, Text>{
		private Text word = new Text();
		private String articleName = null;
		private String articleText = "";

		private void flushArticle(Context context) throws IOException, InterruptedException {
			// flush article
			if (articleName != null) {
				context.write(new Text(articleName),
						new Text(articleText));
			}
			articleText = "";
		}

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
			System.out.println(key);
			System.out.println(value);
			// key = line offset
			// value = line
			String line = value.toString();
			// StringTokenizer itr = new StringTokenizer(value.toString());
			// while (itr.hasMoreTokens()) {
			//	word.set(itr.nextToken());
			//	context.write(word, one);
			//}

			if (line.length() > 2 &&
					line.substring(0, 2) == "= " &&
					line.substring(line.length() - 2, line.length()) == " =") {
				flushArticle(context);
				articleName = line.substring(2, line.length() - 2);
			} else {
				articleText += line + "\n";
			}
	       }

	       public void cleanup(Context context) throws IOException, InterruptedException {
		       flushArticle(context);
	       }
	}
	*/

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "wiki split");
		job.setJarByClass(WikiSplit.class);

		// Set input.
		job.setInputFormatClass(MyFIF.class);
		MyFIF.addInputPath(job, new Path(args[0]));

		// Set mapper and input/output classes.
	//	job.setMapperClass(ArticleSplitterMapper.class);
		job.setMapperClass(IdentityMapper.class);
		//job.setMapOutputKeyClass(Text.class);
		//job.setMapOutputValueClass(Text.class);

		//job.setOutputKeyClass(Text.class);
		//job.setOutputValueClass(Text.class);

		// Set output.
		job.setOutputFormatClass(TextOutputFormat.class);
		TextOutputFormat.setOutputPath(job, new Path(args[1]));

	//	job.setCombinerClass(IntSumReducer.class);
	//	job.setNumReduceTasks(0);
	//	job.setInputFormatClass(TextInputFormat.class);
	//	TextInputFormat.addInputPath(job, new Path(args[0]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}
