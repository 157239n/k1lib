# AUTOGENERATED FILE! PLEASE DON'T EDIT
"""
All tools related to context variables. Expected to use behind the "ctx"
module name, like this::

    from k1lib.imports import *
    ctx["country"] = 3

Note that this is quite a niche module, and the full purpose of it is
therefore under question. Also remember that by default, this module is
not active. Do this to turn it on::

    cliSettings["useCtx"] = True
"""
from typing import Callable, Union, List, overload, Iterator, Any, Set
from k1lib.cli.init import BaseCli, settings, Table, T
import k1lib.cli as cli
import k1lib, numpy as np, numbers, torch
from collections import deque
__all__ = ["ctx", "Promise", "getC", "setC", "deref",
           "consume", "enum", "f"]
context = dict()
def ctx():
    """Returns the internal context dictionary. Only use this if you
want to write your own context-manipulating Callbacks"""
    return context
class Promise:
    def __init__(self, ctx:str):
        """A delayed variable that represents a value in the current
context. Not intended to be instantiated by the end user. Use
:meth:`__call__` to get the actual value (aka "dereferencing").

This delayed variable just loves to be dereferenced. A lot of operations
that you do with it will dereferences it right away, like this::

    from k1lib.imports import *
    ctx["a"] = 4
    ctx['a'] # returns Promise object
    f"value: {ctx['a']}" # returns string "value: 4"
    ctx['a'] + 5 # returns 9
    ctx['a'] / 5 # returns 0.8

If a :class:`Promise` attribute is set in :class:`~k1lib.cli.init.BaseCli`
subclass, then it will automagically be dereferenced at ``__ror__`` of
:class:`~k1lib.cli.init.BaseCli`.

If you don't interact with it directly like the above operations, but
just pass it around, then it won't dereference. You can then force it to
do so like this::

    # returns an iterator, with the first variable dereferenced
    [ctx['a'], 5] | ctx.deref()
    # returns [4, 5]
    [ctx['a'], 5] | ctx.deref() | toList()
    # returns [4, 5]
    [ctx['a'], 5] | deref()"""
        self.ctx = ctx
    def __call__(self): return context[self.ctx]
    @staticmethod
    def strip(o):
        """If is :class:`Promise`, then returns the value in context,
else returns ``o``."""
        if isinstance(o, Promise): return o()
        else: return o
    def __str__(self): return str(self())
    def __add__(self, o): return self() + o
    def __mul__(self, o): return self() * o
    def __sub__(self, o): return self() - o
    def __rsub__(self, o): return o - self()
    def __truediv__(self, o): return self() / o
    def __rtruediv__(self, o): return o / self()
    def __repr__(self): return str(self())
def setC(ctx:str, value):
    """Sets the context variable. Shortcut available like
this::

    ctx["a"] = 3 # instead of ctx.setC("a", 3)"""
    context[ctx] = value
def getC(ctx:str) -> Promise:
    """Gets the context variable. Shortcut available like
this::

    ctx["a"] = 4
    ctx["a"] # return Promise, that will dereferences to 4"""
    return Promise(ctx)
basicTypes = (numbers.Number, torch.Tensor, np.number, str)
def gen(self, it):
    for e in it: yield e | self
class deref(BaseCli):
    """If encountered a :class:`Promise`, then replaces it with the value.
It's important to note that :class:`k1lib.cli.utils.deref`
already replaces every :class:`Promise`, so you don't have to pass
through this cli beforehand if you intend to dereference. Example::

    ctx.setC('a', 4)
    # returns [4]
    [ctx.Promise('a')] | ctx.deref() | toList()

Note that this ``deref()`` is inside a quite obscure module, and not the
main one at :class:`k1lib.cli.utils.deref` that's used much more
often."""
    def __ror__(self, it):
        if isinstance(it, basicTypes): return it
        if isinstance(it, Promise): return it()
        return gen(self, it)
class consume(BaseCli):
    def __init__(self, ctx:str, **kwargs):
        """Consumes the input, dereferences it and stores it in context.
Example::

    # returns [2, 3, 4, 5, 6]
    range(5) | ctx.consume('a') | apply(lambda x: x+2) | toList()
    # returns [0, 1, 2, 3, 4]
    ctx['a']()

:param kwargs: args to pass to :class:`~k1lib.cli.utils.deref`."""
        super().__init__(); self.ctx = ctx; self.kwargs = kwargs
    def __ror__(self, it:T) -> T:
        it = it | cli.deref(**self.kwargs)
        context[self.ctx] = it; return it
class enum(BaseCli):
    def __init__(self, ctx:str):
        """Saves the list index to context.
Example::

    # returns [['abc', 0], ['def', 1]]
    ["abc", "def"] | ctx.enum("a") | apply(lambda r: [r, ctx['a']]) | deref()"""
        super().__init__(); self.ctx = ctx
    def __ror__(self, it:Iterator[T]) -> Iterator[T]:
        ctx = self.ctx
        for i, e in enumerate(it): context[ctx] = i; yield e
class f(BaseCli):
    def __init__(self, ctx:str, f:Callable[[T], T]=None):
        """Saves the f-transformed list element to context.
Example::

    # returns [['abc', 3], ['ab', 2]]
    ["abc", "ab"] | ctx.f('a', lambda s: len(s)) | apply(lambda r: [r, ctx['a']]) | deref()

:param f: if not specified, then just save the object as-if"""
        self.ctx = ctx; self.f = f or (lambda x: x)
    def __ror__(self, it:Iterator[T]) -> Iterator[T]:
        ctx = self.ctx; f = self.f
        for e in it: context[ctx] = f(e); yield e