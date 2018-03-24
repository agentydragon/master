import java.io.IOException;
import java.io.*;

import org.apache.hadoop.fs.*;
import java.util.*;
import java.lang.System;
import org.apache.log4j.Logger;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.Path;
public class ArticleSet {
	private List<String> articles = new ArrayList<>();
	private Set<String> whitelist = new HashSet<>();

	public void load(Configuration conf) throws IOException {
		FileSystem fs = FileSystem.get(conf);
		FSDataInputStream inputStream = fs.open(new Path("/user/prvak/articles.tsv"));
		try (BufferedReader r = new BufferedReader(new InputStreamReader(inputStream))) {
			String line;

			int i = 0;

			while  ((line = r.readLine()) != null) {
				String article = line.split("\t")[1];
				articles.add(article);
				whitelist.add(article);
				i++;
			}
		}
		inputStream.close();
	}

	public List<String> getArticleList() {
		return articles;
	}

	public boolean contains(String title) {
		return whitelist.contains(title);
	}
}
