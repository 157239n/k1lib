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

Here, :class:`~modifier.aS` is pretty much the simplest cli available. It just makes whatever
function you give it pipe-able, as you can't quite pipe things to lambda functions in vanilla Python.

You can think of the flow of these clis in terms of 2 phases. 1 is configuring what you
want the cli to do, and 2 is actually executing it. Let's say you want to take a list
of numbers and take the square of them::

   # configuration stage. You provide a function to `apply` to tell it what function to apply to each element in the list, kinda like Python's "map" function
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

   def gen(): # this is a generator, a special type of iterator. It generates elements
       yield 3
       print("after yielding 3")
       yield 2
       yield 5
   for e in gen():
       print("in for loop:", e)

It will print this out:

.. code-block:: text

   in for loop: 3
   after yielding 3
   in for loop: 2
   in for loop: 5

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

.. warning::

   If you're not an advanced user, just skip this warning.

   All cli tools should work fine with :class:`torch.Tensor`, :class:`numpy.ndarray` and :class:`pandas.core.series.Series`,
   but k1lib actually modifies Numpy arrays and Pandas series deep down for it to work.
   This means that you can still do normal bitwise or with a numpy float value, and
   they work fine in all regression tests that I have, but you might encounter strange bugs.
   You can disable it manually by changing :attr:`~k1lib.settings`.startup.or_patch like this::

      import k1lib
      k1lib.settings.startup.or_patch.numpy = False
      from k1lib.imports import *

   If you choose to do this, you'll have to be careful and use these workarounds::

      torch.randn(2, 3, 5) | shape()                  # returns (2, 3, 5), works fine
      np.random.randn(2, 3, 5) | shape()              # will not work, returns weird numpy array of shape (2, 3, 5)
      shape()(np.random.randn(2, 3, 5))               # returns (2, 3, 5), mitigation strategy #1
      [np.random.randn(2, 3, 5)] | (item() | shape()) # returns (2, 3, 5), mitigation strategy #2

   Again, please note that you only need to do these workarounds if you choose to turn off C-type
   modifications. If you keep things by default, then all examples above should work just fine.

All cli-related settings are at :attr:`~k1lib.settings`.cli.

Argument expansion
------------------

I'd like to quickly mention the argument expansion motif that's prominent in some cli tools. Check out this example::

   [3, 5] | aS(lambda a: a[0] + a[1]) # returns 8, long version, not descriptive elements ("a[0]" and "a[1]")
   [3, 5] | ~aS(lambda x, y: x + y) # returns 8, short version, descriptive elements ("x" and "y")

   [[3, 5], [2, 7]] | apply(lambda a: a[0] + a[1]) | aS(list) # returns [8, 9], long version
   [[3, 5], [2, 7]] | ~apply(lambda x, y: x + y) | aS(list) # returns [8, 9], short version

Here, the tilde operator ("~", officially called "invert" in Python) used on :class:`~modifier.aS` and
:class:`~modifier.apply` means that the input object/iterator will be expanded so that it fills all
available arguments. This is a small quality-of-life feature, but makes a big difference, as parameters
can now be named separately and nicely ("x" and "y", which can convey that this is a coordinate of some
sort, instead of "a[0]" and "a[1]", which conveys nothing).

Inverting conditions
--------------------

The tilde operator does not always mean expanding the arguments though. Sometimes it's used for actually
inverting the functionality of some clis::

   range(5) |  filt(lambda x: x % 2 == 0) | aS(list) # returns [0, 2, 4]
   range(5) | ~filt(lambda x: x % 2 == 0) | aS(list) # returns [1, 3]

   [3, 5.5, "text"] | ~instanceOf(int) | aS(list) # returns [5.5, "text"]

Capturing operators
-------------------

Some clis have the ability to "capture" the behavior of other clis and modify them on the fly. For
example, let's see tryout(), which catches errors in the pipeline and returns a default value if
an error is raised::

    "a3" | (tryout(4) | aS(int)) | op()*2 # returns 8, because int("a3") will throws an error, which will be caught, and the pipeline reduces down to 4*2
    "3"  | (tryout(4) | aS(int)) | op()*2 # returns 6, because int("3") will not throw an error, and the pipeline effectively reduces down to int("3")*2
    "3"  |  tryout(4) | aS(int)  | op()*2 # throws an error, because tryout() doesn't capture anything

Just a side note, op() will record all operations done on it, and it will replay those operations
on anything that's piped into it.

