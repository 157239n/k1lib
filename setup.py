#!/usr/bin/env python

from setuptools import find_packages, setup
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    with open("readme.md") as f:
        md = f.read()
except:
    md = ""

deps = ["graphviz", "torchvision", "pillow",
        "scikit-image", "pyperclip", "k1a>=1.2,<2", "torch"]

# ('k1lib/k1ui', ['k1lib/k1ui/mouseKey.pth', 'k1lib/k1ui/256.model.state_dict.pth']), used too much space

setup(
    name="k1lib",
    packages=["k1lib", "k1lib._hidden",
              "k1lib.cli", "k1lib.assets",
              "k1lib.callbacks", "k1lib.callbacks.profilers",
              "k1lib.callbacks.lossFunctions",
              "k1lib._mo", "k1lib.serve", "k1lib.k1ui"],
    data_files=[('k1lib/serve', ['k1lib/serve/main.html']),
                ('k1lib', ['k1lib/pw_top100k_bloom.bin']),
                ('k1lib/assets', ['k1lib/assets/k1js_amd.js', 'k1lib/assets/k1js_umd.js', 'k1lib/assets/acorn.js', 'k1lib/assets/acorn_walk.js', 'k1lib/assets/chartist.js', 'k1lib/assets/chartist.css', 'k1lib/assets/leaflet.js', 'k1lib/assets/leaflet.css'])],
    version="1.8.1", # remember to also modify this number in __init__.py
    python_requires='>=3.7',
    install_requires=["numpy>=1.14", "matplotlib>=2.0", "dill", "forbiddenfruit", "wurlitzer", "validators"],
    extras_require={"all": deps},
    description="Some nice ML overhaul",
    url="https://k1lib.com",
    author="Quang Ho",
    author_email="157239q@gmail.com",
    long_description=md,
    long_description_content_type='text/markdown',
    include_package_data=True,
    license="MIT",
)
