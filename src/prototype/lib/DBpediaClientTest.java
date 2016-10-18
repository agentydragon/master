import java.lang.System;
import java.util.*;
import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class DBpediaClientTest {
	@Test
	public void testDbpediaUriToWikidataId() throws Exception {
		DBpediaClient client = new DBpediaClient("http://hador:3030/merged/query");

		String wikidataId = client.dbpediaUriToWikidataId("http://dbpedia.org/resource/Barack_Obama");
		System.out.println("[" + wikidataId + "]");
		assertEquals("Q76", wikidataId);

		Map<String, String> result = client.dbpediaUrisToWikidataIds(Arrays.asList("http://dbpedia.org/resource/Barack_Obama"));
		assertEquals("Q76", result.get("http://dbpedia.org/resource/Barack_Obama"));
	}
}
