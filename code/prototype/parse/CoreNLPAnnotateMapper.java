import java.io.IOException;

import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.hbase.mapreduce.TableMapper;

//public class CoreNLPAnnotateMapper extends Mapper<Text, Text, Text, Text>{

// output key: K
// output value: Put
public class CoreNLPAnnotateMapper/*<K>*/ extends TableMapper</*K*/ImmutableBytesWritable, Put>{
	private int prefixLength;
	private CoreNLPInterface corenlpInterface = new CoreNLPInterface();

	@Override
	public void setup(Context context) {
		Configuration conf = context.getConfiguration();
		prefixLength = conf.getInt("prefix_length", 10);
		corenlpInterface.setup();
	}

	@Override
	public void map(ImmutableBytesWritable rowkey, Result result, Context context) throws IOException, InterruptedException {
		//String articleText = value.toString();
		String articleText = new String(result.getValue("wiki".getBytes(), "plaintext".getBytes()));

		// Reduce the length of the text.
		// XXX: HAX
		int length = articleText.length();
		if (prefixLength >= 0 && length > prefixLength) {
			length = prefixLength;
		}
		articleText = articleText.substring(0, length);
		// articleText = "Jackdaws love my big sphinx on quartz.";

		Put put = new Put(rowkey.get());
		String xml = corenlpInterface.getXML(articleText);
		put.add("wiki".getBytes(), "corenlp_xml".getBytes(), xml.getBytes());
		// put.add("wiki".getBytes(), "corenlp_xml".getBytes(), articleText.getBytes());
		// context.write(key, new Text(xml));
		context.write(null, put);
	}
}
