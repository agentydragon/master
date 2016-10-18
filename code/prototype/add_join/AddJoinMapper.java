import java.io.IOException;
import java.io.*;

import java.util.*;
import java.lang.System;
import org.apache.log4j.Logger;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.hbase.mapreduce.TableMapper;

public class AddJoinMapper extends TableMapper<ImmutableBytesWritable, Put>{
	public static enum Counters {
		ARTICLES_SKIPPED_NO_PLAINTEXT,
		ARTICLES_SKIPPED_NO_PARSE,
		ARTICLES_SKIPPED_NO_SPOTLIGHT,
		ARTICLES_JOINED_SUCCESSFULLY,
		ARTICLES_FAILED_WITH_EXCEPTION,
	};

	private Logger logger = Logger.getLogger(AddJoinMapper.class);
	private DBpediaClient dbpediaClient;

	@Override
	public void setup(Context context) {
		logger.info("mapper setup");
		dbpediaClient = new DBpediaClient(context.getConfiguration());
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

		try {
			document.addProtoToDocument(dbpediaClient);

			Put put = new Put(rowkey.get());
			put.add(ArticlesTable.WIKI, ArticlesTable.SENTENCES, document.getSentencesSerialization());
			put.add(ArticlesTable.WIKI, ArticlesTable.COREFERENCES, document.getCoreferencesSerialization());
			put.add(ArticlesTable.WIKI, ArticlesTable.SPOTLIGHT_MENTIONS, document.getSpotlightMentionsSerialization());
			context.write(null, put);
			context.getCounter(Counters.ARTICLES_JOINED_SUCCESSFULLY).increment(1);
		} catch (Exception e) {
			e.printStackTrace();
			context.getCounter(Counters.ARTICLES_FAILED_WITH_EXCEPTION).increment(1);
		}
	}
}
