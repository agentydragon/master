import org.json.*;
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
		String title = new String(rowkey);
		byte[] plaintextBytes = result.getValue(Bytes.toBytes("wiki"), Bytes.toBytes("plaintext"));
		String plaintext = null;
		if (plaintextBytes != null) {
			plaintext = new String(plaintextBytes);
		}
		byte[] corenlpXmlBytes = result.getValue(Bytes.toBytes("wiki"), Bytes.toBytes("corenlp_xml"));
		String corenlpXml = null;
		if (corenlpXmlBytes != null) {
			corenlpXml = new String(corenlpXmlBytes);
		}
		String spotlightJson = null;
		byte[] spotlightJsonBytes = result.getValue(Bytes.toBytes("wiki"),
				Bytes.toBytes("spotlight_json"));
		if (spotlightJsonBytes != null) {
		       spotlightJson = new String(spotlightJsonBytes);
		}

		if (plaintext == null || corenlpXml == null || spotlightJson == null) {
			return;
		}
		System.out.println(title);
		// System.out.println(plaintext);
		// System.out.println(corenlpXml);
		// System.out.println(spotlightJson);

		JSONObject json = new JSONObject(); //ArticleRepository.readArticle(title);
		json.put("title", title);
		json.put("plaintext", plaintext);
		json.put("corenlp_xml", corenlpXml);
		json.put("spotlight_json", new JSONObject(spotlightJson));

		ArticleRepository.writeArticle(title, json);
		System.out.println("written " + title);
	}

	public int run(String[] args) throws Exception {
		loadWhitelist();

		Configuration conf = getConf();
		HBaseAdmin admin = new HBaseAdmin(conf);
		try {
			HTable table = new HTable(conf, "prvak:wiki_articles");

			int batchSize = 100;

			for (int i = 0; i < whitelist.size(); i += batchSize) {
				System.out.println("Batch " + i + " / " + whitelist.size());
				List<Get> batch = new ArrayList<>();
				for (int j = i; j < (i + batchSize) && (j < whitelist.size()); j++) {
					String title = whitelist.get(j);
					Get get = new Get(Bytes.toBytes(title)); //"George Washington"));
					get.addColumn(Bytes.toBytes("wiki"),
							Bytes.toBytes("plaintext"));
					get.addColumn(Bytes.toBytes("wiki"),
							Bytes.toBytes("corenlp_xml"));
					get.addColumn(Bytes.toBytes("wiki"),
							Bytes.toBytes("spotlight_json"));
					batch.add(get);
				}

				Result[] results = table.get(batch);
				for (Result result : results) {
					processResult(result);
				}
			}

		//	Put put = new Put(Bytes.toBytes("Hello"));
		//	put.add(Bytes.toBytes("wiki"), Bytes.toBytes("plaintext"), Bytes.toBytes("Hello hello ..."));
		//	table.put(put);
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

	/*
	private void processArticle(String title) {
		try {
			System.out.println(title);

			if (!ArticleRepository.articleExists(title)) {
				System.out.println("Article doesn't exist");
				return;
			}

			JSONObject json = ArticleRepository.readArticle(title);

			// Skip if already processed.
			if (json.has("corenlp_xml") && json.get("corenlp_xml") != JSONObject.NULL) {
				System.out.println("Article already annotated");
				return;
			}

			String articleText = (String) json.get("plaintext");
			json.put("corenlp_xml", corenlpInterface.getXML(articleText));
			ArticleRepository.writeArticle(title, json);
		} catch (IOException e) {
			System.out.println("Failed: " + title);
			System.out.println(e);
		}
	}
	*/

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
