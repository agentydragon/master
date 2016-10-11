import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.hbase.client.Put;
import java.lang.System;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;

//public static class ArticleSplitterMapper extends Mapper<LongWritable, Text, Text, Text>{
public class ArticleSplitterMapper<K> extends Mapper<LongWritable, Text, K, /*Writable*/Put>{
	private String articleName = null;
	private String articleText = "";

	private void writeArticle(Context context) throws IOException, InterruptedException {
		/*
		context.write(new Text(articleName),
				new Text(articleText));
		*/
		byte[] rowkey = articleName.getBytes();
		Put put = new Put(rowkey);
		put.add("wiki".getBytes(), "plaintext".getBytes(), articleText.getBytes());
		// (key ignored)
		context.write(null, put);
		//context.getCounter(Counters.PROCESSED_ARTICLES).increment(1);
	}

	private void flushArticle(Context context) throws IOException, InterruptedException {
		// flush article
		if (articleName != null) {
			writeArticle(context);
		}
		articleText = "";
	}

	private String titleFromLine(String line) {
		if (line.length() > 4 && line.charAt(0) == '=' && line.charAt(1) == ' ' &&
				line.charAt(line.length() - 1) == '=' && line.charAt(line.length() - 2) == ' ') {
				/*line.substring(0, 2) == "= "*//* &&
				line.substring(line.length() - 2, line.length()) == " ="*///) {
			return line.substring(2, line.length() - 2);
		} else {
			return null;
		}
	}

	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
		String line = value.toString();
		String title = titleFromLine(line);
		if (title != null) {
			flushArticle(context);
			articleName = title;
		} else {
			articleText += line + "\n";
		}
       }

       public void cleanup(Context context) throws IOException, InterruptedException {
	       flushArticle(context);
       }
}
