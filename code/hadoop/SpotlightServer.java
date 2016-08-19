import java.lang.Process;
import java.lang.System;
import java.lang.ProcessBuilder;
import java.io.*;
import java.util.*;

import java.net.*;

public class SpotlightServer {
	private Process process;

	public void start() throws IOException {
		ProcessBuilder pb = new ProcessBuilder(
				"spotlight/Spotlight");
		process = pb.start();

		BufferedReader reader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
		do {
			String line = reader.readLine();
			if (line == null) {
				System.exit(1);
			}
			if (line.contains("Server started")) {
				// Server is running now.
				break;
			}
		} while (true);
	}

	public void stop() {
		process.destroy();
		process = null;
	}

	public String getAnnotationJSON(String text) throws IOException {
		HttpURLConnection connection = null;
		URL url = new URL("http://localhost:2222/rest/annotate");
		connection = (HttpURLConnection) url.openConnection();
		connection.setRequestMethod("POST");
		connection.setRequestProperty("Accept", "application/json");
		connection.setDoOutput(true);
		connection.setDoInput(true);

		DataOutputStream wr = new DataOutputStream(connection.getOutputStream());
		String params = "text=" + URLEncoder.encode(text, "UTF-8") + "&confidence=0.35";
		wr.writeBytes(params);
		wr.flush();
		wr.close();

		InputStream is = connection.getInputStream();
		BufferedReader rd = new BufferedReader(new InputStreamReader(is));
		StringBuilder out = new StringBuilder();
		String line;
		while ((line = rd.readLine()) != null) {
			out.append(line);
		}
		return out.toString();

		/*
		// Request parameters and other properties.
		List<NameValuePair> params = new ArrayList<NameValuePair>(2);
		params.add(new BasicNameValuePair("text", text));
		params.add(new BasicNameValuePair("confidence", "0.35"));
		httppost.setEntity(new UrlEncodedFormEntity(params, "UTF-8"));
		*/

		/*
		InputStream instream = entity.getContent();
		try {
			return IOUtils.toString(instream, "UTF-8");
			// do something useful
		} finally {
			instream.close();
		}
		*/
	}
}
