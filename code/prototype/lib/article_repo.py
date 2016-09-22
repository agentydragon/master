import paths
import json
from py import file_util
import io
import os.path

def sanitize_articletitle(title):
    sanitized_articletitle = title.replace(' ', '_').replace('/', '_').replace('.', '_')
    if len(sanitized_articletitle) > 100:
        sanitized_articletitle = sanitized_articletitle[:100]
    return sanitized_articletitle

def article_title_to_path(target_dir, title):
    sanitized_articletitle = sanitize_articletitle(title)
    first1 = sanitized_articletitle[:1]
    first2 = sanitized_articletitle[:2]
    first3 = sanitized_articletitle[:3]
    target_dir = target_dir + '/' + first1 + '/' + first2 + '/' + first3
    file_util.ensure_dir(target_dir)
    return target_dir + '/' + sanitized_articletitle + '.json'

def write_article(target_dir, title, data):
    path = article_title_to_path(target_dir, title)
    with io.open(path, 'w', encoding='utf8') as f:
        json.dump(data, f)

def article_exists(title,
                   target_dir=paths.WIKI_ARTICLES_PLAINTEXTS_DIR):
    path = article_title_to_path(target_dir, title)
    return os.path.isfile(path)

def load_article(target_dir, title):
    path = article_title_to_path(target_dir, title)
    with io.open(path, 'r', encoding='utf8') as f:
        try:
            return json.load(f)
        except:
            print("Error loading article", title)
            raise
