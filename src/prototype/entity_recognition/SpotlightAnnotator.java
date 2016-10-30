// Can't run both DBpedia Spotlight and Hadoop MR in one subprocess
// because of clash in log4j.

import java.io.IOException;

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
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.hbase.mapreduce.TableOutputFormat;
import org.apache.log4j.BasicConfigurator;

// Input:
//   Key:   article name (Text)
//   Value: article plaintext (Text)
//
// Output:
//   Key:   article name (Text)
//   Value: article spotting from Spotlight as JSON (Text)
//
// Arguments: -D spotlight_server=http://(...),http://(...),http://(...) (input) (output)

public class SpotlightAnnotator extends Configured implements Tool {
	public int run(String[] args) throws Exception {
		// Configuration processed by ToolRunner
		Configuration conf = getConf();
		/*
		if (!SpotlightAnnotatorMapper.startOwnSpotlight) {
			if (conf.get("spotlight_server") == null) {
				System.out.println("No spotlight_server given");
				return 1;
			}
		}
		*/

		// Create a JobConf using the processed conf
		Job job = Job.getInstance(conf, SpotlightAnnotator.class.getName());
		job.setJarByClass(SpotlightAnnotator.class);

		Scan scanner = new Scan();
		scanner.addColumn(ArticlesTable.WIKI, ArticlesTable.PLAINTEXT);
		// TODO: get only latest version; or overwrite.

		job.setNumReduceTasks(0);

		TableMapReduceUtil.initCredentials(job);

		// Set output.
		job.getConfiguration().set(TableOutputFormat.OUTPUT_TABLE, ArticlesTable.FULL_TABLE_NAME_STRING);
		job.setOutputFormatClass(TableOutputFormat.class);

		TableMapReduceUtil.initTableMapperJob(
				ArticlesTable.FULL_TABLE_NAME,
				scanner,
				SpotlightAnnotatorMapper.class,
				ImmutableBytesWritable.class,
				Put.class,
				job);

		int result = job.waitForCompletion(true) ? 0 : 1;
		System.out.println("Articles skipped (not in whitelist): " + job.getCounters().findCounter(SpotlightAnnotatorMapper.Counters.ARTICLES_SKIPPED_NOT_IN_WHITELIST).getValue());
		System.out.println("Articles in whitelist: " + job.getCounters().findCounter(SpotlightAnnotatorMapper.Counters.ARTICLES_IN_WHITELIST).getValue());
		System.out.println("Articles failed with exception: " + job.getCounters().findCounter(SpotlightAnnotatorMapper.Counters.ARTICLES_FAILED_WITH_EXCEPTION).getValue());
		System.out.println("Articles annotated successfully: " + job.getCounters().findCounter(SpotlightAnnotatorMapper.Counters.ARTICLES_ANNOTATED_SUCCESSFULLY).getValue());

		return result;
	}

	public static void main(String[] args) throws Exception {
		BasicConfigurator.configure();

		Configuration conf = HBaseConfiguration.create();
		conf.addResource(new Path("/storage/brno2/home/prvak/master/src/hadoop/overrides.xml"));

		// TODO: Reduce memory?
		conf.setLong(JobContext.MAP_MEMORY_MB, 1000);
		conf.set(JobContext.MAP_JAVA_OPTS, "-Xmx800m -XX:+UseParallelOldGC -XX:ParallelGCThreads=4");
		conf.setLong(JobContext.TASK_TIMEOUT, 600000);
		conf.setLong(JobContext.MAP_MAX_ATTEMPTS, 1);

		int res = ToolRunner.run(conf, new SpotlightAnnotator(), args);
		System.exit(res);
	}
}
