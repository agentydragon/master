import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;
import java.lang.System;
import org.apache.jena.query.Query;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.query.QueryExecutionFactory;

// TODO test

public class WikidataClient {
	private static final String sparqlUrl = "https://query.wikidata.org/sparql";
	// http://localhost:3030/wikidata/query

	public static class Triple {
		public String subject;
		public String predicate;
		public String object;

		public Triple(String subject, String predicate, String object) {
			this.subject = subject;
			this.predicate = predicate;
			this.object = object;
		}
	}

	// TODO: cache

	private static final String PREFIXES = "PREFIX wd: <http://www.wikidata.org/entity/>\n" +
			"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" +
			"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n";

	private static final String wikidataEntityPrefix = "http://www.wikidata.org/entity/";

	private static boolean relationInteresting(String relation) {
		if (Arrays.asList("http://schema.org/description",
					"http://www.w3.org/2004/02/skos/core#altLabel",
					"http://www.w3.org/2000/01/rdf-schema#label").contains(relation)) {
			return false;
		}
		if (!relation.contains("wikidata")) {
			return false;
		}
		return true;
	}

	private static final String propertyPrefix = "http://www.wikidata.org/entity/P";
	private static final String extendedPropertyPrefix = "http://www.wikidata.org/wiki/Property:P";

	private static String normalizeRelation(String relation) {
		if (relation.startsWith(propertyPrefix) && (relation.endsWith("s") || relation.endsWith("c"))) {
			relation = relation.replace(propertyPrefix, extendedPropertyPrefix);
			relation = relation.substring(0, relation.length() - 1);
		}
		return relation;
	}

	private static boolean isStatement(String uri) {
		return uri.startsWith("http://www.wikidata.org/entity/statement/");
	}

	private static boolean isWikidataEntityUrl(String uri) {
		return uri.startsWith(wikidataEntityPrefix);
	}

	private static String wikidataEntityUrlToEntityId(String uri) {
		assert isWikidataEntityUrl(uri);
		return uri.substring(wikidataEntityPrefix.length());
	}

	private static String pp = "http://www.wikidata.org/prop/direct/";
	private static String wikidataPropertyUrlToPropertyId(String uri) {
		assert uri.startsWith(pp);
		return uri.substring(pp.length());
	}

	private static Triple transformRelation(String subject, String predicate, String object) {
		if (!relationInteresting(predicate)) {
			return null;
		}
		predicate = normalizeRelation(predicate);
		if (isStatement(subject) || isStatement(object)) {
			return null;
		}
		if (!subject.contains("/Q") || !object.contains("/Q")) {
			return null;
		}
		if (!predicate.contains("/P")) {
			return null;
		}
		if (!isWikidataEntityUrl(subject) || !isWikidataEntityUrl(object)) {
			return null;
		}
		subject = wikidataEntityUrlToEntityId(subject);
		object = wikidataEntityUrlToEntityId(object);
		predicate = wikidataPropertyUrlToPropertyId(predicate);
		return new Triple(subject, predicate, object);
	}

	public static List<Triple> collectForwardProperties(String wikidataId) {
		String queryString = PREFIXES + "\n" +
			"SELECT ?rel ?other WHERE { wd:" + wikidataId + " ?rel ?other . }";

		String subject = wikidataEntityPrefix + wikidataId;
		List<Triple> resultsx = new ArrayList<>();

		Query query = QueryFactory.create(queryString);
		try (QueryExecution execution = QueryExecutionFactory.sparqlService(sparqlUrl, query)) {
			ResultSet results = execution.execSelect();
			while (results.hasNext()) {
				QuerySolution soln = results.nextSolution();
				RDFNode rn = soln.get("rel");
				RDFNode on = soln.get("other");
				if (!rn.isResource() || !on.isResource()) {
					// (literals)
					continue;
				}
				Resource rel = soln.getResource("rel");
				Resource other = soln.getResource("other");
				if (!rel.isAnon() && !other.isAnon()) {
					Triple triple = transformRelation(subject, rel.getURI(), other.getURI());
					if (triple != null) {
						resultsx.add(triple);
					}
				}
			}
		}
		return resultsx;
	}

	public static List<Triple> collectBackwardProperties(String wikidataId) {
		String queryString = PREFIXES + "\n" +
			"SELECT ?rel ?other WHERE { ?other ?rel wd:" + wikidataId + " . }";

		String object = wikidataEntityPrefix + wikidataId;
		List<Triple> resultsx = new ArrayList<>();

		Query query = QueryFactory.create(queryString);
		try (QueryExecution execution = QueryExecutionFactory.sparqlService(sparqlUrl, query)) {
			ResultSet results = execution.execSelect();
			while (results.hasNext()) {
				QuerySolution soln = results.nextSolution();
				RDFNode rn = soln.get("rel");
				RDFNode on = soln.get("other");
				if (!rn.isResource() || !on.isResource()) {
					// (literals)
					continue;
				}
				Resource rel = soln.getResource("rel");
				Resource other = soln.getResource("other");
				if (!rel.isAnon() && !other.isAnon()) {
					Triple triple = transformRelation(other.getURI(), rel.getURI(), object);
					if (triple != null) {
						resultsx.add(triple);
					}
				}
			}
		}
		return resultsx;
	}

	public static List<Triple> getAllTriplesOfEntity(String wikidataId) {
		ArrayList<Triple> triples = new ArrayList<Triple>();
		triples.addAll(collectForwardProperties(wikidataId));
		triples.addAll(collectBackwardProperties(wikidataId));
		return triples;
	}
}
