import java.io.IOException;
import java.io.*;

import org.apache.hadoop.fs.*;
import java.util.*;
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
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.InputFormat;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.hbase.mapreduce.TableMapper;

public class SpotlightAnnotatorMapper extends TableMapper<ImmutableBytesWritable, Put>{
	private Logger logger = Logger.getLogger(SpotlightAnnotatorMapper.class);
	private SpotlightConnection connection;

	private Set<String> whitelist = new HashSet<>();
	private void loadWhitelist(Configuration conf) {
		try {
			FileSystem fs = FileSystem.get(conf);
			FSDataInputStream inputStream = fs.open(new Path("/user/prvak/articles.tsv"));
			try (BufferedReader r = new BufferedReader(new InputStreamReader(inputStream))) {
				String line;
				while  ((line = r.readLine()) != null) {
					whitelist.add(line.split("\t")[1]);
				}
			}

			inputStream.close();
		} catch (IOException e) {
			e.printStackTrace();
			whitelist = null;
		}
	}

	// public static boolean startOwnSpotlight = true;

	@Override
	public void setup(Context context) {
		logger.info("mapper setup");
		Configuration conf = context.getConfiguration();

		loadWhitelist(conf);
		/*
		if (startOwnSpotlight) {
			try {
				server.start();
			} catch (IOException e) {
				logger.error("failed to start Spotlight server", e);
				System.exit(1);
			}
			connection = new SpotlightConnection("http://localhost:2222/rest/annotate");
		} else {
		*/

		String[] connectionUrls = SpotlightPooledConnection.splitEndpointList(conf.get("spotlight_server"));
		connection = new SpotlightPooledConnection(connectionUrls);
		//}
	}

	@Override
	public void cleanup(Context context) {
		/*
		if (startOwnSpotlight) {
			server.stop();
		}
		*/
	}

	@Override
	public void map(ImmutableBytesWritable rowkey, Result result, Context context) throws IOException, InterruptedException {
		//String articleTitle = key.toString();
		//String articleText = value.toString();

		String articleTitle = new String(rowkey.get());

		if (!whitelist.contains(articleTitle)) {
			return;
		}

		String articleText = new String(result.getValue("wiki".getBytes(), "plaintext".getBytes()));

		try {
			//String jsonOut = connection.getAnnotationJSON(articleText);
			//context.write(key, new Text(jsonOut.toString()));
			Put put = new Put(rowkey.get());
			String jsonOut = connection.getAnnotationJSON(articleText);
			put.add("wiki".getBytes(), "spotlight_json".getBytes(), jsonOut.getBytes());
			context.write(null, put);
		} catch (IOException e) {
			// nothing -- TODO (response code 400 sometimes)
		}
	}
}
