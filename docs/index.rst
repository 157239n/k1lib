.. module:: k1lib

k1lib library
=============

This is a library that has nice PyTorch overhauls that lets you train models
effortlessly. There's also the module :mod:`k1lib.cli` that's great for manipulating
lists and iterators. Finally, it has quality of life features scattered throughout.
Check out the tutorials to get a feel of what the library can do.

.. toctree::
   :maxdepth: 1

   base

Subpackages
-----------

.. toctree::
   :maxdepth: 1

   cli/index
   callbacks/index

Submodules
----------

.. toctree::
   :maxdepth: 1

   kdata
   eqn
   fmt
   graphEqn
   imports
   mo
   knn
   schedule
   selector
   viz

Installation
------------

Just do this::

   pip install k1lib[extras]

If you can't install the optional extra dependencies then do this::

   pip install k1lib

Then in a notebook, do this::

   from k1lib.imports import *

This library has very few dependencies, and all of them are very commonly used

Repo is at https://github.com/157239n/k1lib/ btw. Also, the search bar is your
friend!

.. toctree::
   :hidden:

   monkey
   tutorials
   changelogs
