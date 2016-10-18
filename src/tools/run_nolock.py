#!/usr/bin/env python3

import sys
import subprocess
import tempfile

# Invocation: ./run_nolock.py (Bazel target) (args for target)
# NOTE: No need to add '--'.

f = tempfile.NamedTemporaryFile(delete=False)
f.close()

rv = subprocess.call([
    'bazel',
    'run',
    '--script_path',
    f.name,
    sys.argv[1],
    '--',
] + sys.argv[2:])
if rv != 0:
    sys.exit(rv)

rv = subprocess.call([f.name])
if rv != 0:
    sys.exit(rv)
