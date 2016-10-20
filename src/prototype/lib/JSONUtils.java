import org.json.*;
import java.util.*;
import java.util.stream.*;
import java.util.function.*;
import java.io.*;

public class JSONUtils {
	public static <T> List<T> arrayMap(JSONArray array, Function<JSONObject, T> convert) {
		List<T> r = new ArrayList<>();
		for (int i = 0; i < array.length(); i++) {
			r.add(convert.apply((JSONObject) array.get(i)));
		}
		return r;
	}

	public static List<Integer> arrayToIntList(JSONArray array) {
		List<Integer> r = new ArrayList<>();
		for (int i = 0; i < array.length(); i++) {
			r.add(array.getInt(i));
		}
		return r;
	}

	public static <T> JSONArray toArray(List<T> array, Function<T, JSONObject> convert) {
		return new JSONArray(array.stream().map(convert).collect(Collectors.toList()));
	}

	public static JSONArray toIntArray(List<Integer> array) {
		return new JSONArray(array);
	}
}
