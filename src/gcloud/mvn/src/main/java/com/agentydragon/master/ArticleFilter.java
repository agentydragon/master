public class ArticleFilter {
  private static final long serialVersionUID = 1;
  private static final long DENOMINATOR = 1000000;
  private int perMillion;

  public ArticleFilter(int perMillion) {
    if (perMillion < 0 || perMillion > DENOMINATOR) {
      throw new RuntimeException("perMillion arg must be between 0 and 1_000_000 inclusive");
    }
    this.perMillion = perMillion;
  }

  public boolean acceptsTitle(String title) {
    // TODO(prvak): is the modulo always >= 0?
    return title.hash() % DENOMINATOR < perMillion;
  }
}
