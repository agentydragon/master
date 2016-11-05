import java.util.*;
import java.util.stream.*;

public class SampleGeneration {
	private static Set<WikidataClient.Triple> getDocumentSubgraph(SavedDocument document, WikidataClient wikidataClient, List<String> relations) {
		Set<String> batchWikidataIds = new HashSet<>();
		Set<WikidataClient.Triple> allTriples = new HashSet<>();
		int batchSize = 20;

		for (SavedDocument.DocumentSentence sentence : document.sentences) {
			SentenceWrapper sentenceWrapper = new SentenceWrapper(document, sentence);
			batchWikidataIds.addAll(sentenceWrapper.getSentenceWikidataIds());

			if (batchWikidataIds.size() >= batchSize) {
				allTriples.addAll(wikidataClient.getTriplesBetweenEntities(
					batchWikidataIds,
					relations
				));
				batchWikidataIds.clear();
			}
		}
		allTriples.addAll(wikidataClient.getTriplesBetweenEntities(
			batchWikidataIds,
			relations
		));
		return allTriples;
	}

	private static Set<String> getAllDocumentEntities(SavedDocument document) {
		Set<String> allWikidataIds = new HashSet<>();
		for (SavedDocument.DocumentSentence sentence : document.sentences) {
			SentenceWrapper sentenceWrapper = new SentenceWrapper(document, sentence);
			allWikidataIds.addAll(sentenceWrapper.getSentenceWikidataIds());
		}
		return allWikidataIds;
	}

	public static List<TrainingSample> getLabeledSamplesFromDocument(SavedDocument document, WikidataClient wikidataClient) {
		List<TrainingSample> samples = new ArrayList<>();

		Set<WikidataClient.Triple> allTriples = getDocumentSubgraph(document, wikidataClient, Relations.RELATIONS);
		Set<String> allWikidataIds = getAllDocumentEntities(document);

		Collection<WikidataClient.EntityRelationPair> documentSubjectRelationPairs = wikidataClient.getSubjectRelationPairs(allWikidataIds, Relations.RELATIONS);
		Collection<WikidataClient.EntityRelationPair> documentObjectRelationPairs = wikidataClient.getObjectRelationPairs(allWikidataIds, Relations.RELATIONS);

		for (SavedDocument.DocumentSentence sentence : document.sentences) {
			SentenceWrapper sentenceWrapper = new SentenceWrapper(document, sentence);
			Set<String> wikidataIds = sentenceWrapper.getSentenceWikidataIds();

			List<WikidataClient.EntityRelationPair> sentenceSubjectRelationPairs = documentSubjectRelationPairs.stream().filter(pair -> wikidataIds.contains(pair.entity)).collect(Collectors.toList());
			List<WikidataClient.EntityRelationPair> sentenceObjectRelationPairs = documentObjectRelationPairs.stream().filter(pair -> wikidataIds.contains(pair.entity)).collect(Collectors.toList());

			Set<String> sentenceRelations = new HashSet<>();
			sentenceRelations.addAll(sentenceSubjectRelationPairs.stream().map(pair -> pair.relation).collect(Collectors.toList()));
			sentenceRelations.addAll(sentenceObjectRelationPairs.stream().map(pair -> pair.relation).collect(Collectors.toList()));

			for (String relation : sentenceRelations) {
				List<String> subjectWikidataIds = sentenceSubjectRelationPairs.stream().filter(pair -> pair.relation.equals(relation)).map(pair -> pair.entity).collect(Collectors.toList());
				List<String> objectWikidataIds = sentenceObjectRelationPairs.stream().filter(pair -> pair.relation.equals(relation)).map(pair -> pair.entity).collect(Collectors.toList());

				for (String subject : wikidataIds) {
					for (String object : wikidataIds) {
						// Against reflexive references ("Country is in country").
						if (sentenceWrapper.mentionsInSentenceOverlap(subject, object)) {
							continue;
						}

						WikidataClient.Triple triple = new WikidataClient.Triple(subject, relation, object);
						TrainingSample.Positiveness positiveness;
						if (allTriples.contains(triple)) {
							// True relation. Not a negative.
							positiveness = TrainingSample.Positiveness.TRUE;
						} else {
							boolean subjectHasCounterexample = subjectWikidataIds.contains(subject);
							boolean objectHasCounterexample = objectWikidataIds.contains(object);
							boolean hasCounterexample = (subjectHasCounterexample || objectHasCounterexample);

							if (hasCounterexample) {
								// This sentence is false (LCWA)
								positiveness = TrainingSample.Positiveness.FALSE;
							} else {
								// Sentence may be either true or false.
								positiveness = TrainingSample.Positiveness.UNKNOWN;
								// continue;
							}
						}
						TrainingSample sample = sentenceWrapper.makeTrainingSample(
								subject,
								relation,
								object,
								positiveness);
						samples.add(sample);
					}
				}
			}
		}

		System.out.println("Document produced " + samples.size() + " labeled samples.");
		return samples;
	}

