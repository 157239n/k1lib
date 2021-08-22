#!/usr/bin/env python3

from glob import glob
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

os.system("rm -r tutorials")
os.system("mkdir tutorials")

# generate docs
for f in glob("*.ipynb"):
    os.system(f"jupyter nbconvert {f} --to html --output-dir='tutorials'")

