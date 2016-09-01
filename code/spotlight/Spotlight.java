import java.io.IOException;
import java.util.StringTokenizer;

import java.util.Properties;
import java.io.StringWriter;
import java.lang.System;
import org.dbpedia.spotlight.web.rest.Server;

public class Spotlight {
	public static void main(String[] args) throws Exception {
		Server.main(new String[]{"spotlight/en", "http://localhost:2222/rest"});
	}
}
