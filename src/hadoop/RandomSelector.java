import java.io.IOException;
import java.util.Properties;
import java.lang.System;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.InputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;

public class RandomSelector extends Configured implements Tool {
	public int run(String[] args) throws Exception {
		Configuration conf = getConf();
		if (conf.get("selection_probability") == null) {
			System.out.println("No selection_probability given");
			return 1;
		}

		Job job = Job.getInstance(conf, "random-select");
		job.setJarByClass(RandomSelector.class);

		job.setInputFormatClass(SequenceFileInputFormat.class);
		SequenceFileInputFormat.addInputPath(job, new Path(args[0]));

		job.setOutputFormatClass(SequenceFileOutputFormat.class);
		SequenceFileOutputFormat.setOutputPath(job, new Path(args[1]));

		job.setMapperClass(RandomSelectorMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		// Submit the job, then poll for progress until the job is complete
		return job.waitForCompletion(true) ? 0 : 1;
	}

	public static void main(String[] args) throws Exception {
		int res = ToolRunner.run(null, new RandomSelector(), args);
		System.exit(res);
	}
}
