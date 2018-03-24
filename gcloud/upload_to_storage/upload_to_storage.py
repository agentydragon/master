from __future__ import absolute_import

from google.cloud import storage
import urllib2

url_to_download = 'https://dumps.wikimedia.org/enwiki/20180301/enwiki-20180301-pages-articles.xml.bz2'
filename = 'wiki-dumps/enwiki/20180301/enwiki-20180301-pages-articles.xml.bz2'

def _get_storage_client():
    return storage.Client(
        project='extended-atrium-198523')  # current_app.config['PROJECT_ID'])

client = _get_storage_client()
bucket = client.bucket("agentydragon-gspython")  # current_app.config['CLOUD_STORAGE_BUCKET'])
http = urllib2.urlopen(url_to_download)
blob = bucket.blob(filename, chunk_size=1024 * 1024)


class UrlFile:
    """Wraps a urllib2 opened URL to enable uploading it by chunks."""
    def __init__(self, wrapped_file):
        self.wrapped_file = wrapped_file
        self.position = 0

    def read(self, length):
        print 'reading', length, 'bytes'
        data = self.wrapped_file.read(length)
        self.position += len(data)
        print 'read', len(data), 'bytes, position=', self.position
        return data

    def tell(self):
        return self.position


blob.upload_from_file(UrlFile(http), content_type="text/html")

print "Success! Downloaded the URL into Google Cloud Storage."
print blob.public_url
