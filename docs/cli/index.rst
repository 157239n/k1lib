.. module:: k1lib.cli

k1lib.cli module
================

Setup
-----

To install the library, run this in a terminal:

.. code-block:: console

   pip install k1lib[all]

If you don't want to install extra dependencies (not recommended), you can do this instead:

.. code-block:: console

   pip install k1lib

To use it in a python file or a notebook, do this::

   from k1lib.imports import *

Because there are a lot of functions with common names, you may have custom functions or
classes that have the same name, which will override the functions in the library. If you
want to use them, you can use ``cli.sort()`` instead of ``sort()`` for example.

Intro
-----

The main idea of this package is to emulate the terminal (hence "cli", or "command
line interface"), but doing all of that inside Python itself. So this bash statement:

.. code-block:: console

   cat file.txt | head -5 > headerFile.txt

Turns into this statement::

   cat("file.txt") | head(5) > file("headerFile.txt")

Let's step back a little bit. In the bash statement, "cat" and "head" are actual programs
accessible through the terminal, and "|" will pipe the output of 1 program into another
program. ``cat file.txt`` will read a file and returns a list of all rows in it, which
will then be piped into ``head -5``, which will only return the first 5 lines. Finally,
``> headerFile.txt`` will redirect the output to the "headerFile.txt" file. See this video
for more: https://www.youtube.com/watch?v=bKzonnwoR2I

On the Python side, "cat", "head" and "file" are Python classes extended from :class:`~init.BaseCli`.
``cat("file.txt")`` will read the file line by line, and return a list of all of them. ``head(5)``
will take in that list and return a list with only the first 5 lines. Finally, ``> file("headerFile.txt")``
will take that in and writes it to a file.

You can even integrate with existing shell commands::

   ls("~") | cmd("grep *.so")

Here, "ls" will list out files inside the home directory, then pipes it into regular
grep on linux, which is then piped back into Python as a list of strings. So it's
equivalent to this bash statement:

.. code-block:: console

   ls | grep *.so

Let's see a really basic example::

   # just a normal function
   f = lambda x: x**2
   # returns 9, no surprises here
   f(3)
   # f is now a cli tool
   f = aS(lambda x: x**2)
   # returns 9, demonstrating that they act like normal functions
   f(3)
   # returns 9, demonstrating that you can also pipe into them
   3 | f

You can think of the flow of these clis in terms of 2 phases. 1 is configuring what you
want the cli to do, and 2 is actually executing it. Let's say you want to take a list
of numbers and take the square of them::

   # configuration stage. You provide a function to `apply` to tell it what to apply to each element in the list
   f = apply(lambda x: x**2)
   # initialize the input
   x = range(5)
   # execution stage, normal style, returns [0, 1, 4, 9, 16]
   list(f(x))
   # execution stage, pipe style, returns [0, 1, 4, 9, 16]
   list(x | f)
   
   # typical usage: combining configuration stage and execution stage, returns [0, 1, 4, 9, 16]
   list(range(5) | apply(lambda x: x**2))
   # refactor converting to list so that it uses pipes, returns [0, 1, 4, 9, 16]
   range(5) | apply(lambda x: x**2) | aS(list)

You may wonder why do we have to turn it into a list. That's because all cli tools execute
things lazily, so they will return iterators, instead of lists. Here's how iterators work::

   def gen(): # this is a generator. It generates elements
       yield 3
       print("after yielding 3")
       yield 2
       yield 5
   for e in gen():
       print(e)

It will print this out:

.. code-block:: text

   3
   after yielding 3
   2
   5

So, iterators feels like lists. In fact, a list is an iterator, ``range(5)``, numpy arrays
and strings are also iterators. Basically anything that you can iterate through is an
iterator. The above iterator is a little special, as it's specifically called a "generator".
They are actually a really cool aspect of Python, in terms of they execute code lazily, meaning
``gen()`` won't run all the way when you call it. In fact, it doesn't run at all. Only once you
request new elements when trying to iterate over it will the function run.

All cli tools utilize this fact, in terms of they will not actually execute anything unless you
force them to::

   # returns "<generator object apply.__ror__.<locals>.<genexpr> at 0x7f7ae48e4d60>"
   range(5) | apply(lambda x: x**2)
   # you can iterate through it directly:
   for element in range(5) | apply(lambda x: x**2):
       print(element)
   # returns [0, 1, 4, 9, 16], in case you want it in a list
   list(range(5) | apply(lambda x: x**2))
   # returns [0, 1, 4, 9, 16], demonstrating deref
   range(5) | apply(lambda x: x**2) | deref()

In the first line, it returns a generator, instead of a normal list, as nothing has actually been
executed. You can still iterate through generators using for loops as usual, or you can convert it
into a list. When you get more advanced, and have iterators nested within iterators within iterators,
you can use :class:`~utils.deref` to turn all of them into lists.

Also, a lot of these tools (like :class:`~modifier.apply` and :class:`~filt.filt`)
sometimes assume that we are operating on a table. So this table:

+------+------+------+
| col1 | col2 | col3 |
+======+======+======+
| 1    | 2    | 3    |
+------+------+------+
| 4    | 5    | 6    |
+------+------+------+

Is equivalent to this list::

   [["col1", "col2", "col3"], [1, 2, 3], [4, 5, 6]]

:class:`~structural.transpose` and :class:`~init.mtmS` provides more flexible ways
to transform a table structure (but usually involves more code).

Besides operating on string iterators alone, this package can also be extra meta,
and operate on streams of strings, or streams of streams of anything. I think this
is one of the most powerful concept of the cli workflow. Check over it here:

.. toctree::
   :maxdepth: 1

   streams

All cli tools should work fine with :class:`torch.Tensor`, :class:`numpy.ndarray` and :class:`pandas.core.series.Series`,
but k1lib actually modifies Numpy arrays and Pandas series deep down for it to work.
This means that you can still do normal bitwise or with a numpy float value, and
they work fine in all regression tests that I have, but you might encounter strange bugs.
You can disable it manually by changing :attr:`~k1lib.settings`.startup.or_patch. If you
chooses to do this, you have to be careful and use these workarounds::

   # returns (2, 3, 5), works fine
   torch.randn(2, 3, 5) | shape()
   # will not work, returns weird numpy array of shape (2, 3, 5)
   np.random.randn(2, 3, 5) | shape()
   # returns (2, 3, 5), mitigation strategy #1
   shape()(np.random.randn(2, 3, 5))
   # returns (2, 3, 5), mitigation strategy #2
   [np.random.randn(2, 3, 5)] | (item() | shape())

All cli-related settings are at :attr:`~k1lib.settings`.cli.

Where to start?
-------------------------

Core clis include:

- :class:`~modifier.apply`, :class:`~modifier.aS`, :class:`~modifier.op`, :class:`~grep.grep`
- :class:`~filt.filt`, :class:`~filt.head`, :class:`~filt.rows`, :class:`~filt.cut`
- :class:`~utils.deref`, :class:`~utils.item`, :class:`~utils.shape`
- :class:`~structural.transpose`, :class:`~structural.joinStreams`, :class:`~structural.batched`, :class:`~structural.count`
- :meth:`~inp.cat`, :meth:`~inp.ls`, :class:`~output.file`, :class:`~output.stdout`

These clis are pretty important, and are used all the time, so look over
them to see what the library can do. Whenever you find some cli you have
not encountered before, you can just search it in the search bar on the
top left of the page.

Then other important, not necessarily core clis include:

- :class:`~modifier.applyMp`, :class:`~modifier.sort`, :class:`~modifier.randomize`
- :class:`~utils.wrapList`, :class:`~utils.ignore`, :class:`~inp.cmd`
- :class:`~structural.repeat` and friends, :class:`~structural.groupBy`

So, start reading over what these do first, as you can pretty much 95% utilize everything
the cli workflow has to offer with those alone. Then skim over basic conversions in
module :mod:`~k1lib.cli.conv`. While you're doing that, checkout :meth:`~trace.trace`,
for a quite powerful debugging tool.

There are several `written tutorials <../tutorials.html>`_ about cli here, and I
also made some `video tutorials <https://www.youtube.com/playlist?list=PLP1sw-g877osNI_dMXwR72kVDREeHsYnt>`_
as well, so go check those out.

For every example in the tutorials that you found, you might find it useful to follow
the following debugging steps, to see how everything works::

   # assume there's this piece of code:
   A | B | C | D
   # do this instead:
   A | deref()
   # once you understand it, do this:
   A | B | deref()

   # assume there's this piece of code:
   A | B.all() | C
   # do this instead:
   A | item() | B | deref()
   # once you understand it, you can move on:
   A | B.all() | deref()

   # assume there's this piece of code:
   A | (B & C)
   # do this instead:
   A | B | deref()

   # assume there's this piece of code:
   A | (B + C)
   # do these instead:
   A | deref() | op()[0] | B | deref()
   A | deref() | op()[1] | C | dereF()
   # there are alternatives to that:
   A | item() | B | deref()
   A | rows(1) | item() | C | deref()

Finally, you can read over the summary below, see what catches your eye and
check that cli out.

Summary
-------------------------

.. include:: ../literals/cli-tables.rst

Under the hood
-------------------------

How it works underneath is pretty simple. All cli tools implement the "reverse or"
operation, or __ror__. So essentially, these 2 statements are equivalent::

   3 | obj
   obj.__ror__(3)

There are several other operations that certain clis can override, like ">" or ">>".
Also, if you're an advanced user, there's also an optimizer that looks like LLVM, so
you can implement optimization passes to speed up everything by a lot:

.. toctree::
   :maxdepth: 1

   llvm

Biology-related clis
***********************

I separated these out because they might not be interesting to the majority of users.

.. include:: ../literals/cli-bio-tables.rst

bio module
-------------------------

.. automodule:: k1lib.cli.bio
   :members:
   :undoc-members:
   :show-inheritance:

cif module
-------------------------

.. automodule:: k1lib.cli.cif
   :members:
   :undoc-members:
   :show-inheritance:

conv module
-------------------------

.. automodule:: k1lib.cli.conv
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

.. autoclass:: k1lib.cli.init.BaseCli
   :members:
   :undoc-members:
   :special-members: __and__, __add__, __or__, __ror__, __lt__, __call__
   :show-inheritance:

.. automodule:: k1lib.cli.init
   :members: serial, oneToMany, mtmS, fastF
   :undoc-members:
   :show-inheritance:

   .. attribute:: yieldT

      Object often used as a sentinel, or an identifying token in lots of clis,
      including
      that can be yielded in a stream to ignore this stream for the moment in
      :class:`~k1lib.cli.structural.joinStreamsRandom`, :class:`~k1lib.cli.utils.deref`,
      :class:`~k1lib.cli.typehint.tCheck` and :class:`~k1lib.cli.typehint.tOpt`

inp module
-------------------------

.. automodule:: k1lib.cli.inp
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: k1lib.cli.inp.cat.pickle

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

nb module
-------------------------

.. automodule:: k1lib.cli.nb
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

typehint module
-------------------------

.. automodule:: k1lib.cli.typehint
   :members:
   :undoc-members:
   :show-inheritance:

optimizations module
-------------------------

.. automodule:: k1lib.cli.optimizations
   :members:
   :undoc-members:
   :show-inheritance:

Elsewhere in the library
-------------------------

There might still be more cli tools scattered around the library. These are pretty
rare, quite dynamic and most likely a cool extra feature, not a core functionality,
so not worth it/can't mention it here. Anyway, execute this::

   cli.scatteredClis()

to get a list of them.
