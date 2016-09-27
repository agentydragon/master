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

    def split_train_test_calibrate(self):
        train = []
        test = []
        calibrate = []
        for i, title in enumerate(self.article_names):
            # 50% train 30% test 20% calibration
            if i % 10 in (2, 3, 5, 7, 9):
                train.append(title)

            if i % 10 in (0, 1, 4):
                test.append(title)

            if i % 10 in (6, 8):
                calibrate.append(title)
        return train, test, calibrate
