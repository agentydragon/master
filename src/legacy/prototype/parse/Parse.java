import org.json.*;
import java.io.*;
import java.lang.*;

public class Parse {
	private CoreNLPInterface corenlpInterface = new CoreNLPInterface();

	private void processArticle(String title) {
		try {
			System.out.println(title);

			if (!ArticleRepository.articleExists(title)) {
				System.out.println("Article doesn't exist");
				return;
			}

			JSONObject json = ArticleRepository.readArticle(title);

			// Skip if already processed.
			if (json.has("corenlp_xml") && json.get("corenlp_xml") != JSONObject.NULL) {
				System.out.println("Article already annotated");
				return;
			}

			String articleText = (String) json.get("plaintext");
			json.put("corenlp_xml", corenlpInterface.getXML(articleText));
			ArticleRepository.writeArticle(title, json);
		} catch (IOException e) {
			System.out.println("Failed: " + title);
			System.out.println(e);
		}
	}

	public void run(String[] args) {
		corenlpInterface.setup();

		for (String title : args) {
			processArticle(title);
		}
	}

	public static void main(String[] args) {
		new Parse().run(args);
	}
}
