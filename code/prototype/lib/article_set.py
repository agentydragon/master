import paths
from prototype.lib import flags

flags.add_argument('--article_list_file',
                   default=paths.ARTICLE_LIST_PATH)
flags.add_argument('--max_articles', default=None, type=int)

class ArticleSet(object):
    def __init__(self, path = None, maximum = None):
        if path is None:
            path = flags.parse_args().article_list_file

        if maximum is None:
            maximum = flags.parse_args().max_articles

        with open(path) as f:
            article_names = list(map(lambda line: line.strip(), list(f)))

        if maximum is not None:
            article_names = article_names[:maximum]

        self.article_names = article_names

    def split_train_test(self):
        train = []
        test = []
        for i, title in enumerate(self.article_names):
            if i % 10 in (2, 3, 5, 7): # 40% test 60% train
                test.append(title)
            else:
                train.append(title)
        return train, test
