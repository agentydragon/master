import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import java.util.Map;
import java.util.HashMap;

public class GetTrainingSamples {
	public static class MentionInSentence {
		public int startTokenId;
		public int endTokenId;
		public String wikidataId;

		public MentionInSentence(int startTokenId, int endTokenId, String wikidataId) {
			this.startTokenId = startTokenId;
			this.endTokenId = endTokenId;
			this.wikidataId = wikidataId;
		}
	}

	private static class EntityPair {
		public String e1;
		public String e2;

		public EntityPair(String e1, String e2) {
			this.e1 = e1;
			this.e2 = e2;
		}

		@Override
		public boolean equals(Object other) {
			if (!(other instanceof EntityPair)) {
				return false;
			}
			EntityPair o = (EntityPair) other;
			return (e1 == o.e1) && (e2 == o.e2);
		}

		@Override
		public int hashCode() {
			return e1.hashCode() ^ e2.hashCode();
		}
	}

	public static class SentenceInDocument {
		private List<MentionInSentence> mentions;
		private List<String> wikidataIds;
		private Sentence.Document document;
		private int sentenceId;

		public List<String> getWikidataIds() {
			return wikidataIds;
		}

		public SentenceInDocument(Sentence.Document document, int sentenceId) {
			this.document = document;
			this.sentenceId = sentenceId;

			Set<String> wikidataIds = new HashSet<>();
			for (Sentence.Coreference coref : document.getCoreferencesList()) {
				if (!coref.hasWikidataEntityId() || coref.getWikidataEntityId() == "") {
					// entity not detected
					continue;
				}
				for (Sentence.Mention mention : coref.getMentionsList()) {
					mentions.add(new MentionInSentence(
								mention.getStartWordId(),
								mention.getEndWordId(),
								coref.getWikidataEntityId()));
					wikidataIds.add(coref.getWikidataEntityId());
				}
			}
			this.wikidataIds = new ArrayList(wikidataIds);
		}

		public List<EntityPair> getAllEntityPairs() {
			List<EntityPair> pairs = new ArrayList<>();
			for (String e1 : wikidataIds) {
				if (e1 == null) {
					continue;
				}
				for (String e2 : wikidataIds) {
					if (e2 == null) {
						// TODO: hax should not be
						// needed
						continue;
					}
					pairs.add(new EntityPair(e1, e2));
				}
			}
			return pairs;
		}

		public Sentence.DocumentSentence getSentence() {
			for (Sentence.DocumentSentence sentence : document.getSentencesList()) {
				if (sentence.getId() == sentenceId) {
					return sentence;
				}
			}
			return null;
		}

		public String getText() {
			return getSentence().getText();
		}

		public TrainingSamples.TrainingSample toSample(String relation, String e1, String e2, boolean positive) {
			assert wikidataIds.contains(e1) && wikidataIds.contains(e2);

			TrainingSamples.TrainingSample.Builder sample = TrainingSamples.TrainingSample.newBuilder()
				.setPositive(positive)
				.setRelation(relation)
				.setE1(e1)
				.setE2(e2);

			Sentence.DocumentSentence sentence = getSentence();

			List<Integer> e1Indices = new ArrayList<>();
			List<Integer> e2Indices = new ArrayList<>();
			for (MentionInSentence mention : mentions) {
				for (int tokenIndex = mention.startTokenId - 1;
						tokenIndex < mention.endTokenId - 1;
						tokenIndex++) {
					if (mention.wikidataId == e1 && !e1Indices.contains(tokenIndex)) {
						e1Indices.add(tokenIndex);
					}
					if (mention.wikidataId == e2 && !e2Indices.contains(tokenIndex)) {
						e2Indices.add(tokenIndex);
					}
				}
			}
			sample.addAllE1TokenIndices(e1Indices)
				.addAllE2TokenIndices(e2Indices);

			TrainingSamples.TrainingSampleParsedSentence.Builder bldr = TrainingSamples.TrainingSampleParsedSentence.newBuilder();
			//sample.getSentence().setText(sentence.getText());
			bldr.setText(sentence.getText());

			int sentenceStart = sentence.getTokens(0).getStartOffset();
			for (Sentence.SentenceToken token : sentence.getTokensList()) {
				TrainingSamples.TrainingSampleSentenceToken.Builder b = TrainingSamples.TrainingSampleSentenceToken.newBuilder();
				b.setStartOffset(token.getStartOffset() - sentenceStart);
				b.setEndOffset(token.getEndOffset() - sentenceStart);
				b.setLemma(token.getLemma());
				b.setPos(token.getPos());
				b.setNer(token.getNer());
				bldr.addTokens(b);
			}
			sample.setSentence(bldr);
			return sample.build();
		}
	}

	public static Map<EntityPair, List<String>> getTrueTriplesExpressedBySentence(SentenceInDocument sentence) {
		List<String> mentionedWikidataIds = sentence.getWikidataIds();
		List<EntityPair> sentenceEntityPairs = sentence.getAllEntityPairs();
		WikidataClient wikidataClient = new WikidataClient();

		Map<EntityPair, List<String>> allPairs = new HashMap<>();
		for (String wikidataId : mentionedWikidataIds) {
			for (WikidataClient.Triple triple : wikidataClient.getAllTriplesOfEntity(wikidataId)) {
				EntityPair pair = new EntityPair(triple.subject, triple.object);
				if (!sentenceEntityPairs.contains(pair)) {
					// relation holds, but not expressed by sentence
					continue;
				}
				if (!allPairs.containsKey(pair)) {
					// TODO: fixme: relations returned twice -- forward and backward
					allPairs.put(pair, new ArrayList<>());
				}
				allPairs.get(pair).add(triple.predicate);
			}
		}
		return allPairs;
	}

	public static List<TrainingSamples.TrainingSample> documentToSamples(Sentence.Document document) {
		ArrayList<TrainingSamples.TrainingSample> samples = new ArrayList<>();
		for (Sentence.DocumentSentence sentence : document.getSentencesList()) {
			SentenceInDocument sid = new SentenceInDocument(document, sentence.getId());
			samples.addAll(sentenceToTrainingSamples(sid));
		}
		return samples;
	}

	public static List<TrainingSamples.TrainingSample> sentenceToTrainingSamples(SentenceInDocument sentence) {
		Map<EntityPair, List<String>> allPairs = getTrueTriplesExpressedBySentence(sentence);

		List<TrainingSamples.TrainingSample> samples = new ArrayList<>();
		// Add positive samples.
		for (EntityPair pair : allPairs.keySet()) {
			for (String relation : allPairs.get(pair)) {
				TrainingSamples.TrainingSample sample = sentence.toSample(relation, pair.e1, pair.e2, true);
				samples.add(sample);
			}
		}

		// Add negative samples.
		// TODO
		if (sentence.getWikidataIds().size() >= 2) {
			String e1 = sentence.getWikidataIds().get(0);
			String e2 = sentence.getWikidataIds().get(1);

			EntityPair key = new EntityPair(e1, e2);

			for (String relation : Relations.IMPORTANT_RELATIONS) {
				if ((!allPairs.containsKey(key)) || (!allPairs.get(key).contains(relation))) {
					TrainingSamples.TrainingSample sample = sentence.toSample(relation, e1, e2, false);
					samples.add(sample);
				}
			}
		}

		return samples;
	}
}
