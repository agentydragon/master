import unicodedata
import json
from py import file_util
import io

def sanitize_articletitle(title):
    sanitized_articletitle = title.replace(' ', '_').replace('/', '_')
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
    with io.open(path, 'w', encoding='utf8') as out:
        json.dump(data)

def load_article(target_dir, title):
    path = article_title_to_path(target_dir, title)
    with io.open(path, 'r', encoding='utf8') as f:
        return json.load(f)
