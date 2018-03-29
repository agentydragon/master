package com.agentydragon.master;

import com.google.cloud.bigtable.beam.CloudBigtableIO;
import com.google.cloud.bigtable.beam.CloudBigtableScanConfiguration;
import com.google.cloud.bigtable.beam.CloudBigtableTableConfiguration;
import java.nio.charset.StandardCharsets;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.Read;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.KV;
import org.apache.hadoop.hbase.client.Mutation;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;

public class CoreNLPOnArticles {
  static class RowResultToPlaintextFn extends DoFn<Result, KV<byte[], String>> {
    private static final long serialVersionUID = 1L;

    @ProcessElement
    public void processElement(DoFn<Result, KV<byte[], String>>.ProcessContext c) throws Exception {
      byte[] plaintextBytes =
          c.element()
              .getColumnLatestCell(
                  WikiArticlesBigtable.COLUMN_FAMILY_NAME, WikiArticlesBigtable.PLAINTEXT_COLUMN)
              .getValueArray();
      String plaintext = new String(plaintextBytes, StandardCharsets.UTF_8);
      c.output(KV.of(c.element().getRow(), plaintext));
    }
  };

  static class WriteAnnotationProtoFn extends DoFn<KV<byte[], byte[]>, Mutation> {
    private static final long serialVersionUID = 1L;

    @ProcessElement
    public void processElement(DoFn<KV<byte[], byte[]>, Mutation>.ProcessContext c)
        throws Exception {
      c.output(
          new Put(c.element().getKey())
              .addColumn(
                  WikiArticlesBigtable.COLUMN_FAMILY_NAME,
                  WikiArticlesBigtable.CORENLP_ANNOTATION_PROTO_COLUMN,
                  c.element().getValue()));
    }
  }

  public static void main(String[] args) {
    CloudBigtableTableConfiguration config_write =
        WikiArticlesBigtable.CreateConfigurationBuilder().build();

    Scan scan = new Scan();
    scan.addColumn(WikiArticlesBigtable.COLUMN_FAMILY_NAME, WikiArticlesBigtable.PLAINTEXT_COLUMN);
    // TODO: will this return just the last version...? if not, how to only
    // return the last version?
    // scan.setFilter(new FirstKeyOnlyFilter());
    CloudBigtableScanConfiguration config =
        WikiArticlesBigtable.CreateScanConfigurationBuilder().withScan(scan).build();

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
