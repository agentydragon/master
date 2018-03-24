from __future__ import absolute_import
from __future__ import print_function

import sys

# Workaround for issue #5.
# TODO(#5): Come up with a better work-around, or remove this hack once Bazel
# fixes their thing.


def hoist_package_to_top_of_path(package):
    hoisted_paths = []
    for path in sys.path:
        if package in path:
            hoisted_paths.append(path)
    if len(hoisted_paths) != 1:
        raise RuntimeError('Not exactly 1 path to be hoisted: ' +
                           str(hoisted_paths))
    sys.path.insert(0, hoisted_paths[0])


hoist_package_to_top_of_path('pypi__google_cloud_storage_1_7_0')

from google.cloud import storage
import datetime

filename = datetime.datetime.now().strftime('single-file-%Y%m%d-%H%M%S.txt')


def _get_storage_client():
    return storage.Client(
        project='extended-atrium-198523')  # current_app.config['PROJECT_ID'])


client = _get_storage_client()
# current_app.config['CLOUD_STORAGE_BUCKET'])
bucket = client.bucket("agentydragon-gspython")
blob = bucket.blob(filename)
blob.upload_from_string("Hello, World!", content_type="text/html")

print("Success! File written:", blob.public_url)
