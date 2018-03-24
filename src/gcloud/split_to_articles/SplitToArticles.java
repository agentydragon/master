// package com.example.cloud.bigtable.helloworld;

import com.google.cloud.ReadChannel;
import com.google.cloud.bigtable.hbase.BigtableConfiguration;
import com.google.cloud.storage.Blob;
import com.google.cloud.storage.BlobId;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import info.bliki.wiki.dump.IArticleFilter;
import info.bliki.wiki.dump.Siteinfo;
import info.bliki.wiki.dump.WikiArticle;
import info.bliki.wiki.dump.WikiXMLParser;
import java.io.IOException;
import java.nio.channels.Channels;
import java.time.Duration;
import java.time.Instant;
import org.apache.commons.compress.compressors.bzip2.BZip2CompressorInputStream;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.BufferedMutator;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Put;
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
    private BufferedMutator mutator;
    private Table table;
    private boolean batchMode;

    private Instant processingStart;
    private int articlesProcessed = 0;
    private Instant lastLog;

    private static final byte[] WIKITEXT_COLUMN = Bytes.toBytes("wikitext");
    private static final byte[] TITLE_COLUMN = Bytes.toBytes("title");

    public WriteToBigtableArticleFilter(BufferedMutator mutator, Table table, boolean batchMode) {
      this.mutator = mutator;
      this.table = table;
      this.batchMode = batchMode;
      processingStart = Instant.now();
      lastLog = Instant.MIN;
    }

    // Log every minute.
    private static final Duration LOG_EVERY_DURATION = Duration.ofMinutes(1);

    private double getSpeedInArticlesPerSec() {
      Duration timeElapsed = Duration.between(processingStart, Instant.now());
      double secondsElapsed = timeElapsed.toMillis() / 10000;
      return ((double) articlesProcessed) / secondsElapsed;
    }

    private void logStats() {
      lastLog = Instant.now();
      double articlesPerSec = getSpeedInArticlesPerSec();
      System.out.printf(
          "Speed: %.2f articles/s (%s mode)\n", articlesPerSec, batchMode ? "batch" : "serial");
    }

    private Put createArticlePut(WikiArticle page) {
      // Write the article into the Bigtable. Its rowkey is its title.
      String title = page.getTitle();
      String text = page.getText();
      // Some articles in the dataset have null titles or texts, for some
      // reason. Make sure we don't crash on those (by calling
      // Bytes.toBytes on null).
      if (title == null) {
        System.out.println("Article with null title detected, and will be skipped. Body:");
        System.out.println(text == null ? "NULL" : text);
        return null;
      }
      if (text == null) {
        System.out.println("Article with null text detected, and will be skipped. Title: " + text);
        return null;
      }
      return new Put(Bytes.toBytes(title))
          .addColumn(COLUMN_FAMILY_NAME, WIKITEXT_COLUMN, Bytes.toBytes(text))
          .addColumn(COLUMN_FAMILY_NAME, TITLE_COLUMN, Bytes.toBytes(title));
    }

    private boolean isTimeUpToLogStats() {
      Instant now = Instant.now();
      return Duration.between(lastLog, now).compareTo(LOG_EVERY_DURATION) >= 0;
    }

    public void process(WikiArticle page, Siteinfo info) {
      articlesProcessed++;
      // Log every 1000 ms.
      if (isTimeUpToLogStats()) {
        logStats();
        System.out.printf("Writing article #%d: %s\n", articlesProcessed, page.getTitle());
      }
      Put put = createArticlePut(page);
      if (put == null) {
        System.out.println("null put created, skipping");
        return;
      }
      try {
        if (batchMode) {
          mutator.mutate(put);
        } else {
          table.put(put);
        }
      } catch (IOException e) {
        e.printStackTrace();
        print("io exception while writing " + page.getTitle());
        System.exit(1);
      }
    }
  }

  private static final byte[] TABLE_NAME = Bytes.toBytes("wiki-articles");

  private static void createTable(Connection connection) throws IOException {
    Admin admin = connection.getAdmin();
    HTableDescriptor descriptor = new HTableDescriptor(TableName.valueOf(TABLE_NAME));
    descriptor.addFamily(new HColumnDescriptor(COLUMN_FAMILY_NAME));
    print("Create table " + descriptor.getNameAsString());
    admin.createTable(descriptor);
  }

  private static void addArticles(Connection connection) throws IOException {
    Storage store = StorageOptions.getDefaultInstance().getService();
    String bucketName = "agentydragon-gspython";
    BlobId blobId =
        BlobId.of(bucketName, "wiki-dumps/enwiki/20180301/enwiki-20180301-pages-articles.xml.bz2");
    Blob blob = store.get(blobId);
    if (blob == null) {
      print("Did not find blob.");
      System.exit(1);
    }

    Table table = connection.getTable(TableName.valueOf(TABLE_NAME));
    try (ReadChannel reader = blob.reader()) {
      BufferedMutator mutator = connection.getBufferedMutator(TableName.valueOf(TABLE_NAME));
      print("BufferedMutator write buffer size: " + mutator.getWriteBufferSize() + " B");
      // print("BufferedMutator periodic flush timeout: " +
      // mutator.getWriteBufferPeriodicFlushTimeoutMs() + " ms");
      IArticleFilter handler = new WriteToBigtableArticleFilter(mutator, table, true);
      WikiXMLParser parser =
          new WikiXMLParser(
              new BZip2CompressorInputStream(Channels.newInputStream(reader), true), handler);
      parser.parse();
      mutator.flush();
    } catch (IOException e) {
      e.printStackTrace();
      print("io exception");
      System.exit(1);
    } catch (Exception e) {
      e.printStackTrace();
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
      e.printStackTrace();
      print("io exception");
      System.exit(1);
    }
  }
}
