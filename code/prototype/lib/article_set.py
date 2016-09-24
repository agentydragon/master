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

    def split_train_test(self):
        train = []
        test = []
        for i, title in enumerate(self.article_names):
            if i % 10 in (2, 3, 5, 7): # 40% test 60% train
                test.append(title)
            else:
                train.append(title)
        return train, test
