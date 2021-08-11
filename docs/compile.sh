#!/bin/bash

# some functions within the package triggers automatic
# plotting, so this is a signal to prevent that
export SPHINX=1

rm -r _build

#sphinx-apidoc -f -o . ../k1lib
#sphinx-apidoc -o . ../k1lib
make html

rm -r ../../k1lib.github.io/*
cp -r _build/html/* ../../k1lib.github.io/

