import java.io.*;
import java.lang.*;
import org.apache.hadoop.fs.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.*;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.HBaseAdmin;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.log4j.BasicConfigurator;

public class HBaseToJSON extends Configured implements Tool {
	private int ok = 0;
	private int nullRowKey = 0;
	private int noPlaintext = 0;
	private int noCorenlpXml = 0;
	private int noSpotlightJson = 0;
	private int noJoin = 0;

	private void processResult(Result result) throws IOException {
		byte[] rowkey = result.getRow();
		if (rowkey == null) {
			System.out.println("null rowkey");
			nullRowKey++;
			return;
		}
		SavedDocument document = new SavedDocument(result);
		if (document.plaintext == null) {
			noPlaintext++;
			return;
		}
		if (document.corenlpXml == null) {
			noCorenlpXml++;
			return;
		}
		if (document.spotlightJson == null) {
			noSpotlightJson++;
			return;
		}
		if (document.sentences == null || document.coreferences == null || document.spotlightMentions == null) {
			noJoin++;
			return;
		}
		System.out.println(document.title);

		ArticleRepository.writeArticle(document.title, document.toJSON());
		System.out.println("written " + document.title);
		ok++;
	}

	public int run(String[] args) throws Exception {
		loadWhitelist();

		Configuration conf = getConf();
		HBaseAdmin admin = new HBaseAdmin(conf);
		try {
			HTable table = new HTable(conf, ArticlesTable.FULL_TABLE_NAME);

			int batchSize = 100;

			List<String> articles = articleSet.getArticleList();
			for (int i = 0; i < articles.size(); i += batchSize) {
				System.out.println("Batch " + i + " / " + articles.size());
				List<Get> batch = new ArrayList<>();
				for (int j = i; j < (i + batchSize) && (j < articles.size()); j++) {
					String title = articles.get(j);
					batch.add(SavedDocument.getGet(title));
				}

				Result[] results = table.get(batch);
				for (Result result : results) {
					processResult(result);
				}
			}
		} finally {
			admin.close();
		}

		System.out.println("OK: " + ok);
		System.out.println("Null rowkey: " + nullRowKey);
		System.out.println("No plaintext: " + noPlaintext);
		System.out.println("No CoreNLP xml: " + noCorenlpXml);
		System.out.println("No Spotlight JSON: " + noSpotlightJson);
		System.out.println("No join: " + noJoin);

		return 0;
	}

	private ArticleSet articleSet;
	private void loadWhitelist() {
		Configuration conf = getConf();
		try {
			articleSet = new ArticleSet();
			articleSet.load(conf);
		} catch (IOException e) {
			e.printStackTrace();
			articleSet = null;
		}
	}

	public static void main(String[] args) throws Exception {
		BasicConfigurator.configure();

		Configuration conf = HBaseConfiguration.create();
		conf.addResource(new Path("/storage/brno2/home/prvak/master/src/hadoop/overrides.xml"));

		int res = ToolRunner.run(conf, new HBaseToJSON(), args);
		System.exit(res);
	}
}
