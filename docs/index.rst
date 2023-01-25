.. module:: k1lib

k1lib library
=============

PyTorch is awesome, and it provides a very effective way to execute ML code fast. What
it lacks is surrounding infrastructure to make general debugging and discovery process
better. Other more official wrapper frameworks sort of don't make sense to me, so this
is an attempt at recreating a robust suite of tools that makes sense.

This is more than just an ML library though. A prominent feature is the set of "cli tools"
originally intended to replace the bash/awk/perl bioinformatics workflow. It essentially
allows you to pipe inputs into functions, which returns an output which can be piped into
other functions. Using these tools, you can literally perform complex operations in multiple
dimensions in 2-3 lines of code that would normally take >100 lines. It's also super
flexible, operates on multiple dimensions and not locked in, as you can change the
dataflow in quite a fundamental level in ~5 minutes. Check over the basics of it
here: :mod:`k1lib.cli`.

After doing that, you can check out the tutorials to get a large overview of how everything
integrates together nicely.

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
   eqn
   fmt
   graphEqn
   imports
   mo
   knn
   p5
   schedule
   selector
   serve
   viz

Installation
------------

Just do this::

   pip install k1lib[all]

If you can't install the optional extra dependencies for some reason then do this::

   pip install k1lib

Then in a notebook, do this::

   from k1lib.imports import *

I've found importing all symbols work best for my day-to-day use, and it makes
cli tools more pleasant to use. However, if you're those diehard programmers
who sworn to never import all, then you can just do `import k1lib` instead.
Still, look over the `k1lib.imports` module to know what you should import.

This library has very few dependencies, and all of them are very commonly used.
The library has a soft dependency on PyTorch. It will run fine without PyTorch, but
a lot of functionalities related to deep learning will not work. While tests are
rigorously run in an environment where PyTorch is installed, they're not run for
environments that don't, so strange bugs may appear.

Repo is at https://github.com/157239n/k1lib/ btw. Also, if you have anything that
looks strange, use the search bar on the top left to quickly lookup stuff.

.. toctree::
   :hidden:

   monkey
   tutorials
   changelogs
