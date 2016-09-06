import java.io.*;
import java.util.*;
import java.net.*;

public class SpotlightPooledConnection implements SpotlightConnection {
	private SpotlightConnection[] pool;
	private Random random = new Random();

	// example: "http://localhost:2222/rest/annotate,..."
	public SpotlightPooledConnection(String[] endpointList) {
		pool = new SpotlightConnection[endpointList.length];
		for (int i = 0; i < endpointList.length; i++) {
			pool[i] = new SpotlightSingleConnection(endpointList[i]);
		}
	}

	public static String[] splitEndpointList(String endpointList) {
		return endpointList.split(",");
	}

	@Override
	public String getAnnotationJSON(String text) throws IOException {
		SpotlightConnection connection = pool[random.nextInt(pool.length)];
		return connection.getAnnotationJSON(text);
	}
}
