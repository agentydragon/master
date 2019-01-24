# Python 3

import sys
import json
import requests
import urllib.parse
import os.path
import glob

d = 'individual-articles'
endpoint = 'localhost:2222'

for file in glob.glob(os.path.join(d, '*', '*', '*.plaintext')):
    print(file)
    with open(file) as f:
        content = f.read()
    if len(content.replace(' ', '').replace('\n', '')) == 0:
        continue
    # default confidence = 0.5
    # default support = 0
    # TODO: could be useful to also use confidence >= 0.2?
    data = {"text": content, "support": 0, "confidence": 0.2}
    r = requests.post('http://' + endpoint + "/rest/annotate",
                      data=urllib.parse.urlencode(data),
                      headers={'content-type':
                               'application/x-www-form-urlencoded',
                               'accept': 'application/json'})
    resultpath = file + '.spotlightjson'
    with open(resultpath, 'w') as f:
        f.write(r.text)
