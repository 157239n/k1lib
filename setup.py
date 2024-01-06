#!/usr/bin/env python3

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

setup(
    name="k1lib",
    packages=["k1lib", "k1lib._hidden",
              "k1lib.cli",
              "k1lib.callbacks", "k1lib.callbacks.profilers",
              "k1lib.callbacks.lossFunctions",
              "k1lib._mo", "k1lib.serve", "k1lib.k1ui"],
    data_files=[('k1lib/serve', ['k1lib/serve/main.html']),
                ('k1lib/k1ui', ['k1lib/k1ui/mouseKey.pth', 'k1lib/k1ui/256.model.state_dict.pth'])],
    version="1.5",
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
