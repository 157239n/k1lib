
Cli streams
===========

Symmetric
---------

So let's say you have a list of files::

    fileNames = ["a.txt", "b.txt", "c.txt"]

You now want to read every line from every file quickly, using cli tools, and get
the number of rows in each file, instead of something like this::

    sizes = []
    for fileName in fileNames:
        sizes.append(cat(fileName) | shape(0))

...which really defeats the purpose of the elegant cli tool workflow. Instead, you
can do::

    sizes = fileNames | cats() | shape(0).all() | toList()

Let's analyze this in detail. ``fileNames`` is ``Iterator[str]``. It gets passed to
``cats()``, which if you recall, :class:`~k1lib.bioinfo.cli.input.cats` is actually
just ``apply(lambda s: cat(s))``, so now, the output is
``Iterator[Iterator[str]]``. Now we want to get the #rows of every file, but we
can't pipe the input directly to ``shape(0)``, as it will count how many files are
there instead. So, the operator :meth:`~k1lib.bioinfo.cli.init.BaseCli.all` will
return a new cli object that will apply ``shape(0)`` to every stream. The output of
that will be ``Iterator[int]``, which we can convert to a list easily with
``toList()``.

This is pretty powerful, as you can be as meta as you'd like. Something crazy like
this works::

    # assume a, b, c has 10, 20, 30 lines
    fileNames = [["a.txt"], ["b.txt", "c.txt"]]
    # returns [[10], [20, 30]]
    sizes = fileNames | (cats() | shape(0).all() | toList()).all() | toList()

Here, the inner block ``cats() | shape(0).all() | toList()`` is just like last time.
This time, it's applied on all ``List[str]`` elements in ``fileNames``, and
``toList()`` just dereferences the iterator. The maximum meta level is actually
``Iterator[Iterator[Iterator[str]]]`` here.

You can also join different streams into just 1, by doing something like this::

    fileNames = ["a.txt", "b.txt", "c.txt"]
    # returns number of lines of all files
    fileNames | cats() | joinStreams() | shape(0)

Asymmetric
----------

The streams need not be symmetrical (derived from ``.all()`` operation) like the
examples above::

    # returns [0, 1, 2, 'a', 'b', 'c']
    ["a", "b", "c"] | (toRange() & identity()) | joinStreams() | toList()
    # displays a table with first column [0, 1, 2] and second column ['a', 'b', 'c']
    ["a", "b", "c"] | (toRange() & identity()) | joinColumns() | display()

Here, a list of strings is piped into ``(toRange() & identity())`` operator. This will
effectively split the input into 2 streams. 1 gets passed through ``toRange()``,
and 1 through ``identity()``. So, the output is effectively
``[Iterator[int], Iterator[str]]``, which we can join together just like before.

When combining streams asymmetrically (using the ``&`` operator, and all cli
operators are the same), the input to the streams need not be a list. Internally,
k1lib uses the :meth:`itertools.tee` method to get multiple iterators from a single
iterator, so as to avoid creating an entire list which would waste resources. Of
course, whether this wastes resources or not depends a lot on how you structure
things. If there is an operation that blows through the entire iterator before
others use any elements, then that would slow things down.

Also, there's another way to join cli operators together. Let's check over an
example::

    even = filt(lambda x: x % 2 == 0, None)
    odd = filt(lambda x: x % 2 == 1, None)
    # returns [[10, 12, 14, 16, 18], [31, 33, 35, 37, 39]]
    [range(10, 20), range(30, 40)] | (even + odd) | dereference()
    # pretty much identical to:
    [range(10, 20) | even, range(30, 40) | odd] | dereference()

This time, we're using the ``+`` operator. What this does is pass different streams
to their corresponding cli operator.

It can be hard to remember what ``&`` and ``+`` do right away, so the strategy is to
think of ``&`` as "I'm going to pass the (single) input stream to a() **and** b()
**and** c(), so I should get 3 streams out in total". For ``+``, think of them as
stacking floors of cli operators on top of another:

.. code-block:: text

    +----------------+
    | stream1 -> a() |
    +----------------+
    | stream2 -> b() |
    +----------------+
    | stream3 -> c() |
    +----------------+

