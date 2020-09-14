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


def already_done(resultpath):
    try:
        with open(file) as f:
            p = json.load(f)
        return True
    except:
        return False


married = """0e/a3/La_Malinche.xml.plaintext
0e/ac/Czechoslovakia.xml.plaintext
0e/5a/Aristide_Maillol.xml.plaintext
b7/da/Haggai.xml.plaintext
b7/bc/Emma_Abbott.xml.plaintext
6b/5f/James_Blaylock.xml.plaintext
6b/00/Douglas_Adams.xml.plaintext
6b/19/Hedwig_of_Silesia.xml.plaintext
6b/71/Greece.xml.plaintext
55/8f/Marshall_McLuhan.xml.plaintext
55/b8/Old_Catholic_Church.xml.plaintext
55/4f/Elagabalus.xml.plaintext
5f/9d/Gary_Coleman.xml.plaintext
5f/a4/Mel_Brooks.xml.plaintext
5f/fb/George_Benson.xml.plaintext
5f/eb/Russia.xml.plaintext
6f/a4/Musical_theatre.xml.plaintext
6f/a3/Mehmed_the_Conqueror.xml.plaintext
6f/e5/Karlheinz_Stockhausen.xml.plaintext
6f/c1/Nostradamus.xml.plaintext
6f/74/Hugh_Hefner.xml.plaintext
f3/c9/%60Abdu%27l-Bah%C3%A1.xml.plaintext
f3/a6/Jakarta.xml.plaintext
f3/ac/Bethlehem.xml.plaintext
f3/25/Herman_Melville.xml.plaintext
2f/99/Scott_Adams.xml.plaintext
2f/e9/Hugh_Binning.xml.plaintext
2f/e3/Jorge_Luis_Borges.xml.plaintext
2f/25/Hezekiah.xml.plaintext
2f/3f/Bob_Jones_University.xml.plaintext
64/2c/Liberia.xml.plaintext
64/2c/Kurt_Vonnegut.xml.plaintext
64/79/Eleanor_of_Aquitaine.xml.plaintext
9b/88/Bill_Holbrook.xml.plaintext
9b/f1/Julio-Claudian_dynasty.xml.plaintext
f7/2f/Mike_Moore_%28New_Zealand_politician%29.xml.plaintext
f7/1f/Bohdan_Khmelnytsky.xml.plaintext
17/e1/History_of_modern_Greece.xml.plaintext
17/b7/Condom.xml.plaintext
17/cd/Hecate.xml.plaintext
17/ba/Ottonian_dynasty.xml.plaintext
67/d6/Felix_Bloch.xml.plaintext
67/bb/George_Whipple.xml.plaintext
67/6e/Empress_Gensh%C5%8D.xml.plaintext
67/c7/Nastassja_Kinski.xml.plaintext
db/fd/Jefferson_Davis.xml.plaintext
db/4f/Barry_Goldwater.xml.plaintext
db/bf/Agnosticism.xml.plaintext
62/2e/Satires_%28Juvenal%29.xml.plaintext
62/08/John_Hanson.xml.plaintext
62/b9/Ken_Kesey.xml.plaintext
69/f4/Stephen_Bachiler.xml.plaintext
69/02/Society_for_Creative_Anachronism.xml.plaintext
69/12/Henry_Bruce%2C_1st_Baron_Aberdare.xml.plaintext
69/56/Richard_III_of_England.xml.plaintext
69/bd/Heracles.xml.plaintext
a1/90/Shah_Jahan.xml.plaintext
e7/a8/Pope_Urban_III.xml.plaintext
e7/81/History_of_Lithuania.xml.plaintext
e7/11/Giovanni_Boccaccio.xml.plaintext
0b/d3/Bing_Crosby.xml.plaintext
0b/8c/Charles_Evers.xml.plaintext
0b/85/Nj%C3%B6r%C3%B0r.xml.plaintext
36/ea/American_Civil_Liberties_Union.xml.plaintext
36/ce/T._S._Eliot.xml.plaintext
36/6e/Robert_Byrd.xml.plaintext
f8/44/Neville_Chamberlain.xml.plaintext
f8/1b/Marquette%2C_Michigan.xml.plaintext
f8/ae/Miss_Marple.xml.plaintext
c4/ad/Anthony_of_Saxony.xml.plaintext
31/60/Oswald_Spengler.xml.plaintext
31/3c/Falstaff.xml.plaintext
31/1b/Li_Bai.xml.plaintext
31/12/Andromeda_%28mythology%29.xml.plaintext
9d/a2/Colin_Dexter.xml.plaintext
9d/96/Claude_Auchinleck.xml.plaintext
9d/0f/Stephen_King.xml.plaintext
b2/69/Amalasuntha.xml.plaintext
b2/ce/Reno%2C_Nevada.xml.plaintext
32/62/Roger_Penrose.xml.plaintext
32/f6/Murray_Rothbard.xml.plaintext
32/88/Jerome_Kern.xml.plaintext""".split('\n')
married = map(lambda x: os.path.join(d, x), married)


# for file in glob.glob(os.path.join(d, '*', '*', '*.plaintext')):
for file in married:
    print(file)
    with open(file) as f:
        content = f.read()
    resultpath = file + '.corenlpjson'
    if already_done(resultpath):
        print('already done')
        continue

    properties = {"annotators": "tokenize,ssplit", "outputFormat": "json"}
    r = requests.post('http://' + endpoint + "/?properties=" +
                      urllib.parse.quote_plus(json.dumps(properties)),
                      data=content.encode('utf-8'))
    resultpath = file + '.corenlpjson'
    with open(resultpath, 'w') as f:
        f.write(r.text)
