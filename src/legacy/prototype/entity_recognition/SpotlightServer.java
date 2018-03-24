import java.io.IOException;
import java.util.StringTokenizer;

import java.util.Properties;
import java.io.StringWriter;
import java.lang.System;
import org.dbpedia.spotlight.web.rest.Server;

public class SpotlightServer {
	public static void main(String[] args) throws Exception {
		String port;
		if (args.length > 0) {
			port = args[0];
		} else {
			port = "2222";
		}
		Server.main(new String[]{"src/prototype/entity_recognition/en", "http://localhost:" + port + "/rest"});
	}
}
