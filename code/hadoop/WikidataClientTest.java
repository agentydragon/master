import java.util.List;
import java.lang.System;
import org.junit.Test;

public class WikidataClientTest {
	// TODO: Actually test something!
	@Test
	public void testTripleFetch() throws Exception {
		String id = "Q76";  // Obama
		List<WikidataClient.Triple> triples = WikidataClient.getAllTriplesOfEntity(id);
		for (WikidataClient.Triple triple : triples) {
			System.out.println(triple.subject + "\t" + triple.predicate + "\t" + triple.object);
		}
	}
}
