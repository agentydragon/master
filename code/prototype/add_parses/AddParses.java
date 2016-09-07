import org.json.*;
import java.io.*;
import java.lang.*;
import org.apache.commons.io.FileUtils;

public class AddParses {
	// TODO: SWIG?
	private static String basePath = "/storage/brno7-cerit/home/prvak/wiki-articles-plaintexts";

	private static String prefix(String str, int len) {
		if (str.codePointCount(0, str.length()) < len) {
			return str;
		}
		return str.substring(0, str.offsetByCodePoints(0, len));
	}

	private static String articleTitleToPath(String title) {
		title = title.replace(" ", "_");
		title = title.replace("/", "_");
		if (title.codePointCount(0, title.length()) > 100) {
			title = prefix(title, 100);
		}
		String sub = prefix(title, 1) + "/" + prefix(title, 2) + "/" + prefix(title, 3) + "/" + title + ".json";
		return basePath + "/" + sub;
	}
	private static void processArticle(String title) {
		try {
			String path = articleTitleToPath(title);
			System.out.println(path);

			File file = new File(path);

			String jsonContent = FileUtils.readFileToString(file);
			JSONObject json = new JSONObject(jsonContent);
			String articleText = (String) json.get("plaintext");
			json.put("corenlp_xml", corenlpInterface.getXML(articleText));

			FileUtils.writeStringToFile(file, json.toString());
		} catch (IOException e) {
			System.out.println("Failed: " + title);
			System.out.println(e);
		}
	}

	public static void main(String[] args) {
		CoreNLPInterface corenlpInterface = new CoreNLPInterface();
		corenlpInterface.setup();

		for (String title : args) {
			processArticle(title);
		}
	}
}
