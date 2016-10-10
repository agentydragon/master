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
            article_names = []
            for line in f:
                line = line.strip()
                id, name, wikipedia_page = line.split("\t")
                # TODO: Use wikipedia_page instead.
                article_names.append(name)

        if maximum is not None:
            article_names = article_names[:maximum]

        self.article_names = article_names

    def split_train_test_calibrate(self):
        train = []
        test = []
        calibrate = []
        for i, title in enumerate(self.article_names):
            x = (i % 100)

            # 75% train 20% test 5% calibration
            if x < 75:
                train.append(title)
            elif x < 95:
                test.append(title)
            else:
                calibrate.append(title)
        return train, test, calibrate
