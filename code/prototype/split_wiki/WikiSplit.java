import java.lang.System;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.hbase.mapreduce.TableOutputFormat;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.log4j.BasicConfigurator;

public class WikiSplit extends Configured implements Tool {
	// Custom InputFormat that processes entire file in blocks.
	public static class MyFIF extends TextInputFormat {
		@Override
		protected boolean isSplitable(JobContext ctx, Path file) {
			// Never split up individual files.
			return false;
		}
	}

	public int run(String[] args) throws Exception {
		Configuration conf = getConf();
		Job job = Job.getInstance(conf, WikiSplit.class.getName());
		job.setJarByClass(WikiSplit.class);

		// Set input.
		job.setInputFormatClass(MyFIF.class);
		MyFIF.addInputPath(job, new Path(args[0]));

		job.setMapperClass(ArticleSplitterMapper.class);
		job.setNumReduceTasks(0);

		// Set output.
		job.getConfiguration().set(TableOutputFormat.OUTPUT_TABLE, ArticlesTable.FULL_TABLE_NAME_STRING);
		job.setOutputFormatClass(TableOutputFormat.class);

		TableMapReduceUtil.initCredentials(job);

		return job.waitForCompletion(true) ? 0 : 1;
	}

	public static void main(String[] args) throws Exception {
		BasicConfigurator.configure();

		Configuration conf = HBaseConfiguration.create();
		conf.addResource(new Path("/storage/brno2/home/prvak/master/code/hadoop/overrides.xml"));

		int res = ToolRunner.run(conf, new WikiSplit(), args);
		System.exit(res);
	}
}
