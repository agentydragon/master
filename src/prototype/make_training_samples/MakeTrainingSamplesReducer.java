import java.io.IOException;
import java.io.*;
import java.util.stream.*;
import java.lang.*;

import org.json.*;
import java.util.*;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.lib.output.MultipleOutputs;
import org.apache.hadoop.mapreduce.Reducer;

public class MakeTrainingSamplesReducer extends Reducer<Text, Text, Text, Text> {
	private MultipleOutputs mos;
	private ArticleSet articleSet;

	@Override
	protected void setup(Context context) throws IOException {
		mos = new MultipleOutputs(context);
		articleSet = new ArticleSet();
		articleSet.load(context.getConfiguration());
	}

	public static enum Counters {
		ARTICLES_WRITTEN_OK,
		ARTICLES_IN_NO_SET,
		SAMPLES_SKIPPED_EXCEPTION
	};

	@Override
	protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
		String k = key.toString();
		System.out.println("Key: " + k);
		String[] splits = k.split(":");
		String subject = splits[0], relation = splits[1], object = splits[2];

		int hashCode = (subject + ":" + relation + ":" + object).hashCode();
		if (hashCode < 0) hashCode = -hashCode;
		hashCode %= 100;

		String set;
		if (hashCode < 70) {
			set = "train";
		} else if (hashCode < 75) {
			set = "validate";
		} else {
			set = "test-known";
		}

		String fileName = null;

		for (Text value : values) {
			if (fileName == null) {
				try {
					TrainingSample ts = TrainingSample.fromJSON(new JSONObject(value.toString()));
					if (ts.positive == TrainingSample.Positiveness.UNKNOWN) {
						// fileName = generateFileName(relation, "test-unknown");
						continue;
					} else {
						fileName = generateFileName(relation, set);
					}
				} catch (Exception e) {
					e.printStackTrace();
					context.getCounter(Counters.SAMPLES_SKIPPED_EXCEPTION).increment(1);
					continue;
				}
			}
			mos.write(key, value, fileName);
		}
		context.getCounter(Counters.ARTICLES_WRITTEN_OK).increment(1);
	}

	private static String generateFileName(String relation, String set) {
		return relation + "/" + set;
	}

	@Override
	protected void cleanup(Context context) throws IOException, InterruptedException {
		mos.close();
	}
}
