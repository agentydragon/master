import java.io.*;
import java.util.*;
import java.net.*;

public interface SpotlightConnection {
	String getAnnotationJSON(String text) throws IOException;
}
