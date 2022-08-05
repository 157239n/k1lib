#!/usr/bin/env python3

from k1lib.imports import *
import os
import sys

"""
To build everything: `./compile.py`

To build only the docs, skipping the tutorials: `./compile.py 0`
"""

os.system(f"./_compile.sh {k1lib.__version__} {' '.join(sys.argv[1:])}")

links = [
    "https://k1lib.com/latest/index.html",
    "https://k1lib.com/latest/base.html",
    "https://k1lib.com/latest/cli/index.html",
    "https://k1lib.com/latest/callbacks/index.html",
    "https://k1lib.com/latest/kdata.html",
    "https://k1lib.com/latest/eqn.html",
    "https://k1lib.com/latest/fmt.html",
    "https://k1lib.com/latest/graphEqn.html",
    "https://k1lib.com/latest/imports.html",
    "https://k1lib.com/latest/mo.html",
    "https://k1lib.com/latest/schedule.html",
    "https://k1lib.com/latest/selector.html",
    "https://k1lib.com/latest/viz.html",
    "https://k1lib.com/latest/monkey.html",
    "https://k1lib.com/latest/tutorials.html",
]

htmlE = lambda e, extras="": aS(lambda x: f"<{e}{extras}>{x}</{e}>")
lastUpdated = k1.now().split("T")[0]

sitemapFile = os.path.dirname(os.path.realpath(
    __file__)) + "/../../k1lib.github.io/sitemap.xml" | aS(os.path.realpath)

links | apply(htmlE("loc")) | (wrapList() | insert(lastUpdated | htmlE("lastmod"), begin=False) | insert("<changefreq>weekly</changefreq>", begin=False)).all()\
    | (join("") | htmlE("url")).all() | join("\n") | htmlE("urlset", ' xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')\
    | wrapList() | insert('<?xml version="1.0" encoding="UTF-8"?>') | file(sitemapFile)
