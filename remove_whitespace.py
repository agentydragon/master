# Python 3

import os.path
import glob

d = 'individual-articles'

for file in glob.glob(os.path.join(d, '*', '*', '*.plaintext')):
    with open(file) as f:
        content = f.read()
    with open(file, 'w') as f:
        f.write(content.strip())
