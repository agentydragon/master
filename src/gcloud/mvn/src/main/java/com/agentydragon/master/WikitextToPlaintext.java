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

public class WikitextToPlaintext {
  static final DoFn<Result, KV<byte[], String>> ROW_RESULT_TO_WIKITEXT =
      new DoFn<Result, KV<byte[], String>>() {
        private static final long serialVersionUID = 1L;

        @ProcessElement
        public void processElement(DoFn<Result, KV<byte[], String>>.ProcessContext c)
            throws Exception {
          byte[] wikitextBytes =
              c.element()
                  .getColumnLatestCell(
                      WikiArticlesBigtable.COLUMN_FAMILY_NAME, WikiArticlesBigtable.WIKITEXT_COLUMN)
                  .getValueArray();
          String wikitext = new String(wikitextBytes, StandardCharsets.UTF_8);
          c.output(KV.of(c.element().getRow(), wikitext));
        }
      };

  static final DoFn<KV<byte[], String>, Mutation> WRITE_PLAINTEXT =
      new DoFn<KV<byte[], String>, Mutation>() {
        private static final long serialVersionUID = 1L;

        @ProcessElement
        public void processElement(DoFn<KV<byte[], String>, Mutation>.ProcessContext c)
            throws Exception {
          c.output(
              new Put(c.element().getKey())
                  .addColumn(
                      WikiArticlesBigtable.COLUMN_FAMILY_NAME,
                      WikiArticlesBigtable.PLAINTEXT_COLUMN,
                      c.element().getValue().getBytes()));
        }
      };

  public static void main(String[] args) {
    CloudBigtableTableConfiguration config_write =
        WikiArticlesBigtable.CreateConfigurationBuilder().build();

    Scan scan = new Scan();
    scan.addColumn(WikiArticlesBigtable.COLUMN_FAMILY_NAME, WikiArticlesBigtable.WIKITEXT_COLUMN);
    // TODO: will this return just the last version...? if not, how to only
    // return the last version?
    // scan.setFilter(new FirstKeyOnlyFilter());
    CloudBigtableScanConfiguration config =
        WikiArticlesBigtable.CreateScanConfigurationBuilder().withScan(scan).build();

    PipelineOptions options =
        PipelineOptionsFactory.fromArgs(args).withValidation().as(PipelineOptions.class);
    Pipeline p = Pipeline.create(options);
    p.apply(Read.from(CloudBigtableIO.read(config)))
        .apply(ParDo.of(ROW_RESULT_TO_WIKITEXT))
        .apply(ParDo.of(new WikitextToPlaintextDoFn()))
        .apply(ParDo.of(WRITE_PLAINTEXT))
        .apply(CloudBigtableIO.writeToTable(config_write));

    p.run().waitUntilFinish();
  }
}
