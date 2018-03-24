// package com.example.cloud.bigtable.helloworld;




import com.google.cloud.bigtable.hbase.BigtableConfiguration;

import com.google.cloud.storage.Bucket;
import com.google.cloud.ReadChannel;
import com.google.cloud.storage.BucketInfo;
import com.google.cloud.storage.Blob;
import com.google.cloud.storage.BlobId;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;
import java.nio.ByteBuffer;
import java.nio.channels.Channels;
import java.nio.channels.WritableByteChannel;
import java.io.InputStream;
import java.io.PrintStream;

import java.io.IOException;

/**
 * A minimal application that connects to Cloud Bigtable using the native HBase API
 * and performs some basic operations.
 */
public class SplitToArticles {

  // Refer to table metadata names by byte array in the HBase API
  private static final byte[] TABLE_NAME = Bytes.toBytes("Hello-Bigtable");
  private static final byte[] COLUMN_FAMILY_NAME = Bytes.toBytes("cf1");
  private static final byte[] COLUMN_NAME = Bytes.toBytes("greeting");

  // Write some friendly greetings to Cloud Bigtable
  private static final String[] GREETINGS =
      { "Hello World!", "Hello Cloud Bigtable!", "Hello HBase!" };

  /**
   * Connects to Cloud Bigtable, runs some basic operations and prints the results.
   */
  private static void doHelloWorld(String projectId, String instanceId) {

    // [START connecting_to_bigtable]
    // Create the Bigtable connection, use try-with-resources to make sure it gets closed
    try (Connection connection = BigtableConfiguration.connect(projectId, instanceId)) {

      // The admin API lets us create, manage and delete tables
      Admin admin = connection.getAdmin();
      // [END connecting_to_bigtable]

      // [START creating_a_table]
      // Create a table with a single column family
      HTableDescriptor descriptor = new HTableDescriptor(TableName.valueOf(TABLE_NAME));
      descriptor.addFamily(new HColumnDescriptor(COLUMN_FAMILY_NAME));

      print("Create table " + descriptor.getNameAsString());
      admin.createTable(descriptor);
      // [END creating_a_table]

      // [START writing_rows]
      // Retrieve the table we just created so we can do some reads and writes
      Table table = connection.getTable(TableName.valueOf(TABLE_NAME));

      // Write some rows to the table
      print("Write some greetings to the table");
      for (int i = 0; i < GREETINGS.length; i++) {
        // Each row has a unique row key.
        //
        // Note: This example uses sequential numeric IDs for simplicity, but
        // this can result in poor performance in a production application.
        // Since rows are stored in sorted order by key, sequential keys can
        // result in poor distribution of operations across nodes.
        //
        // For more information about how to design a Bigtable schema for the
        // best performance, see the documentation:
        //
        //     https://cloud.google.com/bigtable/docs/schema-design
        String rowKey = "greeting" + i;

        // Put a single row into the table. We could also pass a list of Puts to write a batch.
        Put put = new Put(Bytes.toBytes(rowKey));
        put.addColumn(COLUMN_FAMILY_NAME, COLUMN_NAME, Bytes.toBytes(GREETINGS[i]));
        table.put(put);
      }
      // [END writing_rows]

      // [START getting_a_row]
      // Get the first greeting by row key
      String rowKey = "greeting0";
      Result getResult = table.get(new Get(Bytes.toBytes(rowKey)));
      String greeting = Bytes.toString(getResult.getValue(COLUMN_FAMILY_NAME, COLUMN_NAME));
      System.out.println("Get a single greeting by row key");
      System.out.printf("\t%s = %s\n", rowKey, greeting);
      // [END getting_a_row]

      // [START scanning_all_rows]
      // Now scan across all rows.
      Scan scan = new Scan();

      print("Scan for all greetings:");
      ResultScanner scanner = table.getScanner(scan);
      for (Result row : scanner) {
        byte[] valueBytes = row.getValue(COLUMN_FAMILY_NAME, COLUMN_NAME);
        System.out.println('\t' + Bytes.toString(valueBytes));
      }
      // [END scanning_all_rows]

      // [START deleting_a_table]
      // Clean up by disabling and then deleting the table
      print("Delete the table");
      admin.disableTable(table.getName());
      admin.deleteTable(table.getName());
      // [END deleting_a_table]

    } catch (IOException e) {
      System.err.println("Exception while running HelloWorld: " + e.getMessage());
      e.printStackTrace();
      System.exit(1);
    }

    System.exit(0);
  }

  private static void print(String msg) {
    System.out.println("HelloWorld: " + msg);
  }

  public static void main(String[] args) {
    Storage store = StorageOptions.getDefaultInstance().getService();
    String bucketName = "agentydragon-gspython";
    BlobId blobId = BlobId.of(
	    bucketName,
	    "wiki-dumps/enwiki/20180301/enwiki-20180301-pages-articles.xml.bz2");
    Blob blob = store.get(blobId);
    if (blob == null) {
      print("Did not find blob.");
      return;
    }
    PrintStream writeTo = System.out;
    try (ReadChannel reader = blob.reader()) {
      WritableByteChannel channel = Channels.newChannel(writeTo);
      ByteBuffer bytes = ByteBuffer.allocate(1024);
      while (reader.read(bytes) > 0) {
        bytes.flip();
	channel.write(bytes);
        bytes.clear();
	break;  // print just first 1024 bytes to show we can do that.
      }
    } catch (IOException e) {
      print("io exception");
      return;
    }

    // Consult system properties to get project/instance
    String projectId = requiredProperty("bigtable.projectID");
    String instanceId = requiredProperty("bigtable.instanceID");

    doHelloWorld(projectId, instanceId);
  }

  private static String requiredProperty(String prop) {
    String value = System.getProperty(prop);
    if (value == null) {
      throw new IllegalArgumentException("Missing required system property: " + prop);
    }
    return value;
  }

}
