import org.json.*;
import java.io.*;
import java.lang.*;
import org.apache.commons.io.FileUtils;
import java.util.*;

public class SampleRepository {
	private static String basePath = "/storage/brno7-cerit/home/prvak/data/relation-samples";

	private static String prefix(String str, int len) {
		if (str.codePointCount(0, str.length()) < len) {
			return str;
		}
		return str.substring(0, str.offsetByCodePoints(0, len));
	}

	private static String articleRelationToPath(String title, String relation) {
		title = title.replace(" ", "_");
		title = title.replace("/", "_");
		title = title.replace(".", "_");
		if (title.codePointCount(0, title.length()) > 100) {
			title = prefix(title, 100);
		}
		String dir = basePath + "/" + relation + "/positive/" + prefix(title, 1) + "/" + prefix(title, 2) + "/" + prefix(title, 3);
		new File(dir).mkdirs();
		return dir + "/" + title + ".json";
	}

	private static void writeRelations(String title, String relation, List<TrainingSamples.TrainingSample> samples) throws IOException {
		JSONArray samps = new JSONArray();
		for (TrainingSamples.TrainingSample sample : samples) {
			samps.put(sample.toString());
		}

		JSONObject obj = new JSONObject();
		obj.put("samples", samps);

		String path = articleRelationToPath(title, relation);
		File file = new File(path);
		FileUtils.writeStringToFile(file, obj.toString());
	}

	public static void writeArticle(String title, List<TrainingSamples.TrainingSample> samples) throws IOException {
		Set<String> relations = new HashSet<>();
		for (TrainingSamples.TrainingSample sample : samples) {
			relations.add(sample.getRelation());
		}
		for (String relation : relations) {
			List<TrainingSamples.TrainingSample> samps = new ArrayList<>();
			for (TrainingSamples.TrainingSample sample : samples) {
				if (sample.getRelation() == relation) {
					samps.add(sample);
				}
			}
			writeRelations(title, relation, samps);
		}
	}
}
