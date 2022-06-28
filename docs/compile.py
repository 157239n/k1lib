#!/usr/bin/env python3

import k1lib
import os
import sys

"""
To build everything: `./compile.py`

To build only the docs, skipping the tutorials: `./compile.py 0`
"""

os.system(f"./_compile.sh {k1lib.__version__} {' '.join(sys.argv[1:])}")
