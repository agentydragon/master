import org.json.*;
import java.io.*;
import java.lang.*;
import org.apache.commons.io.FileUtils;

public class ArticleRepository {
	private static String basePath = "/storage/brno7-cerit/home/prvak/data/wiki-articles-plaintexts";

	private static String prefix(String str, int len) {
		if (str.codePointCount(0, str.length()) < len) {
			return str;
		}
		return str.substring(0, str.offsetByCodePoints(0, len));
	}

	private static String articleTitleToPath(String title) {
		title = title.replace(" ", "_");
		title = title.replace("/", "_");
		title = title.replace(".", "_");
		if (title.codePointCount(0, title.length()) > 100) {
			title = prefix(title, 100);
		}
		String sub = prefix(title, 1) + "/" + prefix(title, 2) + "/" + prefix(title, 3) + "/" + title + ".json";
		return basePath + "/" + sub;
	}

	public static JSONObject readArticle(String title) throws IOException {
		String path = articleTitleToPath(title);
		File file = new File(path);
		String jsonContent = FileUtils.readFileToString(file);
		return new JSONObject(jsonContent);
	}

	public static void writeArticle(String title, JSONObject data) throws IOException {
		String path = articleTitleToPath(title);
		File file = new File(path);
		FileUtils.writeStringToFile(file, data.toString());
	}

	public static boolean articleExists(String title) {
		String path = articleTitleToPath(title);
		return new File(path).exists();
	}
}