In the first line, ``tryout() | aS(int)`` will be executed first, which will lead to tryout()
capturing all of the clis behind it and injecting in a try-catch code block to wrap all of them
together. In the third line, it doesn't work because ``"3" | tryout(4)`` is executed first,
but here, tryout() doesn't have the chance to capture the clis behind it, so it can't inject
a try-catch block around them. This also means that in the 1st and 2nd line, the final multify-by-2
step is not caught, because tryout() is bounded by the parentheses. If you're composing this
inside of another cli, then the scope is bounded by the outside cli::

    range(5) | apply( tryout(-1) | op()**2)  | deref() # returns [0, 1, 4, 9, 16]. tryout() will capture op()**2
    range(5) | apply((tryout(-1) | op()**2)) | deref() # returns [0, 1, 4, 9, 16], exactly the same as before, demonstrating that you don't have to wrap tryout() around another pair of braces

Cli composition
---------------

One of the very powerful things about this workflow is that you can easily combine cli tools together,
to reach unfathomable levels of complexity while using very little code and still remain relatively readable.
For example, this is an `image dataloader <https://mlexps.com/imagenet/8-vit/>`_ built pretty much from
scratch, but with full functionality comparable to PyTorch's dataloaders::

   base = "~/ssd/data/imagenet/set1/192px"
   idxToCat = base | ls() | head(80) | op().split("/")[-1].all() | insertIdColumn() | toDict()
   catToIdx = idxToCat.items() | permute(1, 0) | toDict()
   # stage 1, (train/valid, classes, samples (url of img))
   st1 = base | ls() | head(80) | apply(ls() | splitW()) | transpose() | deref() | aS(k1.Wrapper)
   # stage 2, (train/valid, classes, samples, [img, class])
   st2 = st1() | (apply(lambda x: [x | toImg() | toTensor(torch.uint8), catToIdx[x.split("/")[-2]]]) | repeatFrom(4) | apply(aS(tf.Resize(192)) | aS(tf.AutoAugment()) | op()/255, 0)).all(2) | deref() | aS(k1.Wrapper)
   def dataF(bs): return st2() | apply(repeatFrom().all() | joinStreamsRandom() | batched(bs) | apply(transpose() | aS(torch.stack) + toTensor(torch.long))) | stagger.tv(10000/bs) | aS(list)

These 6 lines of code will read from a directory, grabs all images from the first 80 categories, splits
them into train and valid sets. Then it will extend the data infinitely (so that we never run out of batches
to train), load the images on multiple worker processes, do augmentations on them, renormalize them, batch
them up, stack them together into a tensor, and split batches into multiple epochs.

All of that, from scratch, where you're in control of every detail, operating in 7 dimensions, in multiple
processes, in just 6 lines of code. This is just so ridiculously powerful that it boggles my mind every day.
Yes, you can argue that it's not clear what's going on, but for a person that is already familiar with them
like I do, seeing exactly how data is being transformed at every stage is quite straightforward and trivial.

Serial composition
******************

So let's see a few examples on how to compose clis together. Let's say you have a list of files::

   fileNames = ["a.txt", "b.txt", "c.txt"]

Let's say you now want to read every line from every file quickly, using cli tools,
and get the number of lines in each file. Instead of something like this::

   sizes = []
   for fileName in fileNames:
      sizes.append(cat(fileName) | shape(0)) # shape(0) is kinda like aS(len). It just returns the length of the input iterator, but difference is that aS(len) can only operate on lists

...which really defeats the purpose of the elegant cli workflow, you can do::

   sizes = fileNames | apply(cat() | shape(0)) | aS(list)

In this example, there is 1 "composition": ``cat() | shape(0)``. If you check out the
docs for :class:`~inp.cat`, which is used to read files, you'd know that there're 2 modes of operation::

   cat("a.txt") | shape(0) # mode 1: cat() acts like a function, returning a list of lines in the file
   "a.txt" | cat() | shape(0) # mode 2: cat() acts like a cli tool, which will return a list of lines in the file when a file name is piped into it
   "a.txt" | (cat() | shape(0)) # mode 2: cat() acts like a cli tool, "cat() | shape(0)" acts as a "serial" cli

   s = cat() | shape(0); "a.txt" | s # equivalent to the 3rd line, but this time declaring "cat() | shape(0)" as a separate object

In the second case, ``"a.txt" | cat()`` will be executed first, then getting the number of elements will be
executed later (``... | shape(0)``), but in the third case, ``cat() | shape(0)`` will be executed first, which
returns the special cli :class:`~init.serial`, then the file name will be piped in later (``"a.txt" | (...)``)

