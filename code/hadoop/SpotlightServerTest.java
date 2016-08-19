
public class SpotlightServerTest {
	public static void main(String[] args) throws Exception {
		SpotlightServer server = new SpotlightServer();
		server.start();
		try {
			String text = "Hello World! Barack Obama is a black man and he is the president of USA, and his wife is named Michelle Obama.";
			System.out.println(text);
			System.out.println(server.getAnnotationJSON(text));

			// TODO: CHECK THINGS
		} finally {
			server.stop();
		}
	}
}
