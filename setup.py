#!/usr/bin/env python3

from setuptools import find_packages, setup
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    with open("readme.md") as f:
        md = f.read()
except:
    md = ""

setup(
    name="k1lib",
    packages=["k1lib", "k1lib._hidden",
              "k1lib.cli",
              "k1lib.callbacks", "k1lib.callbacks.profilers",
              "k1lib.callbacks.lossFunctions",
              "k1lib._mo"],
    version="0.16",
    python_requires='>=3.7',
    install_requires=["torch", "numpy>=1.14", "matplotlib>=2.0", "dill"],
    extras_require={"extras": ["graphviz", "torchvision",
                               "pillow", "scikit-image", "pyperclip", "forbiddenfruit"]},
    description="Some nice ML overhaul",
    url="https://github.com/157239n/k1lib",
    author="Quang Ho",
    author_email="157239q@gmail.com",
    long_description=md,
    long_description_content_type='text/markdown',
    license="MIT",
)
