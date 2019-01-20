package com.agentydragon.master;
// -Dinput_file=...

import info.bliki.wiki.dump.IArticleFilter;
import info.bliki.wiki.dump.Siteinfo;
import info.bliki.wiki.dump.WikiArticle;
import info.bliki.wiki.dump.WikiXMLParser;
import info.bliki.wiki.filter.PlainTextConverter;
import info.bliki.wiki.model.WikiModel;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Duration;
import java.time.Instant;
import org.apache.commons.compress.compressors.bzip2.BZip2CompressorInputStream;
import org.xml.sax.SAXException;

public class LocalSplitAndPlaintextConversion {
  private static WikiModel wikiModel;
  private static PlainTextConverter converter;

  static class MyArticleFilter implements IArticleFilter {
    private Instant processingStart;
    private int articlesProcessed = 0;
    private Instant lastLog;

    public MyArticleFilter() {
      processingStart = Instant.now();
      lastLog = Instant.MIN;
    }

    // Log every minute.
    private static final Duration LOG_EVERY_DURATION = Duration.ofMinutes(1);

    private double getSpeedInArticlesPerSec() {
      Duration timeElapsed = Duration.between(processingStart, Instant.now());
      double secondsElapsed = timeElapsed.toMillis() / 1000;
      return ((double) articlesProcessed) / secondsElapsed;
    }

    private void logStats() {
      lastLog = Instant.now();
      double articlesPerSec = getSpeedInArticlesPerSec();
      System.out.printf("Speed: %.2f articles/s\n", articlesPerSec);
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
      // Write the article into the Bigtable. Its rowkey is its title.
      String title = page.getTitle();
      String wikiText = page.getText();
      if (title == null) {
        System.out.println("Article with null title detected, and will be skipped. Body:");
        System.out.println(wikiText == null ? "NULL" : wikiText);
        return;
      }
      if (wikiText == null) {
        System.out.println("Article with null text detected, and will be skipped. Title: " + title);
        return;
      }
      try {
        String plaintext = wikiModel.render(converter, wikiText);
        // Some articles in the dataset have null titles or texts, for some
        // reason. Make sure we don't crash on those (by calling
        // Bytes.toBytes on null).
        String path = title + ".txt";
        try (PrintWriter out = new PrintWriter(path)) {
          out.print(plaintext);
        }
      } catch (IOException e) {
        e.printStackTrace();
        System.exit(1);
      }
      if (articlesProcessed > 10) {
        System.out.println(title);
        System.exit(0);
      }
    }
  }

  private static void addArticles() throws IOException {
    InputStream inputStream =
        Files.newInputStream(
            Paths.get(
                "/home/agentydragon/repos/master/2019-01-19/"
                    + "enwiki-20190101-pages-articles1.xml-p10p30302.bz2")
            // System.getProperty("input_file")
            );
    IArticleFilter handler = new MyArticleFilter();
    try {
      WikiXMLParser parser =
          new WikiXMLParser(new BZip2CompressorInputStream(inputStream, true), handler);
      parser.parse();
    } catch (SAXException e) {
      e.printStackTrace();
      System.exit(1);
    }
  }

  public static void main(String[] args) {
    try {
      wikiModel =
          new WikiModel(
              "https://en.wikipedia.org/wiki/${image}", "https://en.wikipedia.org/wiki/${title}");
      converter = new PlainTextConverter();
      // We expect to operate on a huge XML document - disable checks against too
      // large documents.
      // See: https://github.com/dbpedia/extraction-framework/issues/487
      System.setProperty("entityExpansionLimit", "0");
      System.setProperty("totalEntitySizeLimit", "0");
      System.setProperty("jdk.xml.totalEntitySizeLimit", "0");
      addArticles();
    } catch (IOException e) {
      e.printStackTrace();
      System.exit(1);
    }
  }
}
