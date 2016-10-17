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
		if (document.plaintext == null || document.corenlpXml == null || document.spotlightJson == null) {
			// TODO: Increase counters?
			return;
		}

		try {
			document.addProtoToDocument(dbpediaClient);

			Put put = new Put(rowkey.get());
			put.add(ArticlesTable.WIKI, ArticlesTable.SENTENCES, document.getSentencesSerialization());
			put.add(ArticlesTable.WIKI, ArticlesTable.COREFERENCES, document.getCoreferencesSerialization());
			put.add(ArticlesTable.WIKI, ArticlesTable.SPOTLIGHT_MENTIONS, document.getSpotlightMentionsSerialization());
			context.write(null, put);
		} catch (Exception e) {
			e.printStackTrace();
			// TODO
		}
	}
}