	private static class SentenceWrapper {
		private SavedDocument document;
		private SavedDocument.DocumentSentence sentence;

		public SentenceWrapper(SavedDocument document, SavedDocument.DocumentSentence sentence) {
			this.document = document;
			this.sentence = sentence;
		}

		public List<Integer> findSentenceTokenIdxsOfEntity(String entity) {
			List<SavedDocument.SpotlightMention> mentions = new ArrayList<>();
			for (SavedDocument.SpotlightMention mention : document.getSpotlightMentionsInSentence(sentence)) {
				if (mention.wikidataId == entity) {
					mentions.add(mention);
				}
			}

			Set<Integer> tokenIdxs = new HashSet<>();
			for (int i = 0; i < sentence.tokens.size(); i++) {
				SavedDocument.SentenceToken token = sentence.tokens.get(i);
				for (SavedDocument.SpotlightMention mention : mentions) {
					if (token.startOffset >= mention.startOffset && token.endOffset <= mention.endOffset) {
						tokenIdxs.add(i);
					}
				}
			}
			List<Integer> list = new ArrayList(tokenIdxs);
			Collections.sort(list);
			return list;
		}

		public Set<String> getSentenceWikidataIds() {
			Set<String> wikidataIds = new HashSet<>();
			for (SavedDocument.SpotlightMention mention : document.getSpotlightMentionsInSentence(sentence)) {
				if (mention.wikidataId == null) {
					continue;
				}

				if (findSentenceTokenIdxsOfEntity(mention.wikidataId).isEmpty()) {
					// TODO: hack
					continue;
				}

				wikidataIds.add(mention.wikidataId);
			}
			return wikidataIds;
		}

		public boolean mentionsInSentenceOverlap(String s, String o) {
			Set<Integer> si = new HashSet<>(findSentenceTokenIdxsOfEntity(s));
			Set<Integer> oi = new HashSet<>(findSentenceTokenIdxsOfEntity(o));
			si.retainAll(oi);
			return !si.isEmpty();
		}

		public TrainingSample makeTrainingSample(String s, String relation, String o, TrainingSample.Positiveness positive) {
			TrainingSample sample = new TrainingSample();
			sample.relation = relation;
			sample.positive = positive;
			sample.subject = s;
			sample.object = o;
			sample.subjectTokenIndices = findSentenceTokenIdxsOfEntity(s);
			sample.objectTokenIndices = findSentenceTokenIdxsOfEntity(o);
			sample.sentence = new TrainingSample.TrainingSampleParsedSentence();
			sample.sentence.text = sentence.text;
			sample.sentence.tokens = new ArrayList<>();
			sample.sentence.originArticle = document.title;
			sample.sentence.originSentenceId = sentence.id;

			assert !sample.subjectTokenIndices.isEmpty();
			assert !sample.objectTokenIndices.isEmpty();

			for (SavedDocument.SentenceToken token : sentence.tokens) {
				TrainingSample.TrainingSampleSentenceToken t = new TrainingSample.TrainingSampleSentenceToken();
				t.startOffset = token.startOffset - sentence.startOffset();
				t.endOffset = token.endOffset - sentence.startOffset();
				t.lemma = token.lemma;
				t.pos = token.pos;
				t.ner = token.ner;
				sample.sentence.tokens.add(t);
			}
			// TODO: Mark all tokens that overlap the mention
			return sample;
		}
	}
}
