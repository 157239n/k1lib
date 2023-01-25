
Streams tutorial
====================

.. currentmodule:: k1lib.cli

Symmetric
---------

So let's say you have a list of files::

    fileNames = ["a.txt", "b.txt", "c.txt"]

Let's say you now want to read every line from every file quickly, using cli tools,
and get the number of rows in each file. Instead of something like this::

    sizes = []
    for fileName in fileNames:
        sizes.append(cat(fileName) | shape(0))

...which really defeats the purpose of the elegant cli tool workflow, you can do::

    sizes = fileNames | apply(cat()) | shape(0).all() | toList()

Let's analyze this in detail. ``fileNames`` is ``Iterator[str]``. It gets passed to
``apply(cat(s))``, so now, the output is ``Iterator[Iterator[str]]``. We want to
get the #rows of every file, but we can't pipe the input directly to
:class:`~utils.shape`, as it will count how many files are there instead. So, the
operator :meth:`~init.BaseCli.all` will return a new cli object that will apply
:class:`~utils.shape` to every stream. The output of that will be ``Iterator[int]``,
which we can convert to a list easily with :class:`~conv.toList`. ``.all()`` is
pretty much the same as :class:`~modifier.apply`, but is more intuitive.

This is pretty powerful, as you can be as meta as you'd like. Something crazy like
this works::

    # assume a, b, c has 10, 20, 30 lines
    fileNames = [["a.txt"], ["b.txt", "c.txt"]]
    # returns [[10], [20, 30]]
    sizes = fileNames | (cat().all() | shape(0).all() | toList()).all() | toList()

Here, the inner block ``cat().all() | shape(0).all() | toList()`` is just like last
time. This time, it's applied on all ``List[str]`` elements in ``fileNames``, and
:class:`~conv.toList` just dereferences the iterator. The maximum meta level is
actually ``Iterator[Iterator[Iterator[str]]]`` here.

You can also join different streams into just 1, by doing something like this::

    fileNames = ["a.txt", "b.txt", "c.txt"]
    # returns number of lines of all files
    fileNames | cat().all() | joinStreams() | shape(0)

Asymmetric
----------

The streams need not be symmetrical (derived from :meth:`~init.BaseCli.all` operation)
like the examples above::

    # returns [0, 1, 2, 'a', 'b', 'c']
    ["a", "b", "c"] | (toRange() & iden()) | joinStreams() | toList()
    # displays a table with first column [0, 1, 2] and second column ['a', 'b', 'c']
    ["a", "b", "c"] | (toRange() & iden()) | joinColumns() | display()

Here, a list of strings is piped into ``(toRange() & iden())`` operator. This will
effectively split the input into 2 streams. 1 gets passed through :class:`~conv.toRange`,
and 1 through :class:`~utils.iden`. So, the output is effectively
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

    even = filt(lambda x: x % 2 == 0)
    odd = filt(lambda x: x % 2 == 1)
    # returns [[10, 12, 14, 16, 18], [31, 33, 35, 37, 39]]
    [range(10, 20), range(30, 40)] | (even + odd) | deref()
    # pretty much identical to:
    [range(10, 20) | even, range(30, 40) | odd] | deref()

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

More procedural?
----------------

Underlying operations :class:`~init.serial`, :class:`~init.oneToMany`,
:class:`~modifier.apply`, :class:`~init.mtmS` that stands for operations
(``|``, ``&``, ``.all()``, ``+``) are exposed, in case your streams have varying
lengths.

Vanilla alternatives
--------------------

These operations are not actually strictly necessary, they're just convenience functions
so that writing code is simpler and more straightforward. They can be implemented using
normal clis like so::

    a = iden()
    b = apply(lambda x: x**2)
    c = shape()

    x = [[1, 2], [3, 4], [5, 6]]
    # returns [[1, 2], [9, 16], [2]]
    x | a + b + c | deref()
    # returns [[1, 2], [9, 16], [2]]
    x | ~aS(lambda x, y, z: [x | a, y | b, z | c]) | deref()

    x = range(5)
    # returns [[0, 1, 2, 3, 4], [0, 1, 4, 9, 16], [5]]
    x | a & b & c | deref()
    # returns [[0, 1, 2, 3, 4], [0, 1, 4, 9, 16], [5]]
    x | aS(lambda x: [x | a, x | b, x | c]) | deref()

So you might want to use these vanilla versions initially if you are unsure what exactly
these higher operations mean.
