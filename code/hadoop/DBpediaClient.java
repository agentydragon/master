import java.lang.System;
import org.apache.jena.query.Query;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.query.QueryExecutionFactory;

public class DBpediaClient {
//	private static Map<String, String> dbpediaUriToWikidataIdCache = TODO;

	private final static String wikidataPrefix = "http://www.wikidata.org/entity/";

	public static String dbpediaUriToWikidataId(String uri) {
		// TODO: load cache
		String queryString = "PREFIX wd: <http://www.wikidata.org/entity/>\n" +
			"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" +
			"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" +
			"\n" +
			"SELECT ?same WHERE { <" + uri + "> owl:sameAs ?same . }";
		Query query = QueryFactory.create(queryString);
		try (QueryExecution execution = QueryExecutionFactory.sparqlService("http://dbpedia.org/sparql", query)) {
			ResultSet results = execution.execSelect();
			while (results.hasNext()) {
				QuerySolution soln = results.nextSolution();
				Resource r = soln.getResource("same");
				if ( ! r.isAnon() ) {
					String sameUri = r.getURI();
					if (sameUri.startsWith(wikidataPrefix)) {
						return sameUri.substring(wikidataPrefix.length());
					}
				}
			}
		}
		return null;
	}
}
