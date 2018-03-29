package com.agentydragon.master;

import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.CoreNLPProtos;
import edu.stanford.nlp.pipeline.ProtobufAnnotationSerializer;
import edu.stanford.nlp.pipeline.StanfordCoreNLPClient;
import java.time.Duration;
import java.time.Instant;
import java.util.Properties;
import org.apache.beam.sdk.metrics.Counter;
import org.apache.beam.sdk.metrics.Distribution;
import org.apache.beam.sdk.metrics.Metrics;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.values.KV;

class ParseWithCoreNLPServiceFn extends DoFn<KV<byte[], String>, KV<byte[], byte[]>> {
  private static final long serialVersionUID = 1L;
  private transient StanfordCoreNLPClient client;
  private Counter nullPlaintextCounter =
      Metrics.counter(ParseWithCoreNLPServiceFn.class, "parse-with-corenlp-service-null-plaintext");
  private Distribution annotationLatencyDistribution =
      Metrics.distribution(
          ParseWithCoreNLPServiceFn.class, "parse-with-corenlp-annotation-latency");
  private static final int THREADS_PER_WORKER = 4;

  @Setup
  public void setup() {
    Properties props = new Properties();
    // TODO: run parse, dcoref when we're ready.
    props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
    // props.setProperty("annotators", "tokenize");
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
