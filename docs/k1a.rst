k1lib._k1a module
--------------------

`k1a <https://k1a.k1lib.com/>`_ is a supplementary library to this library
that accelerates a lot of functionalities by compiling to C. It's exposed in this
main library as the module :mod:`~k1lib._k1a`. When you install the library using
``pip install k1lib[all]``, k1a is automatically installed along with it. At
the moment, this only work on linux systems, could work on mac, and won't work
on windows. Let's see an example::

    from k1lib.imports import *

    # returns ['ok', '"protein A"', 'other'], faster
    k1a.str_split('ok "protein A" other', " ")
    # also returns ['ok', '"protein A"', 'other'], explicitly pure python, slower
    k1a.py.str_split('ok "protein A" other', " ")

If k1a can't be installed on your system, then the code above would still work
as usual, just slower::

    from k1lib.imports import *

    # defaults to python version `k1a.py.str_split` if k1a can't be installed
    k1a.str_split('ok "protein A" other', " ")
    # explicitly python version
    k1a.py.str_split('ok "protein A" other', " ")

This works the same for every function provided here. If you dislike importing
everything into the namespace, then you have to do something like this::

    import k1lib._k1a as k1a
    k1a.str_split('ok "protein A" other', " ")

Again, this will use the C version if k1a is truly available, else use the
python version.

.. automodule:: k1lib._k1a
    :members:
