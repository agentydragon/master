from __future__ import absolute_import
from __future__ import print_function

import pprint
import sys
pprint.pprint(sys.path)

# Running help("modules") makes the google.cloud module available. SOMEHOW.
help("modules")

from google.cloud import storage
import datetime

filename = datetime.datetime.now().strftime('single-file-%Y%m%d-%H%M%S.txt')

def _get_storage_client():
    return storage.Client(
        project='extended-atrium-198523')  # current_app.config['PROJECT_ID'])

client = _get_storage_client()
bucket = client.bucket("agentydragon-gspython")  # current_app.config['CLOUD_STORAGE_BUCKET'])
blob = bucket.blob(filename)
blob.upload_from_string("Hello, World!", content_type="text/html")

print("Success! File written:", blob.public_url)
