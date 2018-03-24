// package com.example.cloud.bigtable.helloworld;

import com.google.cloud.bigtable.hbase.BigtableConfiguration;

import com.google.cloud.ReadChannel;
import com.google.cloud.storage.Blob;
import com.google.cloud.storage.BlobId;
import com.google.cloud.storage.Bucket;
import com.google.cloud.storage.BucketInfo;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import info.bliki.wiki.dump.IArticleFilter;
import info.bliki.wiki.dump.Siteinfo;
import info.bliki.wiki.dump.WikiArticle;
import info.bliki.wiki.dump.WikiXMLParser;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintStream;
import java.io.Reader;
import java.nio.ByteBuffer;
import java.nio.channels.Channels;
import java.nio.channels.WritableByteChannel;
import org.apache.commons.compress.compressors.bzip2.BZip2CompressorInputStream;
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

public class SplitToArticles {
  private static void print(String msg) {
    System.out.println("HelloWorld: " + msg);
  }

  private static final byte[] COLUMN_FAMILY_NAME = Bytes.toBytes("wiki");
  private static final String PROJECT_ID = "extended-atrium-198523";
  private static final String INSTANCE_ID = "wiki-articles";

  static class WriteToBigtableArticleFilter implements IArticleFilter {
    private Table table;
    private int articlesProcessed = 0;

    private static final byte[] WIKITEXT_COLUMN = Bytes.toBytes("wikitext");
    private static final byte[] TITLE_COLUMN = Bytes.toBytes("title");

    public WriteToBigtableArticleFilter(Table table) {
      this.table = table;
    }

    public void process(WikiArticle page, Siteinfo info) {
      articlesProcessed++;
      System.out.println("Writing article " + articlesProcessed + ": " + page.getTitle());
      // Write the article into the Bigtable. Its rowkey is its title.
      Put put = new Put(Bytes.toBytes(page.getTitle()));
      put.addColumn(COLUMN_FAMILY_NAME, WIKITEXT_COLUMN,
		    Bytes.toBytes(page.getText()));
      put.addColumn(COLUMN_FAMILY_NAME, TITLE_COLUMN,
                    Bytes.toBytes(page.getTitle()));
      try {
        table.put(put);
      } catch (IOException e) {
	print("io exception while writing " + page.getTitle());
	System.exit(1);
      }
    }
  }

  private static final byte[] TABLE_NAME = Bytes.toBytes("wiki-articles");

  private static void createTable(Connection connection) throws IOException {
    Admin admin = connection.getAdmin();
    HTableDescriptor descriptor = new HTableDescriptor(
      TableName.valueOf(TABLE_NAME));
    descriptor.addFamily(new HColumnDescriptor(COLUMN_FAMILY_NAME));
    print("Create table " + descriptor.getNameAsString());
    admin.createTable(descriptor);
  }

  private static void addArticles(Connection connection) throws IOException {
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

    Table table = connection.getTable(TableName.valueOf(TABLE_NAME));
    //PrintStream writeTo = System.out;
    try (ReadChannel reader = blob.reader()) {
      IArticleFilter handler = new WriteToBigtableArticleFilter(table);
      WikiXMLParser parser = new WikiXMLParser(
        new BZip2CompressorInputStream(
          Channels.newInputStream(reader), true), handler);
      parser.parse();

      //WritableByteChannel channel = Channels.newChannel(writeTo);
      //ByteBuffer bytes = ByteBuffer.allocate(1024);
      //while (reader.read(bytes) > 0) {
      //  bytes.flip();
      //  channel.write(bytes);
      //  bytes.clear();
      //  break;  // print just first 1024 bytes to show we can do that.
      //}
    } catch (IOException e) {
      print("io exception");
      System.exit(1);
    } catch (Exception e) {
      print("exception");
      System.exit(1);
    }
  }

  public static void main(String[] args) {
    try (Connection connection = BigtableConfiguration.connect(PROJECT_ID, INSTANCE_ID)) {
      // NOTE: Uncomment to create the bigtable.
      // createTable(connection);
      addArticles(connection);
    } catch (IOException e) {
      print("io exception");
      System.exit(1);
    }
  }
}
