package com.agentydragon.master;

import com.google.cloud.bigtable.beam.CloudBigtableIO;
import com.google.cloud.bigtable.beam.CloudBigtableScanConfiguration;
import com.google.cloud.bigtable.beam.CloudBigtableTableConfiguration;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.CoreNLPProtos;
import edu.stanford.nlp.pipeline.ProtobufAnnotationSerializer;
import edu.stanford.nlp.pipeline.StanfordCoreNLPClient;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.time.Instant;
import java.util.Properties;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.Read;
import org.apache.beam.sdk.metrics.Counter;
import org.apache.beam.sdk.metrics.Distribution;
import org.apache.beam.sdk.metrics.Metrics;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.KV;
import org.apache.hadoop.hbase.client.Mutation;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.util.Bytes;

public class CoreNLPOnArticles {
  private static final byte[] COLUMN_FAMILY_NAME = Bytes.toBytes("wiki");
  private static final byte[] PLAINTEXT_COLUMN = Bytes.toBytes("plaintext");
  private static final byte[] CORENLP_ANNOTATION_PROTO_COLUMN =
      Bytes.toBytes("corenlp_annotation_proto");
  private static final String PROJECT_ID = "extended-atrium-198523";
  private static final String INSTANCE_ID = "wiki-articles";
  private static final String TABLE_NAME = "wiki-articles";

  static class RowResultToPlaintextFn extends DoFn<Result, KV<byte[], String>> {
    private static final long serialVersionUID = 1L;

    @ProcessElement
    public void processElement(DoFn<Result, KV<byte[], String>>.ProcessContext c) throws Exception {
      byte[] plaintextBytes =
          c.element().getColumnLatestCell(COLUMN_FAMILY_NAME, PLAINTEXT_COLUMN).getValueArray();
      String plaintext = new String(plaintextBytes, StandardCharsets.UTF_8);
      c.output(KV.of(c.element().getRow(), plaintext));
    }
  };

  static class ParseWithCoreNLPServiceFn extends DoFn<KV<byte[], String>, KV<byte[], byte[]>> {
    private static final long serialVersionUID = 1L;
    private transient StanfordCoreNLPClient client;
    private Counter nullPlaintextCounter =
        Metrics.counter(
            ParseWithCoreNLPServiceFn.class, "parse-with-corenlp-service-null-plaintext");
    private Distribution annotationLatencyDistribution =
        Metrics.distribution(
            ParseWithCoreNLPServiceFn.class, "parse-with-corenlp-annotation-latency");
    private static final int THREADS_PER_WORKER = 4;

    @Setup
    public void setup() {
      Properties props = new Properties();
      // TODO: run parse, dcoref when we're ready.
      // props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
      props.setProperty("annotators", "tokenize");
      client = new StanfordCoreNLPClient(props, "http://corenlp-service", 9000, THREADS_PER_WORKER);
    }

    @ProcessElement
    public void processElement(DoFn<KV<byte[], String>, KV<byte[], byte[]>>.ProcessContext c)
        throws Exception {
      String plaintext = c.element().getValue();
      if (plaintext == null) {
        nullPlaintextCounter.inc();
        System.out.println("Unexpected null plaintext");
        return;
      }
      Annotation documentAnnotation = new Annotation(plaintext);
      Instant start = Instant.now();
      client.annotate(documentAnnotation);
      long annotationLatencyMillis = Duration.between(start, Instant.now()).toMillis();
      annotationLatencyDistribution.update(annotationLatencyMillis);
      CoreNLPProtos.Document document =
          new ProtobufAnnotationSerializer().toProto(documentAnnotation);
      c.output(KV.of(c.element().getKey(), document.toByteArray()));
    }
  }

  static class WriteAnnotationProtoFn extends DoFn<KV<byte[], byte[]>, Mutation> {
    private static final long serialVersionUID = 1L;

    @ProcessElement
    public void processElement(DoFn<KV<byte[], byte[]>, Mutation>.ProcessContext c)
        throws Exception {
      c.output(
          new Put(c.element().getKey())
              .addColumn(
                  COLUMN_FAMILY_NAME, CORENLP_ANNOTATION_PROTO_COLUMN, c.element().getValue()));
    }
  }

  public static void main(String[] args) {
    CloudBigtableTableConfiguration config_write =
        new CloudBigtableTableConfiguration.Builder()
            .withProjectId(PROJECT_ID)
            .withInstanceId(INSTANCE_ID)
            .withTableId(TABLE_NAME)
            .build();

    Scan scan = new Scan();
    scan.addColumn(COLUMN_FAMILY_NAME, PLAINTEXT_COLUMN);
    // TODO: will this return just the last version...? if not, how to only
    // return the last version?
    // scan.setFilter(new FirstKeyOnlyFilter());
    CloudBigtableScanConfiguration config =
        new CloudBigtableScanConfiguration.Builder()
            .withProjectId(PROJECT_ID)
            .withInstanceId(INSTANCE_ID)
            .withTableId(TABLE_NAME)
            .withScan(scan)
            .build();

    PipelineOptions options =
        PipelineOptionsFactory.fromArgs(args).withValidation().as(PipelineOptions.class);
    Pipeline p = Pipeline.create(options);
    p.apply(Read.from(CloudBigtableIO.read(config)))
        .apply(ParDo.of(new RowResultToPlaintextFn()))
        .apply(ParDo.of(new ParseWithCoreNLPServiceFn()))
        .apply(ParDo.of(new WriteAnnotationProtoFn()))
        .apply(CloudBigtableIO.writeToTable(config_write));

    p.run().waitUntilFinish();
  }
}
