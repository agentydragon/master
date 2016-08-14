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
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;

public class WikiSplit {
	// implement custom InputFormat that processes entire file in blocks
	public static class MyFIF extends TextInputFormat {
		@Override
		protected boolean isSplitable(JobContext ctx, Path file) {
			// Never split up individual files.
			return false;
		}
	}

	public static class ArticleSplitterMapper extends Mapper<LongWritable, Text, Text, Text>{
		private Text word = new Text();
		private String articleName = null;
		private String articleText = "";

		private void flushArticle(Context context) throws IOException, InterruptedException {
			// flush article
			if (articleName != null) {
				context.write(new Text(/*"FLUSH - " + */articleName),
						new Text(articleText));
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

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "wiki split");
		job.setJarByClass(WikiSplit.class);

		// Set input.
		job.setInputFormatClass(MyFIF.class);
		MyFIF.addInputPath(job, new Path(args[0]));

		// Set mapper and input/output classes.
		job.setMapperClass(ArticleSplitterMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		// Set output.
		job.setOutputFormatClass(SequenceFileOutputFormat.class);
		TextOutputFormat.setOutputPath(job, new Path(args[1]));

		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}
