import java.io.IOException;
import java.io.*;
import java.util.stream.*;

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
	};

	@Override
	protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
		String k = key.toString();
		String relation = k.split(":")[0];
		String article = k.substring(relation.length() + 1);

		String set = articleSet.getArticleSet(article);
		if (set == null) {
			context.getCounter(Counters.ARTICLES_IN_NO_SET).increment(1);
		} else {
			String outkey = relation + "S" + set;

			for (Text value : values) {
				mos.write(outkey, key, value);
			}
			context.getCounter(Counters.ARTICLES_WRITTEN_OK).increment(1);
		}
	}

	@Override
	protected void cleanup(Context context) throws IOException, InterruptedException {
		mos.close();
	}
}
