import java.io.IOException;
import java.lang.IllegalArgumentException;

import org.apache.hadoop.fs.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.*;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.hbase.mapreduce.TableMapper;

public class CoreNLPAnnotateMapper extends TableMapper<ImmutableBytesWritable, Put>{
	private int prefixLength;
	private CoreNLPInterface corenlpInterface = new CoreNLPInterface();

	private Set<String> whitelist = new HashSet<>();
	private void loadWhitelist(Configuration conf) {
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

	@Override
	public void setup(Context context) {
		Configuration conf = context.getConfiguration();
		prefixLength = conf.getInt("prefix_length", 10);
		corenlpInterface.setup();

		loadWhitelist(conf);
	}

	@Override
	public void map(ImmutableBytesWritable rowkey, Result result, Context context) throws IOException, InterruptedException {
		String articleTitle = new String(rowkey.get());
		String articleText = new String(result.getValue(ArticlesTable.WIKI, ArticlesTable.PLAINTEXT));

		if (!whitelist.contains(articleTitle)) {
			return;
		}

		// Reduce the length of the text.
		// XXX: HAX
		int length = articleText.length();
		if (prefixLength >= 0 && length > prefixLength) {
			length = prefixLength;
		}
		articleText = articleText.substring(0, length);

		try {
			Put put = new Put(rowkey.get());
			String xml = corenlpInterface.getXML(articleText);
			put.add(ArticlesTable.WIKI, ArticlesTable.CORENLP_XML, xml.getBytes());
			context.write(null, put);
		} catch (IllegalArgumentException e) {
			/**
				2016-10-13 13:42:12,160 INFO [AsyncDispatcher event handler] org.apache.hadoop.mapreduce.v2.app.job.impl.TaskAttemptImpl: Diagnostics report from attempt_1469474050624_0453_m_000015_1: Error: java.lang.IllegalArgumentException
					at edu.stanford.nlp.semgraph.SemanticGraph.parentPairs(SemanticGraph.java:699)
					at edu.stanford.nlp.semgraph.semgrex.GraphRelation$DEPENDENT$1.advance(GraphRelation.java:324)
					at edu.stanford.nlp.semgraph.semgrex.GraphRelation$SearchNodeIterator.initialize(GraphRelation.java:1102)
					at edu.stanford.nlp.semgraph.semgrex.GraphRelation$SearchNodeIterator.<init>(GraphRelation.java:1083)
					at edu.stanford.nlp.semgraph.semgrex.GraphRelation$DEPENDENT$1.<init>(GraphRelation.java:309)
					at edu.stanford.nlp.semgraph.semgrex.GraphRelation$DEPENDENT.searchNodeIterator(GraphRelation.java:309)
					at edu.stanford.nlp.semgraph.semgrex.NodePattern$NodeMatcher.resetChildIter(NodePattern.java:320)
					at edu.stanford.nlp.semgraph.semgrex.NodePattern$NodeMatcher.<init>(NodePattern.java:315)
					at edu.stanford.nlp.semgraph.semgrex.NodePattern.matcher(NodePattern.java:276)
					at edu.stanford.nlp.semgraph.semgrex.CoordinationPattern$CoordinationMatcher.<init>(CoordinationPattern.java:147)
					at edu.stanford.nlp.semgraph.semgrex.CoordinationPattern.matcher(CoordinationPattern.java:121)
					at edu.stanford.nlp.semgraph.semgrex.NodePattern$NodeMatcher.resetChild(NodePattern.java:339)
					at edu.stanford.nlp.semgraph.semgrex.NodePattern$NodeMatcher.goToNextNodeMatch(NodePattern.java:438)
					at edu.stanford.nlp.semgraph.semgrex.NodePattern$NodeMatcher.matches(NodePattern.java:555)
					at edu.stanford.nlp.semgraph.semgrex.SemgrexMatcher.find(SemgrexMatcher.java:182)
					at edu.stanford.nlp.dcoref.Mention.findDependentVerb(Mention.java:1068)
					at edu.stanford.nlp.dcoref.Mention.setDiscourse(Mention.java:319)
					at edu.stanford.nlp.dcoref.Mention.process(Mention.java:237)
					at edu.stanford.nlp.dcoref.Mention.process(Mention.java:244)
					at edu.stanford.nlp.dcoref.MentionExtractor.arrange(MentionExtractor.java:215)
					at edu.stanford.nlp.dcoref.MentionExtractor.arrange(MentionExtractor.java:133)
					at edu.stanford.nlp.dcoref.MentionExtractor.arrange(MentionExtractor.java:108)
					at edu.stanford.nlp.pipeline.DeterministicCorefAnnotator.annotate(DeterministicCorefAnnotator.java:120)
					at edu.stanford.nlp.pipeline.AnnotationPipeline.annotate(AnnotationPipeline.java:71)
					at edu.stanford.nlp.pipeline.StanfordCoreNLP.annotate(StanfordCoreNLP.java:499)
					at CoreNLPInterface.getXML(CoreNLPInterface.java:32)
					at CoreNLPAnnotateMapper.map(CoreNLPAnnotateMapper.java:42)
					at CoreNLPAnnotateMapper.map(CoreNLPAnnotateMapper.java:16)
					at org.apache.hadoop.mapreduce.Mapper.run(Mapper.java:145)
					at org.apache.hadoop.mapred.MapTask.runNewMapper(MapTask.java:787)
					at org.apache.hadoop.mapred.MapTask.run(MapTask.java:341)
					at org.apache.hadoop.mapred.YarnChild$2.run(YarnChild.java:164)
					at java.security.AccessController.doPrivileged(Native Method)
					at javax.security.auth.Subject.doAs(Subject.java:422)
					at org.apache.hadoop.security.UserGroupInformation.doAs(UserGroupInformation.java:1693)
					at org.apache.hadoop.mapred.YarnChild.main(YarnChild.java:158)
			*/
			// TODO: log it and which article is it
			// TODO: count it
		}
	}
}
