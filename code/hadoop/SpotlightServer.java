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
}
