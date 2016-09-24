import paths

class ArticleSet(object):
    def __init__(self, path = None, maximum = None):
        if path is None:
            path = paths.ARTICLE_LIST_PATH

        with open(path) as f:
            article_names = list(map(lambda line: line.strip(), list(f)))

        if maximum is not None:
            article_names = article_names[:maximum]

        self.article_names = article_names
