import java.util.List;
import java.util.*;
import org.apache.hadoop.conf.Configuration;
import java.util.stream.*;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
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
	public static String joinEntities(Collection<String> entities) {
		return entities.stream().sorted().map(entity -> "wd:" + entity).collect(Collectors.joining(" "));
	}

	public static String joinRelations(Collection<String> relations) {
		return relations.stream().sorted().map(relation -> "wdp:" + relation).collect(Collectors.joining(" "));
	}

	public static class EntityRelationPair {
		public String entity;
		public String relation;

		public EntityRelationPair(String entity, String relation) {
			this.entity = entity;
			this.relation = relation;
		}

		@Override
		public boolean equals(Object other) {
			if (!(other instanceof EntityRelationPair)) {
				return false;
			}
			EntityRelationPair o = (EntityRelationPair) other;
			return o.entity.equals(entity) && o.relation.equals(relation);
		}

		@Override
		public int hashCode() {
			return entity.hashCode() * 7 ^ relation.hashCode() * 13;
		}
	}

	public static class Triple {
		public String subject;
		public String relation;
		public String object;

		public Triple(String subject, String relation, String object) {
			this.subject = subject;
			this.relation = relation;
			this.object = object;
		}

		@Override
		public String toString() {
			return "Triple{" + subject + " " + relation + " " + object + "}";
		}

		@Override
		public boolean equals(Object other) {
			if (!(other instanceof Triple)) {
				return false;
			}
			Triple o = (Triple) other;
			return o.subject.equals(subject) && o.relation.equals(relation) && o.object.equals(object);
		}

		@Override
		public int hashCode() {
			return subject.hashCode() * 7 ^ relation.hashCode() * 13 + object.hashCode() * 29;
		}
	}

	public static final String WIKIDATA_PUBLIC_ENDPOINT = "https://query.wikidata.org/sparql";
	private String sparqlUrl;

	public WikidataClient(String sparqlUrl) {
		this.sparqlUrl = sparqlUrl;
	}

	public WikidataClient(Configuration configuration) {
		this.sparqlUrl = configuration.get("wikidata_endpoint");

		if (this.sparqlUrl == null || this.sparqlUrl == "") {
			System.out.println("No dbpedia_endpoint given!");
			System.exit(1);
		}
	}

	public static WikidataClient newPublicEndpointClient() {
		return new WikidataClient(WIKIDATA_PUBLIC_ENDPOINT);
	}
	// http://localhost:3030/wikidata/query

	// TODO: cache

	private static final String PREFIXES = "PREFIX wd: <http://www.wikidata.org/entity/>\n" +
			"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" +
			"PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" +
			"PREFIX wd: <http://www.wikidata.org/entity/>\n" +
			"PREFIX wdp: <http://www.wikidata.org/prop/direct/>\n" +
			"";

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
		if (!relationInteresting(relation)) {
			return null;
		}
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

	private static Triple transformRelation(String subject, String relation, String object) {
		if (!relationInteresting(relation)) {
			return null;
		}
		relation = normalizeRelation(relation);
		if (isStatement(subject) || isStatement(object)) {
			return null;
		}
		if (!subject.contains("/Q") || !object.contains("/Q")) {
			return null;
		}
		if (!relation.contains("/P")) {
			return null;
		}
		if (!isWikidataEntityUrl(subject) || !isWikidataEntityUrl(object)) {
			return null;
		}
		subject = wikidataEntityUrlToEntityId(subject);
		object = wikidataEntityUrlToEntityId(object);
		relation = wikidataPropertyUrlToPropertyId(relation);
		return new Triple(subject, relation, object);
	}

	public List<Triple> collectForwardProperties(String wikidataId) {
		String queryString = PREFIXES + "\n" +
			"SELECT ?rel ?other WHERE { wd:" + wikidataId + " ?rel ?other . } LIMIT 500";  // TODO: remove limit 500

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

	public List<Triple> collectBackwardProperties(String wikidataId) {
		String queryString = PREFIXES + "\n" +
			"SELECT ?rel ?other WHERE { ?other ?rel wd:" + wikidataId + " . } LIMIT 500";  // TODO: remove limit 500

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

	private Map<String, List<Triple>> cache = new HashMap<>();

	public List<Triple> getAllTriplesOfEntity(String wikidataId) {
		if (cache.containsKey(wikidataId)) {
			return cache.get(wikidataId);
		}
		ArrayList<Triple> triples = new ArrayList<Triple>();
		triples.addAll(collectForwardProperties(wikidataId));
		triples.addAll(collectBackwardProperties(wikidataId));
		cache.put(wikidataId, triples);
		return triples;
	}

	public List<Triple> getTriplesBetweenEntities(Collection<String> wikidataIds, Collection<String> relations) {
		if (wikidataIds.isEmpty()) {
			return Collections.emptyList();
		}
		String x = joinEntities(wikidataIds);
		String queryString = PREFIXES + String.format(
				"SELECT ?s ?p ?o\n" +
				"WHERE {\n" +
				"    VALUES ?s { %1$s }\n" +
				"    VALUES ?o { %1$s }\n" +
				"    VALUES ?p { %2$s }\n" +
				"    ?s ?p ?o\n" +
				"}", x, joinRelations(relations));

		Query query = QueryFactory.create(queryString);
		List<Triple> resultsx = new ArrayList<>();
		try (QueryExecution execution = QueryExecutionFactory.sparqlService(sparqlUrl, query)) {
			ResultSet results = execution.execSelect();
			while (results.hasNext()) {
				QuerySolution soln = results.nextSolution();
				RDFNode s = soln.get("s");
				RDFNode p = soln.get("p");
				RDFNode o = soln.get("o");
				if (!s.isResource() || !p.isResource() || !o.isResource()) {
					// (literals)
					continue;
				}
				Resource sr = soln.getResource("s");
				Resource pr = soln.getResource("p");
				Resource or = soln.getResource("o");
				if (sr.isAnon() || pr.isAnon() || or.isAnon()) {
					// (anonymous)
					continue;
				}
				Triple triple = transformRelation(sr.getURI(), pr.getURI(), or.getURI());
				if (triple != null) {
					resultsx.add(triple);
				}
			}
		}
		return resultsx;
	}

	public Set<EntityRelationPair> getSubjectRelationPairs(Collection<String> wikidataIds, Collection<String> relations) {
		if (wikidataIds.isEmpty()) {
			return Collections.emptySet();
		}

		Set<String> rels = new HashSet<>();
		String queryString = PREFIXES + String.format(
				"SELECT ?s ?p\n" +
				"WHERE {\n" +
				"    VALUES ?s { %1$s }\n" +
				"    VALUES ?p { %2$s }\n" +
				"    ?s ?p ?o\n" +
				"}", joinEntities(wikidataIds), joinRelations(relations));

		Query query = QueryFactory.create(queryString);
		Set<EntityRelationPair> resultsx = new HashSet<>();
		try (QueryExecution execution = QueryExecutionFactory.sparqlService(sparqlUrl, query)) {
			ResultSet results = execution.execSelect();
			while (results.hasNext()) {
				QuerySolution soln = results.nextSolution();
				RDFNode s = soln.get("s");
				RDFNode p = soln.get("p");
				if (!s.isResource() || !p.isResource()) {
					// (literals)
					continue;
				}
				Resource sr = soln.getResource("s");
				Resource pr = soln.getResource("p");
				if (sr.isAnon() || pr.isAnon()) {
					// (anonymous)
					continue;
				}

				String rr = normalizeRelation(pr.getURI());
				if (rr == null) {
					continue;
				}
				rr = wikidataPropertyUrlToPropertyId(rr);
				String ss = sr.getURI();
				if (!isWikidataEntityUrl(ss)) {
					continue;
				}
				ss = wikidataEntityUrlToEntityId(ss);
				resultsx.add(new EntityRelationPair(ss, rr));
			}
		}
		return resultsx;
	}

	public Set<EntityRelationPair> getObjectRelationPairs(Collection<String> wikidataIds, Collection<String> relations) {
		if (wikidataIds.isEmpty()) {
			return Collections.emptySet();
		}

		Set<String> rels = new HashSet<>();
		String queryString = PREFIXES + String.format(
				"SELECT ?o ?p\n" +
				"WHERE {\n" +
				"    VALUES ?p { %1$s }\n" +
				"    VALUES ?o { %2$s }\n" +
				"    ?s ?p ?o\n" +
				"}", joinEntities(wikidataIds), joinRelations(relations));

		Query query = QueryFactory.create(queryString);
		Set<EntityRelationPair> resultsx = new HashSet<>();
		try (QueryExecution execution = QueryExecutionFactory.sparqlService(sparqlUrl, query)) {
			ResultSet results = execution.execSelect();
			while (results.hasNext()) {
				QuerySolution soln = results.nextSolution();
				RDFNode o = soln.get("o");
				RDFNode p = soln.get("p");
				if (!o.isResource() || !p.isResource()) {
					// (literals)
					continue;
				}
				Resource or = soln.getResource("o");
				Resource pr = soln.getResource("p");
				if (or.isAnon() || pr.isAnon()) {
					// (anonymous)
					continue;
				}

				String rr = normalizeRelation(pr.getURI());
				if (rr == null) {
					continue;
				}
				rr = wikidataPropertyUrlToPropertyId(rr);
				String oo = or.getURI();
				if (!isWikidataEntityUrl(oo)) {
					continue;
				}
				oo = wikidataEntityUrlToEntityId(oo);
				resultsx.add(new EntityRelationPair(oo, rr));
			}
		}
		return resultsx;
	}
}
