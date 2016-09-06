import os
import os.path
import json
from py import paths
from py import file_util

class JsonCache(object):
    def __init__(self, name):
        path = paths.JSON_CACHE_DIR + '/' + name + '.json'
        self.path = path
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __contains__(self, key):
        return key in self.data

    def load(self):
        if len(self.data) == 0:
            if os.path.isfile(self.path):
                with open(self.path) as f:
                    self.data = json.loads(f.read())

    def save(self):
        file_util.ensure_dir(paths.JSON_CACHE_DIR)
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.data))
