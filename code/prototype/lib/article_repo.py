import paths
import json
from prototype.lib import file_util
from prototype.lib import flags
import io
import os.path

flags.add_argument('--article_plaintexts_dir',
                   default=paths.WIKI_ARTICLES_PLAINTEXTS_DIR)

def get_article_plaintexts_dir():
    return flags.parse_args().article_plaintexts_dir

def sanitize_articletitle(title):
    sanitized_articletitle = title.replace(' ', '_').replace('/', '_').replace('.', '_')
    if len(sanitized_articletitle) > 100:
        sanitized_articletitle = sanitized_articletitle[:100]
    return sanitized_articletitle

class ArticleRepo(object):
    def __init__(self, target_dir=None):
        if target_dir is None:
            target_dir = get_article_plaintexts_dir()
        self.target_dir = target_dir

    def article_title_to_path(self, title):
        sanitized_articletitle = sanitize_articletitle(title)
        first1 = sanitized_articletitle[:1]
        first2 = sanitized_articletitle[:2]
        first3 = sanitized_articletitle[:3]
        subdir = self.target_dir + '/' + first1 + '/' + first2 + '/' + first3
        file_util.ensure_dir(subdir)
        return subdir + '/' + sanitized_articletitle + '.json'

    def write_article(self, title, document):
        path = self.article_title_to_path(title)
        with io.open(path, 'w', encoding='utf8') as f:
            json.dump(document.to_json(), f)

    def article_exists(self, title):
        path = self.article_title_to_path(title)
        return os.path.isfile(path)

    def load_article(self, title):
        path = self.article_title_to_path(title)
        with io.open(path, 'r', encoding='utf8') as f:
            try:
                return sentence.SavedDocument(json.load(f))
            except:
                print("Error loading article", title)
                raise
