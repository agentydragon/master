import random
import time
import json
import requests

from src.prototype.lib import flags
from src.prototype.lib import zk

DEFAULT_PUBLIC_SPOTLIGHT_ENDPOINT = 'http://spotlight.sztaki.hu:2222/rest/annotate'

flags.add_argument('--spotlight_endpoint',
                   help=('List of Spotlight endpoints. Example: '
                         'http://localhost:2222/rest/annotate,'
                         'http://spotlight.sztaki.hu:2222/rest/annotate'))

def get_default_spotlight_endpoint():
    endpoint = flags.parse_args().spotlight_endpoint
    if endpoint:
        return endpoint

    zk_endpoint = zk.get_spotlight_endpoint()
    if zk_endpoint:
        print("Grabbed Spotlight endpoint from ZK:", zk_endpoint)
        return zk_endpoint

    raise Exception('No Spotlight endpoint available.')

    # print("WARN: Using default public Spotlight endpoint")
    # return DEFAULT_PUBLIC_SPOTLIGHT_ENDPOINT

class SpotlightClient(object):
    def __init__(self, endpoint=None):
        if endpoint is None:
            endpoint = get_default_spotlight_endpoint()
        self.endpoints = endpoint.split(',')

    def annotate_text(self, text):
        assert text.strip() != ''

        retries = 0

        while True:
            endpoint = random.choice(self.endpoints)

            r = requests.post(endpoint, data={
              'text': text,
              'confidence': '0.35'
            }, headers={'Accept': 'application/json'})
            try:
                return r.json()
            except:
                print(r)
                print(r.text)
                retries += 1
                if retries >= 5:
                    raise
                time.sleep(10)

#def main():
#    parser.add_argument('--article_plaintext_path', required=True)
#    parser.add_argument('--output_path', required=True)
#    args = parser.parse_args()
#
#    text = open(args.article_plaintext_path).read()
#    result = annotate_text(text)
#    with open(args.output_path, 'w') as f:
#        f.write(json.dumps(result))
#
#if __name__ == '__main__':
#    main()
