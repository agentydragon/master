import org.apache.hadoop.conf.Configuration;
import org.apache.log4j.BasicConfigurator;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.util.*;

// working as of 2016-10-11:
// export HADOOP_CLASSPATH=`hbase classpath`
// hadoop jar (...)/TestHBase_deploy.jar -Djava.security.auth.login.config=(...)/jaas.conf

public class TestHBase {
	public static void main(String[] args) throws Exception {
		BasicConfigurator.configure();

		Configuration conf = HBaseConfiguration.create();
		conf.set("hbase.zookeeper.quorum", "hador-c1.ics.muni.cz:2181,hador-c2.ics.muni.cz:2181,hador.ics.muni.cz:2181");
		conf.setBoolean("hbase.security.auth.enable", true);
		conf.set("hbase.security.authentication", "kerberos");
		conf.set("hbase.kerberos.regionserver.principal", "hbase/_HOST@ICS.MUNI.CZ");
		conf.set("hbase.sasl.clientconfig", "Client");

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
