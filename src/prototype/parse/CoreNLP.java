import java.lang.System;
import java.util.Arrays;
import java.io.*;
import org.apache.hadoop.fs.*;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.hbase.mapreduce.TableOutputFormat;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.log4j.BasicConfigurator;

// Arguments: -Dprefix_length=200

public class CoreNLP extends Configured implements Tool {
	public int run(String[] args) throws Exception {
		Configuration conf = getConf();

		if (conf.get("prefix_length") == null) {
			System.out.println("No prefix_length given");
			return 1;
		}

		Job job = Job.getInstance(conf, CoreNLP.class.getName());
		job.setJarByClass(CoreNLP.class);

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
				CoreNLPAnnotateMapper.class,
				ImmutableBytesWritable.class,
				Put.class,
				job);

		// Configuration.dumpConfiguration(job.getConfiguration(), new OutputStreamWriter(System.out));

		int result = job.waitForCompletion(true) ? 0 : 1;
		System.out.println("Articles skipped (not in whitelist):" + job.getCounters().findCounter(CoreNLPAnnotateMapper.Counters.ARTICLES_SKIPPED_NOT_IN_WHITELIST).getValue());
		System.out.println("Articles in whitelist: " + job.getCounters().findCounter(CoreNLPAnnotateMapper.Counters.ARTICLES_IN_WHITELIST).getValue());
		System.out.println("Articles parsed successfully: " + job.getCounters().findCounter(CoreNLPAnnotateMapper.Counters.ARTICLES_PARSED_SUCCESSFULLY).getValue());
		System.out.println("Articles failed (IllegalArgumentException): " + job.getCounters().findCounter(CoreNLPAnnotateMapper.Counters.ARTICLES_FAILED_ILLEGAL_ARGUMENT_EXCEPTION).getValue());

		return result;
	}

	public static void main(String[] args) throws Exception {
		BasicConfigurator.configure();

		Configuration conf = HBaseConfiguration.create();
		conf.addResource(new Path("/storage/brno2/home/prvak/master/src/hadoop/overrides.xml"));
		conf.setLong(JobContext.MAP_MEMORY_MB, 9000);
		conf.set(JobContext.MAP_JAVA_OPTS, "-Xmx8000m -XX:+UseParallelOldGC -XX:ParallelGCThreads=4");
		conf.setLong(JobContext.TASK_TIMEOUT, 60000000);
		conf.setInt(JobContext.MAP_MAX_ATTEMPTS, 1);

		int res = ToolRunner.run(conf, new CoreNLP(), args);
		System.exit(res);
	}
}
