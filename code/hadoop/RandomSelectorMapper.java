import java.io.IOException;
import java.util.StringTokenizer;
import java.util.Random;
import java.util.Properties;
import java.io.StringWriter;
import java.lang.System;
import org.apache.log4j.Logger;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.InputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;

public class RandomSelectorMapper extends Mapper<Text, Text, Text, Text>{
	private Logger logger = Logger.getLogger(RandomSelectorMapper.class);
	private double probability;
	private Random random = new Random();

	@Override
	public void setup(Context context) {
		logger.info("mapper setup");
		Configuration conf = context.getConfiguration();
		probability = conf.getDouble("selection_probability", -1);
		if (probability < 0 || probability > 1) {
			logger.error("Invalid selection probability");
			System.exit(1);
		}
	}

	@Override
	public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
		if (random.nextDouble() < probability) {
			context.write(key, value);
		}
	}
}
