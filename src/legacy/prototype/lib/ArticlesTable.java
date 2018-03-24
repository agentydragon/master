import org.apache.hadoop.hbase.util.Bytes;

public class ArticlesTable {
	public static String FULL_TABLE_NAME_STRING = "prvak:wiki_articles";
	public static byte[] FULL_TABLE_NAME = Bytes.toBytes(FULL_TABLE_NAME_STRING);

	public static byte[] WIKI = Bytes.toBytes("wiki");
	public static byte[] PLAINTEXT = Bytes.toBytes("plaintext");
	public static byte[] CORENLP_XML = Bytes.toBytes("corenlp_xml");
	public static byte[] SPOTLIGHT_JSON = Bytes.toBytes("spotlight_json");

	public static byte[] SENTENCES = Bytes.toBytes("sentences");
	public static byte[] COREFERENCES = Bytes.toBytes("coreferences");
	public static byte[] SPOTLIGHT_MENTIONS = Bytes.toBytes("spotlight_mentions");
}
