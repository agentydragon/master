import os
import os.path
import json

cache_dir = 'cache'
if not os.path.isdir(cache_dir):
    os.makedirs(cache_dir)

class JsonCache(object):
    def __init__(self, path):
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
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.data))
