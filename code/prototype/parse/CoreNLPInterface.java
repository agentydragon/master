import java.io.IOException;
import java.io.StringWriter;
import java.util.Properties;
import edu.stanford.nlp.io.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.util.*;
import edu.stanford.nlp.ling.*;

public class CoreNLPInterface {
	private StanfordCoreNLP pipeline;

	public void setup() {
		Properties props = new Properties();
		// TODO: MODEL
		props.put("annotators",
				"tokenize,ssplit,pos,parse," +
				"lemma,ner,dcoref");
		props.put("threads", "10");
		// props.put("pos.maxlen", "100");
		// props.put("parse.maxlen", "100");
		props.put("pos.maxlen", "50");
		props.put("parse.maxlen", "50");

		// Use shift-reduce model to parse faster.
		props.put("parse.model", "edu/stanford/nlp/models/srparser/englishSR.ser.gz");
		pipeline = new StanfordCoreNLP(props);
	}

	public String getXML(String text) throws IOException {
		assert pipeline != null;
		assert text != null;

		Annotation annotation = new Annotation(text);
		StringWriter xmlOut = new StringWriter();
		pipeline.annotate(annotation);
		pipeline.xmlPrint(annotation, xmlOut);
		return xmlOut.toString();
	}
}
