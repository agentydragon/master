import java.io.IOException;
import java.io.*;
import org.json.*;
import java.util.stream.*;

import java.util.*;
import java.lang.System;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.log4j.Logger;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapper;

public class MakeTrainingSamplesMapper extends TableMapper<Text, Text>{
//public class MakeTrainingSamplesMapper extends TableMapper<ImmutableBytesWritable, Put> { // Text, Text>{
	public static enum Counters {
		ARTICLES_SKIPPED_NO_PLAINTEXT,
		ARTICLES_SKIPPED_NO_PARSE,
		ARTICLES_SKIPPED_NO_SPOTLIGHT,
		ARTICLES_SKIPPED_NO_JOIN,
		ARTICLES_PROCESSED_SUCCESSFULLY, // TODO
		ARTICLES_FAILED_WITH_EXCEPTION,
		SAMPLES_PRODUCED,
		SAMPLES_FAILED_WITH_SERIALIZATION_EXCEPTION
	};

	private Logger logger = Logger.getLogger(MakeTrainingSamplesMapper.class);
	private WikidataClient wikidataClient;

	@Override
	public void setup(Context context) {
		logger.info("mapper setup");
		wikidataClient = new WikidataClient(context.getConfiguration());
	}

	@Override
	public void map(ImmutableBytesWritable rowkey, Result result, Context context) throws IOException, InterruptedException {
		String articleTitle = new String(rowkey.get());

		SavedDocument document = new SavedDocument(result);
		if (document.plaintext == null) {
			context.getCounter(Counters.ARTICLES_SKIPPED_NO_PLAINTEXT).increment(1);
			return;
		}
		if (document.corenlpXml == null) {
			context.getCounter(Counters.ARTICLES_SKIPPED_NO_PARSE).increment(1);
			return;
		}
		if (document.spotlightJson == null) {
			context.getCounter(Counters.ARTICLES_SKIPPED_NO_SPOTLIGHT).increment(1);
			return;
		}
		if (document.sentences == null) {
			context.getCounter(Counters.ARTICLES_SKIPPED_NO_JOIN).increment(1);
			return;
		}

		List<TrainingSample> samples = SampleGeneration.getLabeledSamplesFromDocument(document, wikidataClient);
		for (TrainingSample sample : samples) {
			try {
				context.write(new Text(sample.subject + ":" + sample.relation + ":" + sample.object), new Text(sample.toJSON().toString()));
			} catch (Exception e) {
				e.printStackTrace();
				context.getCounter(Counters.SAMPLES_FAILED_WITH_SERIALIZATION_EXCEPTION).increment(1);
			}
		}
		/*
		for (String relation : Relations.RELATIONS) {
			List<TrainingSample> s = samples.stream().filter(x -> x.relation.equals(relation)).collect(Collectors.toList());
			JSONArray ary = JSONUtils.toArray(s, TrainingSample::toJSON);

			Put put = new Put(rowkey.get());
			JSONObject o = new JSONObject()
				.put("samples", ary);
			put.add(Bytes.toBytes("ts"), Bytes.toBytes(relation),
					Bytes.toBytes(o.toString()));
			context.write(null, put);
		}
		*/
		context.getCounter(Counters.SAMPLES_PRODUCED).increment(samples.size());
		context.getCounter(Counters.ARTICLES_PROCESSED_SUCCESSFULLY).increment(1);
	}
}
