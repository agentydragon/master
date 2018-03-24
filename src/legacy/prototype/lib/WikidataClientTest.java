import java.util.List;
import java.lang.System;
import org.junit.Test;

public class WikidataClientTest {
	// TODO: Actually test something!
	@Test
	public void testTripleFetch() throws Exception {
		String id = "Q76";  // Obama
		WikidataClient client = new WikidataClient(WikidataClient.WIKIDATA_PUBLIC_ENDPOINT);
		List<WikidataClient.Triple> triples = client.getAllTriplesOfEntity(id);
		for (WikidataClient.Triple triple : triples) {
			System.out.println(triple.subject + "\t" + triple.relation + "\t" + triple.object);
		}
	}
}
