# Python 3

# tokenize and split to sentences; pos = annotate parts of speech

import sys
import json
import requests
import urllib.parse
import os.path
import glob

d = 'individual-articles'
endpoint = 'localhost:12111'

for file in glob.glob(os.path.join(d, '*', '*', '*.plaintext')):
    print(file)
    with open(file) as f:
        content = f.read()
    properties = {"annotators": "tokenize,ssplit", "outputFormat": "json"}
    r = requests.post('http://' + endpoint + "/?properties=" +
                      urllib.parse.quote_plus(json.dumps(properties)),
                      data=content.encode('utf-8'))
    resultpath = file + '.corenlpjson'
    with open(resultpath, 'w') as f:
        f.write(r.text)
