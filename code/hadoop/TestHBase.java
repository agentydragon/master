import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.util.*;

public class TestHBase {
	public static void main(String[] args) throws Exception {
		Configuration conf = HBaseConfiguration.create();
		HBaseAdmin admin = new HBaseAdmin(conf);
		try {
			HTable table = new HTable(conf, "prvak:wiki_articles");
			Put put = new Put(Bytes.toBytes("Hello"));
			put.add(Bytes.toBytes("wiki"), Bytes.toBytes("plaintext"), Bytes.toBytes("Hello hello ..."));
			table.put(put);
		} finally {
			admin.close();
		}
	}
}
