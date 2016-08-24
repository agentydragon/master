import java.util.List;
import java.util.ArrayList;
import org.json.*;

public class AnnotateCoreferences {
	public List<Sentence.SpotlightMention> SpotlightToMentions(JSONObject spotlightJson) {
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

	public Sentence.Document PropagateEntities(Sentence.Document documentProto, List<Sentence.SpotlightMention> spotlightMentions) {
		return null;
	}
}