Because cli tools are also functions, which includes :class:`~init.serial`, you can pass them into other cli
tools that expects a function, like :class:`~modifier.apply`. You can be extra meta, like this::

   # assume a.txt, b.txt, c.txt has 10, 20, 30 lines
   fileNames = [["a.txt"], ["b.txt", "c.txt"]]
   # returns [[10], [20, 30]]
   sizes = fileNames | apply(apply(cat() | shape(0)))
   # also returns [[10], [20, 30]], and is equivalent to the line above, as "apply(apply(...))" is equivalent to "(...).all(2)"
   sizes = fileNames | (cat() | shape(0)).all(2)

This type of composition is quite straightforward, unlike the next 2.

"&" composition, or "oneToMany"
*******************************

Take a look at this example::

   arr = ["a", "b", "c"]
   arr | toRange()                       # returns range(3), equivalent to [0, 1, 2]
   arr | iden()                          # returns ["a", "b", "c"]
   arr | (toRange() & iden()) | aS(list) # returns [range(3), ["a", "b", "c"]]
   arr | toRange() & iden() | aS(list)   # returns [range(3), ["a", "b", "c"]], demonstrating "&" will be executed before "|", so you don't need parentheses around it
   arr | toRange() & iden() | joinStreams() | aS(list) # returns [0, 1, 2, "a", "b", "c"]

So, this will take the input iterator, duplicates into 2 versions, pipes them into the 2
clis you specified and return both of them. You can do this with as much clis as you want::

   arr | toRange() &  shape() & grep("a")  | deref() # returns [[0, 1, 2], [3, 1], ["a"]]
   arr | toRange() & (shape() & grep("a")) | deref() # also returns [[0, 1, 2], [3, 1], ["a"]], demonstrating a strange edge case that parentheses won't stop all clis adjacent to each other joined by "&" from combining together

Hopefully it now makes sense why it's called "oneToMany", as we're making 1 iterator available
for many clis. Also, if the exact cli operation is only known at run time, then you can
procedurally do this using :class:`~init.oneToMany`.

"+" composition, or "mtmS"
**************************

Take a look at this example::

   even = filt(lambda x: x % 2 == 0)
   odd  = filt(lambda x: x % 2 == 1) # can also just be "~even", but I'm writing it out this way to be clear
   [range(10, 20), range(30, 40)] | (even + odd) | deref()    # returns [[10, 12, 14, 16, 18], [31, 33, 35, 37, 39]]
   [range(10, 20) | even, range(30, 40) | odd] | deref() # also returns [[10, 12, 14, 16, 18], [31, 33, 35, 37, 39]], demonstrating that these are equivalent to each other

So, let's say that there're n items inside of the input iterator and that you specified n
clis. Then, each item will be piped into the corresponding cli, hence the name :class:`~init.mtmS`, or
"manyToManySpecific". Why not just "mtm"? Well, there used to be a "manyToMany" operator,
but it's been removed and I'm lazy to change it back.

Vanilla alternatives
********************

These operations are not actually strictly necessary, they're just convenience functions
so that writing code is simpler and more straightforward. They can be implemented using
normal clis like so::

   a = iden()
   b = apply(lambda x: x**2)
   c = shape()

   x = [[1, 2], [3, 4], [5, 6]]
   x | a + b + c | deref()                                  # returns [[1, 2], [9, 16], [2]]
   x | ~aS(lambda x, y, z: [x | a, y | b, z | c]) | deref() # returns [[1, 2], [9, 16], [2]]

   x = range(5)
   x | a & b & c | deref()                           # returns [[0, 1, 2, 3, 4], [0, 1, 4, 9, 16], [5]]
   x | aS(lambda x: [x | a, x | b, x | c]) | deref() # returns [[0, 1, 2, 3, 4], [0, 1, 4, 9, 16], [5]]

So you might want to use these vanilla versions initially if you're having a hard time with this,
but I wouldn't recommend using vanilla in the long term.

JS transpiler
-------------

.. toctree::
   :maxdepth: 1

   js_transpiler

Philosophy
----------

Just a short note: while I was developing this, the emphasis is on creating very succinct
code that does a whole lot, to aid in exploring/creating datasets. Because of it, I've chosen
to sacrifice readability. The idea is, if it's so fast to create a functionality, whenever
you need to change the code, it'll be faster to just recreate it from scratch than try to
change the existing code. And the mental effort to recreate it is substantially lower than
the mental effort needed to understand a normal codebase written using vanilla Python. Also
this encourages you to rethink the problem in a new light entirely, which usually results in
much shorter and simpler code than if you were to adapt an existing solution. This seem to be
true for me so far.

