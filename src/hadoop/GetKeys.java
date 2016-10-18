import org.apache.hadoop.conf.Configuration;
import org.apache.log4j.BasicConfigurator;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;
import java.util.*;
import org.apache.hadoop.hbase.util.*;
import org.apache.hadoop.hbase.filter.*;

// working as of 2016-10-11:
// export HADOOP_CLASSPATH=`hbase classpath`
// hadoop jar (...)/GetKeys_deploy.jar -Djava.security.auth.login.config=(...)/jaas.conf

public class GetKeys {
	public static void main(String[] args) throws Exception {
		BasicConfigurator.configure();

		Configuration conf = HBaseConfiguration.create();
		conf.set("hbase.zookeeper.quorum", "hador-c1.ics.muni.cz:2181,hador-c2.ics.muni.cz:2181,hador.ics.muni.cz:2181");
		conf.setBoolean("hbase.security.auth.enable", true);
		conf.set("hbase.security.authentication", "kerberos");
		conf.set("hbase.kerberos.regionserver.principal", "hbase/_HOST@ICS.MUNI.CZ");
		conf.set("hbase.sasl.clientconfig", "Client");

		HBaseAdmin admin = new HBaseAdmin(conf);
		Scan s = new Scan();
		FilterList fl = new FilterList();
		fl.addFilter(new FirstKeyOnlyFilter());
		fl.addFilter(new KeyOnlyFilter());
		s.setFilter(fl);

		List<String> keys = new ArrayList<>();

		try {
			HTable table = new HTable(conf, "prvak:wiki_articles");
			ResultScanner rs = table.getScanner(s);
			Result row = rs.next();
			while (row != null) {
				// System.out.println(new String(row.getRow()));
				keys.add(new String(row.getRow()));
				row = rs.next();
			}
		} finally {
			admin.close();
		}

		int nShards = 676;
		for (int i = 0; i < keys.size(); i += (keys.size() / nShards)) {
			System.out.println(keys.get(i));
		}
	}
}
