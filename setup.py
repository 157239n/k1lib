#!/usr/bin/env python3

from setuptools import find_packages, setup
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

setup(
    name="k1lib",
    packages=["k1lib", "k1lib._hidden", "k1lib._callbacks"],
    version="0.1.0",
    install_requires=["torch", "numpy", "matplotlib", "dill"],
    description="Some nice ML overhaul",
    url="https://github.com/157239n/k1lib",
    author="Quang Ho",
    author_email="157239q@gmail.com",
    license="MIT",
)

