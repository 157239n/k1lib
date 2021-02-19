#!/bin/bash

cd $1
python $1/setup.py bdist_wheel
pip install --force-reinstall $1/dist/k1lib-0.1.0-py3-none-any.whl
