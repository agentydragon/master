package com.agentydragon.master;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import org.apache.beam.sdk.metrics.Counter;
import org.apache.beam.sdk.metrics.Distribution;
import org.apache.beam.sdk.metrics.Metrics;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.values.KV;
import org.apache.http.BasicNameValuePair;
import org.apache.http.EntityUtils;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.HttpClients;

class AnnotateWithDBpediaSpotlightServiceFn extends DoFn<KV<byte[], String>, KV<byte[], byte[]>> {
  private static final long serialVersionUID = 1L;
  private Counter nullPlaintextCounter =
      Metrics.counter(AnnotateWithDBpediaSpotlightServiceFn.class, "null-plaintext");
  private Counter nullResponseEntityCounter =
      Metrics.counter(AnnotateWithDBpediaSpotlightServiceFn.class, "null-output-entity");
  private Distribution annotationLatencyDistribution =
      Metrics.distribution(AnnotateWithDBpediaSpotlightServiceFn.class, "annotation-latency");

  @ProcessElement
  public void processElement(DoFn<KV<byte[], String>, KV<byte[], byte[]>>.ProcessContext c)
      throws Exception {
    String plaintext = c.element().getValue();
    if (plaintext == null) {
      nullPlaintextCounter.inc();
      return;
    }
    List<NameValuePair> params = new ArrayList<NameValuePair>(1);
    params.add(new BasicNameValuePair("text", plaintext));
    HttpClient httpClient = HttpClients.createDefault();
    HttpPost httpPost = new HttpPost("http://dbpedia-spotlight-service/annotate");
    Instant start = Instant.now();
    HttpResponse response = httpClient.execute(httpPost);
    long annotationLatencyMillis = Duration.between(start, Instant.now()).toMillis();
    annotationLatencyDistribution.update(annotationLatencyMillis);
    HttpEntity entity = response.getEntity();
    if (entity == null) {
      nullResponseEntityCounter.inc();
      return;
    }
    // TODO: the entity content is ... a string
    c.output(KV.of(c.element().getKey(), EntityUtils.toString(entity).getBytes()));
  }
}
