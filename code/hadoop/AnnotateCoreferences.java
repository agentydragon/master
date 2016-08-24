import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import org.json.*;

public class AnnotateCoreferences {
	public static List<Sentence.SpotlightMention> SpotlightToMentions(JSONObject spotlightJson) {
		List<Sentence.SpotlightMention> mentions = new ArrayList<>();

		JSONArray mentionsList = (JSONArray) spotlightJson.get("Resources");
		for (Object o : mentionsList) {
			JSONObject mentionJson = (JSONObject) o;
			Sentence.SpotlightMention.Builder mentionBuilder = Sentence.SpotlightMention.newBuilder()
				.setStartOffset(Integer.parseInt((String) mentionJson.get("@offset")));
			if (mentionJson.get("@surfaceForm") == null) {
				// TODO HACK?
				continue;
			}
			String surfaceForm = (String) mentionJson.get("@surfaceForm");
			mentionBuilder.setEndOffset(mentionBuilder.getStartOffset() + surfaceForm.length())
				.setSurfaceForm(surfaceForm)
				.setUri((String) mentionJson.get("@URI"));
			mentions.add(mentionBuilder.build());
		}

		return mentions;
	}

	private static Sentence.DocumentSentence findSentenceById(Sentence.Document document, int id) {
		for (Sentence.DocumentSentence sentence : document.getSentencesList()) {
			if (sentence.getId() == id) {
				return sentence;
			}
		}
		return null;
	}

	private static Sentence.SentenceToken findSentenceToken(Sentence.DocumentSentence sentence, int id) {
		for (Sentence.SentenceToken token : sentence.getTokensList()) {
			if (token.getId() == id) {
				return token;
			}
		}
		return null;
	}

	private static int getMentionStart(Sentence.Document document, Sentence.Mention mention) {
		Sentence.DocumentSentence sentence = findSentenceById(document, mention.getSentenceId());
		Sentence.SentenceToken token = findSentenceToken(sentence, mention.getStartWordId());
		if (token == null) {
			// TODO HAX
			return -1;
		}
		return token.getStartOffset();
	}

	private int getMentionEnd(Sentence.Document document, Sentence.Mention mention) {
		Sentence.DocumentSentence sentence = findSentenceById(document, mention.getSentenceId());
		Sentence.SentenceToken token = findSentenceToken(sentence, mention.getEndWordId() - 1);
		if (token == null) {
			// TODO HAX
			return -1;
		}
		return token.getEndOffset();
	}

	private static List<Sentence.SpotlightMention> findResourcesBetween(List<Sentence.SpotlightMention> spotlight, int start, int end) {
		List<Sentence.SpotlightMention> result = new ArrayList<>();
		for (Sentence.SpotlightMention mention : spotlight) {
			if (mention.getStartOffset() >= start && mention.getEndOffset() <= end) {
				result.add(mention);
			}
		}
		return result;
	}

	public static Sentence.Document PropagateEntities(Sentence.Document documentProto, List<Sentence.SpotlightMention> spotlightMentions) {
		Sentence.Document.Builder builder = Sentence.Document.newBuilder();
		builder.mergeFrom(documentProto);

		for (Sentence.Coreference.Builder coref : builder.getCoreferencesBuilderList()) {
			List<Sentence.SpotlightMention> fullMatches = new ArrayList<>();

			for (Sentence.Mention mention : coref.getMentionsList()) {
				int mentionStart = getMentionStart(documentProto, mention);
				int mentionEnd = getMentionStart(documentProto, mention);
				if (mentionEnd == -1) {
					// TODO hax
					continue;
				}
				String mentionText = mention.getText();
				String mentionActualText = documentProto.getText().substring(mentionStart, mentionEnd);
				if (!mentionText.equals(mentionActualText)) {
					// TODO: HAX; check this out.
					// nothing
				}

				for (Sentence.SpotlightMention resource : findResourcesBetween(spotlightMentions, mentionStart, mentionEnd)) {
					if (resource.getSurfaceForm().equals(mentionText) ||
							resource.getSurfaceForm().equals(mentionActualText)) {
						fullMatches.add(resource);
					} else {
						// TODO: ?
					}
				}
			}

			String bestMatch = null;

			Set<String> uris = new HashSet<>();
			for (Sentence.SpotlightMention fullMatch : fullMatches) {
				uris.add(fullMatch.getUri());
			}
			if (uris.size() > 0) {
				if (uris.size() > 1) {
					// TODO
					// print("FAIL: multiple URLs: ", uris)
				} else {
					bestMatch = (String) uris.toArray()[0];
				}
			}

			if (bestMatch != null) {
				String wikidataId = DBpediaClient.dbpediaUriToWikidataId(bestMatch);
				if (wikidataId != null) {
					coref.setWikidataEntityId(wikidataId);
				}
			}
		}

		return builder.build();
	}
}
