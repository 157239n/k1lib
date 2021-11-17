.. module:: k1lib.cli

k1lib.cli module
================

The main idea of this package is to emulate the terminal (hence "cli", or "command
line interface"), but doing all of that inside Python itself. So this bash statement:

.. code-block:: console

   cat file.txt | head -5 > headerFile.txt

Turns into this statement::

   cat("file.txt") | head(5) > file("headerFile.txt")

Here, "cat", "head" and "file" are all classes extended
from :class:`~init.BaseCli`. All of
them implements the "reverse or" operation, or __ror__.
Essentially, these 2 statements are equivalent::

   3 | obj
   obj.__ror__(3)

Also, a lot of these tools assume that we are operating
on a table. So this table:

+------+------+------+
| col1 | col2 | col3 |
+======+======+======+
| 1    | 2    | 3    |
+------+------+------+
| 4    | 5    | 6    |
+------+------+------+

Is equivalent to this list::

   [["col1", "col2", "col3"], [1, 2, 3], [4, 5, 6]]

Also, the expected way to use these tools is to import everything directly into the
current environment, like this::

   from k1lib.imports import *

Because there are a lot of clis, you may sometimes unintentionally overwritten an
exposed cli tool. No oworries, every tool is also under the ``cli`` object, meaning
you can use ``deref()`` or ``cli.deref()``.

Besides operating on string iterators alone, this package can also be extra meta,
and operate on streams of strings, or streams of streams of anything. I think this
is one of the most powerful concept of the cli workflow. If this interests you,
check over this:

.. toctree::
   :maxdepth: 1

   streams

All clis tools should work totally fine with PyTorch tensors, but not numpy arrays.
This is because numpy arrays actually implements ``__or__`` operator, which overrides
cli tools' ``__ror__`` operator. Workarounds might look like this::

   # returns (2, 3, 5), works fine
   torch.randn(2, 3, 5) | shape()
   # will not work, returns weird numpy array of shape (2, 3, 5)
   np.random.randn(2, 3, 5) | shape()
   # returns (2, 3, 5), mitigation strategy #1
   shape()(np.random.randn(2, 3, 5))
   # returns (2, 3, 5), mitigation strategy #2
   [np.random.randn(2, 3, 5)] | (item() | shape())

Where to start?
-------------------------

Core clis include :class:`~modifier.apply`, :class:`~modifier.applyS` (its
multiprocessing cousins :class:`~modifier.applyMp` and :class:`~modifier.applyMpBatched`
are great too), :class:`~modifier.op`, :class:`~filt.filt`, :class:`~utils.deref`,
:class:`~utils.item`, :class:`~utils.shape`, :class:`~utils.iden`, so start reading
there first. Then, skim over everything to know what you can do with these
collection of tools. While you're doing that, checkout :meth:`~trace.trace`, for a
quite powerful debugging tool.

There are several `written tutorials <../tutorials.html>`_ about cli here, and I
also made some `video tutorials <https://www.youtube.com/playlist?list=PLP1sw-g877osNI_dMXwR72kVDREeHsYnt>`_
as well, so go check those out.

bio module
-------------------------

.. automodule:: k1lib.cli.bio
   :members:
   :undoc-members:
   :show-inheritance:

entrez module
-------------------------

.. automodule:: k1lib.cli.entrez
   :members:
   :undoc-members:
   :show-inheritance:

mgi module
-------------------------

.. automodule:: k1lib.cli.mgi
   :members:
   :undoc-members:
   :show-inheritance:

filt module
-------------------------

.. automodule:: k1lib.cli.filt
   :members:
   :undoc-members:
   :show-inheritance:

gb module
-------------------------

.. automodule:: k1lib.cli.gb
   :members:
   :undoc-members:
   :show-inheritance:

grep module
-------------------------

.. automodule:: k1lib.cli.grep
   :members:
   :undoc-members:
   :show-inheritance:

init module
-------------------------

.. autoattribute:: k1lib.cli.cliSettings

   Main settings of :mod:`k1lib.cli`. When using::

      from k1lib.cli import *

   ...you can just set the settings like this::

      cliSettings["defaultIndent"] = "\t"

.. _cliSettings:

   There are a few settings:

   - defaultDelim: default delimiter used in-between columns when creating tables
   - defaultIndent: default indent used for displaying nested structures
   - lookupImgs: whether to automatically look up images when exploring something
   - oboFile: gene ontology obo file location
   - strict: whether strict mode is on. Turning it on can help you debug stuff, but
     could also be a pain to work with
   - svgScale: default svg scales for clis that displays graphviz graphs
   - inf: infinity definition for many clis. Defaulted to just ``float("inf")``. Here
     because you might want to temporarily not loop things infinitely.
   - context: context manager to preserve old settings value. Example::

      with cliSettings["context"]():
         cliSettings["inf"] = 21
      # old settings automatically restored

.. autoclass:: k1lib.cli.init.BaseCli
   :members:
   :undoc-members:
   :special-members: __and__, __add__, __or__, __ror__, __lt__, __call__
   :show-inheritance:

.. automodule:: k1lib.cli.init
   :members: serial, oneToMany, manyToMany, manyToManySpecific, fastF
   :undoc-members:
   :show-inheritance:

inp module
-------------------------

.. automodule:: k1lib.cli.inp
   :members:
   :undoc-members:
   :show-inheritance:

kcsv module
-------------------------

.. automodule:: k1lib.cli.kcsv
   :members:
   :undoc-members:
   :show-inheritance:

kxml module
-------------------------

.. automodule:: k1lib.cli.kxml
   :members:
   :undoc-members:
   :show-inheritance:

modifier module
-------------------------

.. automodule:: k1lib.cli.modifier
   :members:
   :undoc-members:
   :show-inheritance:

output module
-------------------------

.. automodule:: k1lib.cli.output
   :members:
   :undoc-members:
   :show-inheritance:

sam module
-------------------------

.. automodule:: k1lib.cli.sam
   :members:
   :undoc-members:
   :show-inheritance:

structural module
-------------------------

.. currentmodule:: k1lib.cli.structural

.. automodule:: k1lib.cli.structural
   :members:
   :exclude-members: joinStreamsRandom
   :undoc-members:
   :show-inheritance:

   .. attribute:: yieldSentinel

      Object that can be yielded in a stream to ignore this stream for the moment in
      :class:`joinStreamsRandom`. It will also stops :class:`~k1lib.cli.utils.deref`
      early.

   .. autoclass:: joinStreamsRandom
      :members:

trace module
-------------------------

.. automodule:: k1lib.cli.trace
   :members:
   :undoc-members:
   :show-inheritance:

utils module
-------------------------

.. automodule:: k1lib.cli.utils
   :members:
   :undoc-members:
   :show-inheritance:

others module
-------------------------

.. automodule:: k1lib.cli.others
   :members:
   :undoc-members:
   :show-inheritance:

There are a couple monkey-patched clis:

.. automethod:: torch.stack

Elsewhere in the library
-------------------------

There might still be more cli tools scattered around the library. These are pretty
rare, quite dynamic and most likely a cool extra feature, not a core functionality,
so not worth it/can't mention it here. Anyway, execute this::

   cli.scatteredClis()

to get a list of them.
