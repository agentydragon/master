import java.lang.System;
import org.apache.jena.query.Query;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.query.QueryExecutionFactory;
import java.util.*;
import java.util.stream.*;
import java.util.function.*;

public class DBpediaClient {
//	private static Map<String, String> dbpediaUriToWikidataIdCache = TODO;

	private final static String wikidataPrefix = "http://www.wikidata.org/entity/";
	private final static String STANDARD_PREFIXES = "PREFIX wd: <http://www.wikidata.org/entity/>\n" +
			"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" +
			"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" +
			"\n";

	public static String dbpediaUriToWikidataId(String uri) {
		// TODO: load cache
		String queryString = STANDARD_PREFIXES +
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

	public static Map<String, String> dbpediaUrisToWikidataIds(List<String> uris) {
		uris = new ArrayList<>(new HashSet<>(uris));
		// TODO: sort?

		List<String> toFetch = new ArrayList<>();
		Map<String, String> result = new HashMap<>();
		// TODO: cache up.
		for (String uri : uris) {
		    //if uri in self.dbpedia_to_wikidata_cache:
		    //	result[uri] = self.dbpedia_to_wikidata_cache[uri]
		    //   else:
			toFetch.add(uri);
		}

		int batch_size = 100;
		for (int i = 0; i < toFetch.size(); i += batch_size) {
			int end = i + batch_size;
			if (end > toFetch.size()) {
				end = toFetch.size();
			}
			List<String> uriBatch = toFetch.subList(i, end);

			// TODO: use prefixes here
			String urisList = uriBatch.stream().map(s -> "<" + s + ">").collect(Collectors.joining(" "));
			String queryString = STANDARD_PREFIXES +
				"SELECT ?entity ?same WHERE { " +
					"VALUES ?entity { " + urisList + " } " +
					"?entity owl:sameAs ?same . " +
				"}";
			Query query = QueryFactory.create(queryString);
			try (QueryExecution execution = QueryExecutionFactory.sparqlService("http://dbpedia.org/sparql", query)) {
				ResultSet results = execution.execSelect();
				while (results.hasNext()) {
					QuerySolution soln = results.nextSolution();
					Resource entity = soln.getResource("entity");
					Resource same = soln.getResource("same");
					if (!entity.isAnon() && !same.isAnon()) {
						String entityUri = entity.getURI();
						String sameUri = same.getURI();
						if (sameUri.startsWith(wikidataPrefix)) {
							String wikidataId = sameUri.substring(wikidataPrefix.length());
							result.put(entityUri, wikidataId);
							// TODO: and cache
						}
					}
				}
			}
		}
		return result;
	}
}
