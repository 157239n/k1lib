.. module:: k1lib

k1lib library
=============

PyTorch is awesome, and it provides a very effective way to execute ML code fast. What
it lacks is surrounding infrastructure to make general debugging and discovery process
better. Other more official wrapper frameworks sort of don't make sense to me, so this
is an attempt at recreating a robust suite of tools that makes sense.

Also, there's the package :mod:`k1lib.cli` which contains nice cli tools originally intended
to replace the bash/awk/perl bioinformatics workflow. What does this have to do with
PyTorch and DL? Originally nothing, but over time stuff like `batched` and `stagger`
appeared which has largely replaced PyTorch data loaders.

This cli stuff is quite insane man. You can literally perform extremely complex
operations in 2-3 lines of code that would normally take >100 lines. It's also super
flexible, operates on multiple dimensions and not locked in, as you can change the
dataflow in quite a fundamental level in ~5 minutes. It's like alchemy. Although I
created it, I'm continously surprised at what it can do. Check
`this post <https://mlexps.com/mo/3-cif-visualize/>`_ where cli is used to load,
transform, analyze and visualize protein structural data.

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

   k1a
   k1ui
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

If you're on Windows, do this::

   pip install k1lib[extras_windows]

This will install all extra dependencies, except for `k1a`, which is a supplementary
library to accelerate functionalities within this library. If you can't install the
optional extra dependencies for some reason then do this::

   pip install k1lib

Then in a notebook, do this::

   from k1lib.imports import *

I've found importing all symbols work best for my day-to-day use, and it makes
cli tools more pleasant to use. However, if you're those diehard programmers
who sworn to never import all, then you can just do `import k1lib` instead.
Still, look over the `k1lib.imports` module to know what you should import.

This library has very few dependencies, and all of them are very commonly used

Repo is at https://github.com/157239n/k1lib/ btw. Also, the search bar is your
friend, as there're lots of stuff here.

.. toctree::
   :hidden:

   monkey
   tutorials
   changelogs
