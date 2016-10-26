import java.io.IOException;

import java.lang.System;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.MultipleOutputs;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.log4j.BasicConfigurator;

public class MakeTrainingSamples extends Configured implements Tool {
	public int run(String[] args) throws Exception {
		Configuration conf = getConf();

		Job job = Job.getInstance(conf, MakeTrainingSamples.class.getName());
		job.setJarByClass(MakeTrainingSamples.class);

		Scan scanner = new Scan();
		scanner.addColumn(ArticlesTable.WIKI, ArticlesTable.PLAINTEXT);
		scanner.addColumn(ArticlesTable.WIKI, ArticlesTable.CORENLP_XML);
		scanner.addColumn(ArticlesTable.WIKI, ArticlesTable.SPOTLIGHT_JSON);
		scanner.addColumn(ArticlesTable.WIKI, ArticlesTable.SENTENCES);
		scanner.addColumn(ArticlesTable.WIKI, ArticlesTable.COREFERENCES);
		scanner.addColumn(ArticlesTable.WIKI, ArticlesTable.SPOTLIGHT_MENTIONS);
		// TODO: get only latest version; or overwrite.

		//job.setNumReduceTasks(0);

		TableMapReduceUtil.initCredentials(job);

		// Set output.

		FileOutputFormat.setOutputPath(job, new Path("/user/prvak/ts"));

		job.setReducerClass(MakeTrainingSamplesReducer.class);

		TableMapReduceUtil.initTableMapperJob(
				ArticlesTable.FULL_TABLE_NAME,
				scanner,
				MakeTrainingSamplesMapper.class,
				Text.class,
				Text.class,
				job);

		int result = job.waitForCompletion(true) ? 0 : 1;
		// TODO
		System.out.println("Articles skipped (no plaintext): " + job.getCounters().findCounter(MakeTrainingSamplesMapper.Counters.ARTICLES_SKIPPED_NO_PLAINTEXT).getValue());
		System.out.println("Articles skipped (plaintext, no parse): " + job.getCounters().findCounter(MakeTrainingSamplesMapper.Counters.ARTICLES_SKIPPED_NO_PARSE).getValue());
		System.out.println("Articles skipped (plaintext, parse, no spotlight): " + job.getCounters().findCounter(MakeTrainingSamplesMapper.Counters.ARTICLES_SKIPPED_NO_SPOTLIGHT).getValue());
		System.out.println("Articles skipped (plaintext, parse, spotlight, no join): " + job.getCounters().findCounter(MakeTrainingSamplesMapper.Counters.ARTICLES_SKIPPED_NO_JOIN).getValue());
		System.out.println("Articles processed successfully: " + job.getCounters().findCounter(MakeTrainingSamplesMapper.Counters.ARTICLES_PROCESSED_SUCCESSFULLY).getValue());
		System.out.println("Articles failed with exception: " + job.getCounters().findCounter(MakeTrainingSamplesMapper.Counters.ARTICLES_FAILED_WITH_EXCEPTION).getValue());
		System.out.println("Samples produced: " + job.getCounters().findCounter(MakeTrainingSamplesMapper.Counters.SAMPLES_PRODUCED).getValue());
		System.out.println("Articles in no set: " + job.getCounters().findCounter(MakeTrainingSamplesReducer.Counters.ARTICLES_IN_NO_SET).getValue());
		System.out.println("Articles written ok: " + job.getCounters().findCounter(MakeTrainingSamplesReducer.Counters.ARTICLES_WRITTEN_OK).getValue());

		return result;
	}

	public static void main(String[] args) throws Exception {
		BasicConfigurator.configure();

		Configuration conf = HBaseConfiguration.create();
		conf.addResource(new Path("/storage/brno2/home/prvak/master/src/hadoop/overrides.xml"));
		conf.set(JobContext.MAP_MEMORY_MB, 9000);
		conf.set(JobConf.MAPRED_TASK_JAVA_OPTS, "-Xmx8000m");
		conf.set(JobContext.MAP_JAVA_OPTS, "-Xmx8000m -XX:+UseParallelOldGC -XX:ParallelGCThreads=4");
		conf.set(JobContext.TASK_TIMEOUT, 60000000);

		int res = ToolRunner.run(conf, new MakeTrainingSamples(), args);
		System.exit(res);
	}
}
