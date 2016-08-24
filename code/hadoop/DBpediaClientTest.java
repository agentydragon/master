import java.lang.System;
import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class DBpediaClientTest {
	@Test
	public void testDbpediaUriToWikidataId() throws Exception {
		String wikidataId = DBpediaClient.dbpediaUriToWikidataId("http://dbpedia.org/resource/Barack_Obama");
		System.out.println("[" + wikidataId + "]");
		assertEquals("Q76", wikidataId);
	}
}
