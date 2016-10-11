import org.apache.hadoop.hbase.client.Put;
import org.apache.log4j.BasicConfigurator;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.hbase.HBaseConfiguration;
import java.lang.System;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.hbase.mapreduce.TableOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;

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

		// Set mapper and input/output classes.
		job.setMapperClass(ArticleSplitterMapper.class);
		//job.setMapOutputValueClass(Put.class);
		job.setNumReduceTasks(0);

		//job.setOutputKeyClass(Text.class);
		//job.setOutputValueClass(Text.class);
		//job.setOutputValueClass(Put.class);

		//job.setNumReduceTasks(0);

		// Set output.
		//job.setOutputFormatClass(SequenceFileOutputFormat.class);
		//TextOutputFormat.setOutputPath(job, new Path(args[1]));
		job.getConfiguration().set(TableOutputFormat.OUTPUT_TABLE, "prvak:wiki_articles");
		job.setOutputFormatClass(TableOutputFormat.class);

		TableMapReduceUtil.initCredentials(job);

		return job.waitForCompletion(true) ? 0 : 1;
	}

	public static void main(String[] args) throws Exception {
		BasicConfigurator.configure();

		Configuration conf = HBaseConfiguration.create();
		conf.set("hbase.zookeeper.quorum", "hador-c1.ics.muni.cz:2181,hador-c2.ics.muni.cz:2181,hador.ics.muni.cz:2181");
		conf.setBoolean("hbase.security.auth.enable", true);
		conf.set("hbase.security.authentication", "kerberos");
		conf.set("hbase.kerberos.regionserver.principal", "hbase/_HOST@ICS.MUNI.CZ");
		conf.set("hbase.sasl.clientconfig", "Client");
		int res = ToolRunner.run(conf, new WikiSplit(), args);
		System.exit(res);
	}
}
