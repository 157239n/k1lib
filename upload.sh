#!/bin/bash

dir=`dirname "$0"`
cd "$dir"

rm -r build dist k1lib.egg-info __pycache__
#pip uninstall -y k1lib
./setup.py sdist
./setup.py bdist
./setup.py bdist_wheel
twine upload dist/*