Note that creating unreadable, fantastically complicated code only happens around 5%. Majority
of the time it's actually very readable and I can change an obscure detail after 10 seconds.
The way I usually do it is to "feel" what the data looks like, instead of trying to trace what
it looks like from the very beginning. This is possible because certain functions has certain
common signatures. For example, ``~apply(lambda x,y: x+y, 3)`` probably means that it's manipulating
a table with the 3rd column being a list of 2 coordinate numbers. So, overtime, you'll develop
an intuition for what's happenning and can visualize the data's shape right in the middle of the
pipeline.

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
- :class:`~structural.repeat` and friends, :class:`~structural.groupBy`, :class:`~structural.ungroup`,
  :class:`~structural.hist`, :class:`~structural.insert`, :class:`~structural.insertIdColumn`

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
   A | B & C
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

Creating your own cli
-------------------------

It's fairly simple to create your new cli. If it's composed of other clis, you can do
something like this::

   newCli = filt(lambda x: x%2==0) | head(4) | deref()
   range(10) | newCli # returns [0, 2, 4, 6]

If it's more complicated that needs to have access to some state, like a sum of numbers,
then you can extend from :class:`~k1lib.cli.init.BaseCli` like so::

   class NewCli(BaseCli):
       def __init__(self, bias=0):
           self.bias = bias # don't necessarily have to call super.__init__()
       def __ror__(self, it):
           s = self.bias
           for elem in it:
               s += elem
            return s

   [range(12, 30), range(8)] | NewCli(4).all() | deref() # returns [373, 32]

Accelerations
-------------------------

Cli tools are pretty dynamic and clever. A lot of times, they try to understand what you're trying
to do, then rewrite your code into something else completely, but still produce exactly the desired
output. For example::

   ["what is 3+4?", "what is 8+7?"] | apply(complete()) # returns ['0', '7']. I know, LLMs are still bad at math
   np.random.randn(3, 4, 5) | apply(repeat(2).all() | transpose() | joinStreams()) # returns numpy array with shape (3, 8, 5)

On the first line, normally, ``complete()`` takes in 1 single string and also outputs a single string.
But if you know how these LLMs are run, you know that it's a lot more efficient for the GPU to batch
multiple sentences together to generate text at the same time. So on the surface, this line seems
horribly inefficient, as it will call the model 2 times, one for each string. However, cli tools are
smart enough to realize you're trying feed multiple things to a model, and will batch them up automatically.

On the second line, there're lots of operations that should normally heavily bisect the input data
(a numpy array), like ``apply()`` and ``repeat()`` and whatnot, but believe it or not, cli tools are
smart enough to transform the array completely in C, and the output of the whole thing is still another
numpy array and not a nested generator. Here's the summary of the operations that are accelerated in this
way:

.. include:: ../literals/cli-accel.rst

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
   :members: serial, oneToMany, mtmS, fastF, patchNumpy, patchDict, patchPandas
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

kapi module
-------------------------

.. automodule:: k1lib.cli.kapi
   :members:
   :undoc-members:
   :show-inheritance:

kgv module
-------------------------

.. automodule:: k1lib.cli.kgv
   :members:
   :undoc-members:
   :show-inheritance:

kjs module
-------------------------

.. automodule:: k1lib.cli.kjs
   :members:
   :undoc-members:
   :show-inheritance:

ktree module
-------------------------

.. automodule:: k1lib.cli.ktree
   :members:
   :undoc-members:
   :show-inheritance:

kxml module
-------------------------

.. automodule:: k1lib.cli.kxml
   :members:
   :undoc-members:
   :show-inheritance:

lsext module
-------------------------

.. automodule:: k1lib.cli.lsext
   :members:
   :undoc-members:
   :show-inheritance:

models module
-------------------------

.. automodule:: k1lib.cli.models
   :members:
   :undoc-members:
   :show-inheritance:

modifier module
-------------------------

.. automodule:: k1lib.cli.modifier
   :members:
   :undoc-members:
   :show-inheritance:

_applyCl module
-------------------------

These are helper functions for :class:`~k1lib.cli.modifier.applyCl` and are not
intended for the end user (aka you) to use. They're just here so that you can read
the source code if interested.

.. automodule:: k1lib.cli._applyCl
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
