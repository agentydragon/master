# Python 3

import sys
import json
import requests
import urllib.parse
import os.path
import glob

d = 'individual-articles'

file = 'individual-articles/0e/b7/Doctor_V64.xml.plaintext'
with open(file) as f:
    text = f.read()
with open(file + '.corenlpjson') as f:
    corenlpjson = json.load(f)
for sentence in corenlpjson["sentences"]:
    print(sentence)
    begin = sentence["tokens"][0]["characterOffsetBegin"]
    end = sentence["tokens"][-1]["characterOffsetEnd"]
    print("$$$", text[begin:end])
