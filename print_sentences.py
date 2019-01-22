# Python 3

import sys
import json
import requests
import urllib.parse
import os.path
import glob

d = 'individual-articles'

for file in glob.glob(os.path.join(d, '*', '*', '*.plaintext')):
    print(file)
    with open(file) as f:
        text = f.read()
    with open(file + '.corenlpjson') as f:
        corenlpjson = json.load(f)
    if len(corenlpjson["sentences"]) == 0:
        continue
    for sentence in corenlpjson["sentences"]:
        begin = sentence["tokens"][0]["characterOffsetBegin"]
        end = sentence["tokens"][-1]["characterOffsetEnd"]
        print("$$$", text[begin:end])
    break
