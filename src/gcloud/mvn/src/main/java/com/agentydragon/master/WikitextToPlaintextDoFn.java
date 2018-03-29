package com.agentydragon.master;

import info.bliki.wiki.filter.PlainTextConverter;
import info.bliki.wiki.model.WikiModel;
import org.apache.beam.sdk.metrics.Counter;
import org.apache.beam.sdk.metrics.Metrics;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.values.KV;

class WikitextToPlaintextDoFn extends DoFn<KV<byte[], String>, KV<byte[], String>> {
  private static final long serialVersionUID = 1L;
  private transient WikiModel wikiModel;
  private transient PlainTextConverter converter;
  private Counter nullWikitextCounter =
      Metrics.counter(WikitextToPlaintextDoFn.class, "wikitext-to-plaintext-null-wikitext");
  private Counter assertionErrorCounter =
      Metrics.counter(WikitextToPlaintextDoFn.class, "wikitext-to-plaintext-AssertionError");
  private Counter nullPointerExceptionCounter =
      Metrics.counter(WikitextToPlaintextDoFn.class, "wikitext-to-plaintext-NullPointerException");
  private Counter uncaughtExceptionCounter =
      Metrics.counter(WikitextToPlaintextDoFn.class, "wikitext-to-plaintext-uncaught-Exception");

  @Setup
  public void setup() {
    wikiModel =
        new WikiModel(
            "https://en.wikipedia.org/wiki/${image}", "https://en.wikipedia.org/wiki/${title}");
    converter = new PlainTextConverter();
  }

  @ProcessElement
  public void processElement(DoFn<KV<byte[], String>, KV<byte[], String>>.ProcessContext c)
      throws Exception {
    try {
      String wikitext = c.element().getValue();
      if (wikitext == null) {
        nullWikitextCounter.inc();
        System.out.println("Unexpected null wikitext");
        return;
      }
      String plaintext = wikiModel.render(converter, wikitext);
      c.output(KV.of(c.element().getKey(), plaintext));
    } catch (AssertionError e) {
      e.printStackTrace();
      assertionErrorCounter.inc();
    } catch (NullPointerException e) {
      e.printStackTrace();
      nullPointerExceptionCounter.inc();
    } catch (Exception e) {
      e.printStackTrace();
      uncaughtExceptionCounter.inc();
    }
  }
}
