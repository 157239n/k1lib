#!/usr/bin/env python3

from setuptools import find_packages, setup
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

setup(
    name="k1lib",
    packages=["k1lib", "k1lib._hidden", "k1lib._callbacks"],
    version="0.1.0",
    description="Some nice ML overhaul",
    author="Quang Ho",
    license="MIT",
)

