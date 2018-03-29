package com.agentydragon.master;

import com.google.cloud.bigtable.beam.CloudBigtableScanConfiguration;
import com.google.cloud.bigtable.beam.CloudBigtableTableConfiguration;
import org.apache.hadoop.hbase.util.Bytes;

abstract class WikiArticlesBigtable {
  public static final byte[] COLUMN_FAMILY_NAME = Bytes.toBytes("wiki");
  public static final byte[] PLAINTEXT_COLUMN = Bytes.toBytes("plaintext");
  public static final String PROJECT_ID = "extended-atrium-198523";
  public static final String INSTANCE_ID = "wiki-articles";
  public static final String TABLE_NAME = "wiki-articles";
  public static final byte[] WIKITEXT_COLUMN = Bytes.toBytes("wikitext");
  public static final byte[] CORENLP_ANNOTATION_PROTO_COLUMN =
      Bytes.toBytes("corenlp_annotation_proto");

  public static CloudBigtableTableConfiguration.Builder CreateConfigurationBuilder() {
    return new CloudBigtableTableConfiguration.Builder()
        .withProjectId(WikiArticlesBigtable.PROJECT_ID)
        .withInstanceId(WikiArticlesBigtable.INSTANCE_ID)
        .withTableId(WikiArticlesBigtable.TABLE_NAME);
  }

  public static CloudBigtableScanConfiguration.Builder CreateScanConfigurationBuilder() {
    return new CloudBigtableScanConfiguration.Builder()
        .withProjectId(PROJECT_ID)
        .withInstanceId(INSTANCE_ID)
        .withTableId(TABLE_NAME);
  }
};
