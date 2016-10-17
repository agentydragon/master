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
	private void processResult(Result result) throws IOException {
		byte[] rowkey = result.getRow();
		if (rowkey == null) {
			System.out.println("null rowkey");
			return;
		}
		SavedDocument document = new SavedDocument(result);
		if (document.plaintext == null || document.corenlpXml == null || document.spotlightJson == null ||
				document.sentences == null || document.coreferences == null || document.spotlightMentions == null) {
			return;
		}
		System.out.println(document.title);

		ArticleRepository.writeArticle(document.title, document.toJSON());
		System.out.println("written " + document.title);
	}

	public int run(String[] args) throws Exception {
		loadWhitelist();

		Configuration conf = getConf();
		HBaseAdmin admin = new HBaseAdmin(conf);
		try {
			HTable table = new HTable(conf, ArticlesTable.FULL_TABLE_NAME);

			int batchSize = 100;

			for (int i = 0; i < whitelist.size(); i += batchSize) {
				System.out.println("Batch " + i + " / " + whitelist.size());
				List<Get> batch = new ArrayList<>();
				for (int j = i; j < (i + batchSize) && (j < whitelist.size()); j++) {
					String title = whitelist.get(j);
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

		return 0;
	}

	private List<String> whitelist = new ArrayList<>();
	private void loadWhitelist() {
		Configuration conf = getConf();
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

	public static void main(String[] args) throws Exception {
		BasicConfigurator.configure();

		Configuration conf = HBaseConfiguration.create();
		conf.set("hbase.zookeeper.quorum", "hador-c1.ics.muni.cz:2181,hador-c2.ics.muni.cz:2181,hador.ics.muni.cz:2181");
		conf.setBoolean("hbase.security.auth.enable", true);
		conf.set("hbase.security.authentication", "kerberos");
		conf.set("hbase.kerberos.regionserver.principal", "hbase/_HOST@ICS.MUNI.CZ");
		conf.set("hbase.sasl.clientconfig", "Client");

		int res = ToolRunner.run(conf, new HBaseToJSON(), args);
		System.exit(res);
	}
}
