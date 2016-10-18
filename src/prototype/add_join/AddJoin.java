import java.io.IOException;

import java.lang.System;
import org.apache.log4j.Logger;
import org.apache.log4j.BasicConfigurator;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
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

public class AddJoin extends Configured implements Tool {
	public int run(String[] args) throws Exception {
		// Configuration processed by ToolRunner
		Configuration conf = getConf();

		// Create a JobConf using the processed conf
		Job job = Job.getInstance(conf, AddJoin.class.getName());
		job.setJarByClass(AddJoin.class);

		Scan scanner = new Scan();
		scanner.addColumn(ArticlesTable.WIKI, ArticlesTable.PLAINTEXT);
		scanner.addColumn(ArticlesTable.WIKI, ArticlesTable.CORENLP_XML);
		scanner.addColumn(ArticlesTable.WIKI, ArticlesTable.SPOTLIGHT_JSON);
		// TODO: get only latest version; or overwrite.

		job.setNumReduceTasks(0);

		TableMapReduceUtil.initCredentials(job);

		// Set output.
		job.getConfiguration().set(TableOutputFormat.OUTPUT_TABLE, ArticlesTable.FULL_TABLE_NAME_STRING);
		job.setOutputFormatClass(TableOutputFormat.class);

		TableMapReduceUtil.initTableMapperJob(
				ArticlesTable.FULL_TABLE_NAME,
				scanner,
				AddJoinMapper.class,
				ImmutableBytesWritable.class,
				Put.class,
				job);

		int result = job.waitForCompletion(true) ? 0 : 1;
		System.out.println("Articles skipped (no plaintext): " + job.getCounters().findCounter(AddJoinMapper.Counters.ARTICLES_SKIPPED_NO_PLAINTEXT).getValue());
		System.out.println("Articles skipped (plaintext, no parse): " + job.getCounters().findCounter(AddJoinMapper.Counters.ARTICLES_SKIPPED_NO_PARSE).getValue());
		System.out.println("Articles skipped (plaintext, parse, no spotlight): " + job.getCounters().findCounter(AddJoinMapper.Counters.ARTICLES_SKIPPED_NO_SPOTLIGHT).getValue());
		System.out.println("Articles joined successfully: " + job.getCounters().findCounter(AddJoinMapper.Counters.ARTICLES_JOINED_SUCCESSFULLY).getValue());
		System.out.println("Articles failed with exception: " + job.getCounters().findCounter(AddJoinMapper.Counters.ARTICLES_FAILED_WITH_EXCEPTION).getValue());

		return result;
	}

	public static void main(String[] args) throws Exception {
		BasicConfigurator.configure();

		Configuration conf = HBaseConfiguration.create();
		conf.addResource(new Path("/storage/brno2/home/prvak/master/src/hadoop/overrides.xml"));

		int res = ToolRunner.run(conf, new AddJoin(), args);
		System.exit(res);
	}
}
