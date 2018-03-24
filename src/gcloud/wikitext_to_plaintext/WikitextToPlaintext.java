import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.Read;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.transforms.Count;
import org.apache.beam.sdk.values.KV;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Mutation;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.util.Bytes;
import java.nio.charset.StandardCharsets;
// import org.apache.hadoop.hbase.filter.FirstKeyOnlyFilter;

import com.google.cloud.bigtable.beam.CloudBigtableIO;
import com.google.cloud.bigtable.beam.CloudBigtableScanConfiguration;
import com.google.cloud.bigtable.beam.CloudBigtableTableConfiguration;


public class WikitextToPlaintext {
  private static final byte[] COLUMN_FAMILY_NAME = Bytes.toBytes("wiki");
  private static final byte[] PLAINTEXT_COLUMN = Bytes.toBytes("plaintext");
  private static final String PROJECT_ID = "extended-atrium-198523";
  private static final String INSTANCE_ID = "wiki-articles";
  private static final String TABLE_NAME = "wiki-articles";
  private static final byte[] WIKITEXT_COLUMN = Bytes.toBytes("wikitext");

  static final DoFn<Result, KV<byte[], String>> ROW_RESULT_TO_WIKITEXT = new DoFn<Result, KV<byte[], String>>() {
    private static final long serialVersionUID = 1L;

    @ProcessElement
    public void processElement(DoFn<Result, KV<byte[], String>>.ProcessContext c) throws Exception {
      c.output(KV.of(c.element().getRow(),
		new String(c.element().getColumnLatestCell(COLUMN_FAMILY_NAME, WIKITEXT_COLUMN).getValueArray(), StandardCharsets.UTF_8)));
    }
  };

  static final DoFn<KV<byte[], String>, KV<byte[], String>> WIKITEXT_TO_PLAINTEXT = new DoFn<KV<byte[], String>, KV<byte[], String>>() {
    private static final long serialVersionUID = 1L;

    @ProcessElement
    public void processElement(DoFn<KV<byte[], String>, KV<byte[], String>>.ProcessContext c) throws Exception {
      c.output(KV.of(c.element().getKey(), "<plaintext - TODO>"));
    }
  };

  static final DoFn<KV<byte[], String>, Mutation> WRITE_PLAINTEXT = new DoFn<KV<byte[], String>, Mutation>() {
    private static final long serialVersionUID = 1L;

    @ProcessElement
    public void processElement(DoFn<KV<byte[], String>, Mutation>.ProcessContext c) throws Exception {
      c.output(new Put(c.element().getKey()).addColumn(COLUMN_FAMILY_NAME, PLAINTEXT_COLUMN,
          c.element().getValue().getBytes()));
    }
  };

  public static void main(String[] args) {
    CloudBigtableTableConfiguration config_write = new CloudBigtableTableConfiguration.Builder()
        .withProjectId(PROJECT_ID)
        .withInstanceId(INSTANCE_ID)
        .withTableId(TABLE_NAME)
        .build();

    Scan scan = new Scan();
    scan.addColumn(COLUMN_FAMILY_NAME, WIKITEXT_COLUMN);
    // TODO: will this return just the last version...? if not, how to only
    // return the last version?
    // scan.setFilter(new FirstKeyOnlyFilter());
    CloudBigtableScanConfiguration config = new CloudBigtableScanConfiguration.Builder()
        .withProjectId(PROJECT_ID)
        .withInstanceId(INSTANCE_ID)
        .withTableId(TABLE_NAME)
        .withScan(scan)
        .build();

    PipelineOptions options = PipelineOptionsFactory.fromArgs(args).withValidation().as(PipelineOptions.class);
    Pipeline p = Pipeline.create(options);
    p.apply(Read.from(CloudBigtableIO.read(config)))
        .apply(ParDo.of(ROW_RESULT_TO_WIKITEXT))
        .apply(ParDo.of(WIKITEXT_TO_PLAINTEXT))
        .apply(ParDo.of(WRITE_PLAINTEXT))
        .apply(CloudBigtableIO.writeToTable(config_write));

    p.run().waitUntilFinish();
  }
}
