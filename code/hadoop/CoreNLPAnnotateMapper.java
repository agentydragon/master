import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Mapper;

public class CoreNLPAnnotateMapper extends Mapper<Text, Text, Text, Text>{
	private int prefixLength;
	private CoreNLPInterface corenlpInterface = new CoreNLPInterface();

	@Override
	public void setup(Context context) {
		Configuration conf = context.getConfiguration();
		prefixLength = conf.getInt("prefix_length", 10);
		corenlpInterface.setup();
	}

	@Override
	public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
		String articleTitle = key.toString();
		String articleText = value.toString();

		// Reduce the length of the text.
		// XXX: HAX
		int length = articleText.length();
		if (length > prefixLength) {
			length = prefixLength;
		}
		articleText = articleText.substring(0, length);
		// articleText = "Jackdaws love my big sphinx on quartz.";

		context.write(key, new Text(corenlpInterface.getXML(articleText)));
	}
}
