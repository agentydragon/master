import os
import os.path

def parse_proto_file(proto, path):
    message = proto()
    with open(path, 'rb') as f:
        message.ParseFromString(f.read())
    return message

def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def recursive_subfile_paths(dir_path):
    for root, subdirs, files in os.walk(dir_path):
        for filename in files:
            path = os.path.join(root, filename)
            yield path
