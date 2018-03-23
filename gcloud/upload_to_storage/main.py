# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from google.cloud import storage
import six


def _get_storage_client():
    return storage.Client(
        project='extended-atrium-198523')  # current_app.config['PROJECT_ID'])


client = _get_storage_client()
bucket = client.bucket("agentydragon-gspython")  # current_app.config['CLOUD_STORAGE_BUCKET'])
import datetime
filename = datetime.datetime.now().strftime("test-file-%Y%m%d%H%M%S")
blob = bucket.blob(filename)

blob.upload_from_string(
    "hello world",#file_stream,
    content_type="text/plain")#content_type)

# upload_from_file: takes a file-like object

print blob.public_url
