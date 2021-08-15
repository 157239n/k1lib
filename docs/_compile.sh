#!/bin/bash

# expected a version number as the first argument

# also expected the directory structure to look like this:
# ~/repos/labs/
#     k1lib/
#         docs/
#     k1lib.github.io/

# some functions within the package triggers automatic plotting (for convenience sake), so this is a signal to prevent that
export SPHINX=1

# building stuff
rm -r _build
make html

# copying over to k1lib.github,io/ folder. Expected this to not be inside any
# folders, as there are lots of absolute references
base=../../k1lib.github.io
vBase=$base/$1/ # versioned base
rm -r $vBase
mkdir $vBase
cp -r _build/html/* $vBase
echo $1 > $base/version.txt # so that index.html know what version to redirect to

