# AUTOGENERATED FILE! PLEASE DON'T EDIT
"""
This is for functions that sort of changes the table
structure in a dramatic way. They're the core transformations
"""
from typing import List, Union, Iterator, Callable, Any, Tuple, Dict
from collections import defaultdict, Counter
from k1lib.cli.init import patchDefaultDelim, BaseCli, oneToMany, T, Table
import k1lib.cli as cli
import itertools, numpy as np, torch, k1lib
__all__ = ["joinColumns", "transpose", "splitColumns", "joinList", "splitList",
           "joinStreams", "yieldSentinel", "joinStreamsRandom", "batched", "collate",
           "insertRow", "insertColumn", "insertIdColumn",
           "toDict", "toDictF", "split", "expandE", "table", "stitch",
           "listToTable", "tableFromList",
           "count", "permute", "accumulate", "AA_", "peek", "peekF",
           "repeat", "repeatF", "repeatFrom"]
class joinColumns(BaseCli):
    def __init__(self, fillValue=None):
        """Join multiple columns and loop through all rows. Aka transpose.

:param fillValue: if not None, then will try to zip longest with this fill value

Example::

    # returns [[1, 4], [2, 5], [3, 6]]
    [[1, 2, 3], [4, 5, 6]] | joinColumns() | deref()
    # returns [[1, 4], [2, 5], [3, 6], [0, 7]]
    [[1, 2, 3], [4, 5, 6, 7]] | joinColumns(0) | deref()"""
        super().__init__(); self.fillValue = fillValue
    def __ror__(self, it:Iterator[Iterator[T]]) -> Table[T]:
        super().__ror__(it)
        if self.fillValue is None: yield from zip(*it)
        else: yield from itertools.zip_longest(*it, fillvalue=self.fillValue)
splitColumns = transpose = joinColumns
class joinList(BaseCli):
    def __init__(self, element=None, begin=True):
        """Join element into list.

:param element: the element to insert. If None, then takes the input [e, [...]],
    else takes the input [...] as usual

Example::

    # returns [5, 2, 6, 8]
    [5, [2, 6, 8]] | joinList() | deref()
    # also returns [5, 2, 6, 8]
    [2, 6, 8] | joinList(5) | deref()"""
        super().__init__(); self.element = element; self.begin = begin
    def __ror__(self, it:Tuple[T, Iterator[T]]) -> Iterator[T]:
        super().__ror__(it); it = iter(it)
        if self.element is None:
            if self.begin: yield next(it); yield from next(it)
            else: e = next(it); yield from next(it); yield e
        else:
            if self.begin: yield self.element; yield from it
            else: yield from it; yield self.element
class splitList(BaseCli):
    def __init__(self, *weights:List[float]):
        """Splits list of elements into multiple lists. If no weights are provided,
then automatically defaults to [0.8, 0.2]. Example::

    # returns [[0, 1, 2, 3, 4, 5, 6, 7], [8, 9]]
    range(10) | splitList(0.8, 0.2) | deref()
    # same as the above
    range(10) | splitList() | deref()"""
        super().__init__();
        if len(weights) == 0: weights = [0.8, 0.2]
        self.weights = np.array(weights)
    def __ror__(self, it):
        super().__ror__(it); it = list(it); ws = self.weights; c = 0
        ws = (ws * len(it) / ws.sum()).astype(int)
        for w in ws: yield it[c:c+w]; c += w
class joinStreams(BaseCli):
    """Joins multiple streams.
Example::

    # returns [1, 2, 3, 4, 5]
    [[1, 2, 3], [4, 5]] | joinStreams() | deref()"""
    def __ror__(self, streams:Iterator[Iterator[T]]) -> Iterator[T]:
        super().__ror__(streams)
        for stream in streams: yield from stream
import random
def rand(n):
    while True: yield random.randrange(n)
yieldSentinel = object()
class joinStreamsRandom(BaseCli):
    """Join multiple streams randomly. If any streams runs out, then quits. If
any stream yields :data:`yieldSentinel`, then just ignores that result and
continue. Could be useful in active learning. Example::

    # could return [0, 1, 10, 2, 11, 12, 13, ...], with max length 20, typical length 18
    [range(0, 10), range(10, 20)] | joinStreamsRandom() | deref()
    
    stream2 = [[-5, yieldSentinel, -4, -3], yieldSentinel | repeat()] | joinStreams()
    # could return [-5, -4, 0, -3, 1, 2, 3, 4, 5, 6], demonstrating yieldSentinel
    [range(7), stream2] | joinStreamsRandom() | deref()"""
    def __ror__(self, streams:Iterator[Iterator[T]]) -> Iterator[T]:
        super().__ror__(streams)
        streams = [iter(st) for st in streams]
        try:
            for streamIdx in rand(len(streams)):
                o = next(streams[streamIdx])
                if o != yieldSentinel: yield o
        except StopIteration: pass
class batched(BaseCli):
    def __init__(self, bs=32, includeLast=False):
        """Batches the input stream.
Example::

    # returns [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    range(11) | batched(3) | deref()
    # returns [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10]]
    range(11) | batched(3, True) | deref()
    # returns [[0, 1, 2, 3, 4]]
    range(5) | batched(float("inf"), True) | deref()
    # returns []
    range(5) | batched(float("inf"), False) | deref()"""
        super().__init__(); self.bs = bs; self.includeLast = includeLast
    def __ror__(self, it):
        super().__ror__(it); it = iter(it); l = []; bs = self.bs
        if bs == float("inf"):
            if self.includeLast: yield it
            return
        try:
            while True:
                for i in range(bs): l.append(next(it))
                yield l; l = []
        except StopIteration:
            if self.includeLast: yield l
def collate():
    """Puts individual columns into a tensor.
Example::

    # returns [tensor([ 0, 10, 20]), tensor([ 1, 11, 21]), tensor([ 2, 12, 22])]
    [range(0, 3), range(10, 13), range(20, 23)] | collate() | toList()"""
    return transpose() | cli.apply(lambda row: torch.tensor(row))
def insertRow(*row:List[T]):
    """Inserts a row right before every other rows. See also: :meth:`joinList`."""
    return joinList(row)
def insertColumn(*column, begin=True, fillValue=""):
    """Inserts a column at beginning or end.
Example::

    # returns [['a', 1, 2], ['b', 3, 4]]
    [[1, 2], [3, 4]] | insertColumn("a", "b") | deref()
"""
    return transpose(fillValue) | joinList(column, begin) | transpose(fillValue)
def insertIdColumn(table=False, begin=True, fillValue=""):
    """Inserts an id column at the beginning (or end).
Example::

    # returns [[0, 'a', 2], [1, 'b', 4]]
    [["a", 2], ["b", 4]] | insertIdColumn(True) | deref()
    # returns [[0, 'a'], [1, 'b']]
    "ab" | insertIdColumn()

:param table: if False, then insert column to an Iterator[str], else treat
    input as a full fledged table"""
    f = (cli.toRange() & transpose(fillValue)) | joinList(begin=begin) | transpose(fillValue)
    if table: return f
    else: return cli.wrapList() | transpose() | f
class toDict(BaseCli):
    def __init__(self):
        """Converts 2 Iterators, 1 key, 1 value into a dictionary.
Example::

    # returns {1: 3, 2: 4}
    [[1, 2], [3, 4]] | toDict()"""
        pass
    def __ror__(self, it:Tuple[Iterator[T], Iterator[T]]) -> dict:
        return {_k:_v for _k, _v in zip(*it)}
class toDictF(BaseCli):
    def __init__(self, keyF:Callable[[Any], str]=None, valueF:Callable[[Any], Any]=None):
        """Transform an incoming stream into a dict using a function for
values. Example::

    names = ["wanda", "vision", "loki", "mobius"]
    names | toDictF(valueF=lambda s: len(s)) # will return {"wanda": 5, "vision": 6, ...}
    names | toDictF(lambda s: s.title(), lambda s: len(s)) # will return {"Wanda": 5, "Vision": 6, ...}
"""
        super().__init__(); self.keyF = keyF or (lambda s: s)
        self.valueF = valueF or (lambda s: s)
    def __ror__(self, keys:Iterator[Any]) -> Dict[Any, Any]:
        super().__ror__(keys); keyF = self.keyF; valueF = self.valueF
        return {keyF(key):valueF(key) for key in keys}
class split(BaseCli):
    def __init__(self, delim:str=None, idx:int=None):
        """Splits each line using a delimiter, and outputs the
parts as a separate line. Example::

    # returns ["a", "b", "d", "e"]
    ["a,b", "d,e"] | split(",") | deref()
    # returns ['b', 'e']
    ["a,b", "d,e"] | split(",", 1) | deref()

:param idx: if available, only outputs the element at that index"""
        super().__init__()
        self.delim = patchDefaultDelim(delim); self.idx = idx
    def __ror__(self, it:Iterator[str]):
        super().__ror__(it)
        if self.idx == None:
            for line in it:
                for elem in line.split(self.delim): yield elem
        else:
            for line in it:
                elems = line.split(self.delim)
                yield elems[self.idx] if self.idx < len(elems) else None
class expandE(BaseCli):
    def __init__(self, f:Callable[[T], List[T]], column:int):
        """Expands table element to multiple columns.
Example::

    # returns [['abc', 3, -2], ['de', 2, -5]]
    [["abc", -2], ["de", -5]] | expandE(lambda e: (e, len(e)), 0) | deref()

:param f: Function that transforms 1 row element to multiple elements"""
        self.f = f; self.column = column
    def __ror__(self, it):
        f = self.f; c = self.column
        def gen(row):
            for i, e in enumerate(row):
                if i == c: yield from f(e)
                else: yield e
        return (gen(row) for row in it)
class table(BaseCli):
    def __init__(self, delim:str=None):
        """Splits lines to rows (List[str]) using a delimiter.
Example::

    # returns [['a', 'bd'], ['1', '2', '3']]
    ["a|bd", "1|2|3"] | table("|") | deref()"""
        super().__init__(); self.delim = patchDefaultDelim(delim)
    def __ror__(self, it:Iterator[str]) -> Table[str]:
        super().__ror__(it)
        return (line.split(self.delim) for line in it)
class stitch(BaseCli):
    def __init__(self, delim:str=None):
        """Stitches elements in a row together, so they become a simple string.
See also: :class:`~k1lib.cli.output.pretty`. Preferable to
:class:`~k1lib.cli.utils.to1Str` ``.all()``, as there's a lot of overhead in
splitting streams. Example::

    # returns ['1|2', '3|4', '5|6']
    [[1, 2], [3, 4], [5, 6]] | stitch("|") | deref()"""
        super().__init__(); self.delim = patchDefaultDelim(delim)
    def __ror__(self, it:Table[str]) -> Iterator[str]:
        super().__ror__(it); d = self.delim
        for row in it: yield d.join([str(e) for e in row])
def listToTable():
    """Turns Iterator[T] into Table[T]"""
    return cli.wrapList() | transpose()
tableFromList = listToTable
class count(BaseCli):
    """Finds unique elements and returns a table with [frequency, value, percent]
columns. Example::

    # returns [[1, 'a', '33%'], [2, 'b', '67%']]
    ['a', 'b', 'b'] | count() | deref()"""
    def __ror__(self, it:Iterator[str]):
        it = it | cli.apply(lambda row: (tuple(row) if isinstance(row, list) else row))
        c = Counter(it); s = sum(c.values())
        for k, v in c.items(): yield [v, k, f"{round(100*v/s)}%"]
class permute(BaseCli):
    def __init__(self, *permutations:List[int]):
        """Permutes the columns. Acts kinda like :meth:`torch.Tensor.permute`.
Example::

    # returns [['b', 'a'], ['d', 'c']]
    ["ab", "cd"] | permute(1, 0) | deref()"""
        super().__init__(); self.permutations = permutations
    def __ror__(self, it:Iterator[str]):
        super().__ror__(it); p = self.permutations
        def gen(row): row = list(row); return (row[i] for i in p)
        for row in it: yield gen(row)
class accumulate(BaseCli):
    def __init__(self, columnIdx:int=0, avg=False):
        """Groups lines that have the same row[columnIdx], and
add together all other columns, assuming they're numbers

:param columnIdx: common column index to accumulate
:param avg: calculate average values instead of sum"""
        super().__init__(); self.columnIdx = columnIdx; self.avg = avg
        self.dict = defaultdict(lambda: defaultdict(lambda: 0))
    def __ror__(self, it:Iterator[str]):
        super().__ror__(it)
        for row in it:
            row = list(row); key = row[self.columnIdx]
            row.pop(self.columnIdx)
            for i, e in enumerate(row):
                try: self.dict[key][i] += float(e)
                except: self.dict[key][i] = e
        for key, values in self.dict.items():
            n = len(self.dict[key].keys())
            if self.avg:
                for i in range(n):
                    if isinstance(self.dict[key][i], (int, float)):
                        self.dict[key][i] /= n
            elems = [str(self.dict[key][i]) for i in range(n)]
            elems.insert(self.columnIdx, key)
            yield elems
class AA_(BaseCli):
    def __init__(self, *idxs:List[int], wraps=False):
        """Returns 2 streams, one that has the selected element, and the other
the rest. Example::

    # returns [5, [1, 6, 3, 7]]
    [1, 5, 6, 3, 7] | AA_(1)
    # returns [[5, [1, 6, 3, 7]]]
    [1, 5, 6, 3, 7] | AA_(1, wraps=True)

You can also put multiple indexes through::

    # returns [[1, [5, 6]], [6, [1, 5]]]
    [1, 5, 6] | AA_(0, 2)

If you don't specify anything, then all indexes will be sliced::

    # returns [[1, [5, 6]], [5, [1, 6]], [6, [1, 5]]]
    [1, 5, 6] | AA_()

As for why the strange name, think of this operation as "AĀ". In statistics,
say you have a set "A", then "not A" is commonly written as A with an overline
"Ā". So "AA\_" represents "AĀ", and that it first returns the selection A.

:param wraps: if True, then the first example will return [[5, [1, 6, 3, 7]]]
    instead, so that A has the same signature as Ā"""
        super().__init__(); self.idxs = idxs; self.wraps = wraps
    def __ror__(self, it:List[Any]) -> List[List[List[Any]]]:
        super().__ror__(it); idxs = self.idxs; it = list(it)
        if len(idxs) == 0: idxs = range(len(it))
        def gen(idx):
            return [it[idx], [v for i, v in enumerate(it) if i != idx]]
        if not self.wraps and len(idxs) == 1: return gen(idxs[0])
        return [gen(idx) for idx in idxs]
class peek(BaseCli):
    """Returns (firstRow, iterator). This sort of peaks at the first row, to
potentially gain some insights about the internal formats. The returned iterator
is not tampered. Example::

    e, it = iter([[1, 2, 3], [1, 2]]) | peek()
    print(e) # prints "[1, 2, 3]"
    s = 0
    for e in it: s += len(e)
    print(s) # prints "5", or length of 2 lists

You kinda have to be careful about handling the ``firstRow``, because you might
inadvertently alter the iterator::

    e, it = iter([iter(range(3)), range(4), range(2)]) | peek()
    e = list(e) # e is [0, 1, 2]
    list(next(it)) # supposed to be the same as `e`, but is [] instead

The example happens because you have already consumed all elements of the first
row, and thus there aren't any left when you try to call ``next(it)``."""
    def __ror__(self, it:Iterator[T]) -> Tuple[T, Iterator[T]]:
        super().__ror__(it); it = iter(it)
        sentinel = object(); row = next(it, sentinel)
        if row == sentinel: return None, []
        def gen(): yield row; yield from it
        return row, gen()
class peekF(BaseCli):
    def __init__(self, f:Union[BaseCli, Callable[[T], T]]):
        r"""Similar to :class:`peek`, but will execute ``f(row)`` and
return the input Iterator, which is not tampered. Example::

    it = lambda: iter([[1, 2, 3], [1, 2]])
    # prints "[1, 2, 3]" and returns [[1, 2, 3], [1, 2]]
    it() | peekF(lambda x: print(x)) | deref()
    # prints "1\n2\n3"
    it() | peekF(headOut()) | deref()"""
        super().__init__(); self.f = f
    def __ror__(self, it:Iterator[T]) -> Iterator[T]:
        super().__ror__(it); it = iter(it)
        sentinel = object(); row = next(it, sentinel)
        if row == sentinel: return []
        def gen(): yield row; yield from it
        self.f(row); return gen()
class repeat(BaseCli):
    """Yields a specified amount of the passed in object. If you intend to pass in
an iterator, then make a list out of it first, as second copy of iterator probably
won't work as you will have used it the first time. Example::

    # returns [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    [1, 2, 3] | repeat(3) | toList()

:param repeat: if None, then repeats indefinitely"""
    def __init__(self, limit:int=None):
        super().__init__(); self.limit = limit
    def __ror__(self, o:T) -> Iterator[T]:
        super().__ror__(o)
        if self.limit is None:
            while True: yield o
        else:
            for _ in range(self.limit): yield o
def repeatF(f, limit:int=None):
    """Yields a specified amount generated by a specified function.
Example::

    # returns [4, 4, 4]
    repeatF(lambda: 4, 3) | toList()
    # returns 10
    repeatF(lambda: 4) | head() | shape(0)

:param limit: if None, then repeats indefinitely

See also: :class:`repeatFrom`"""
    if limit is None:
        while True: yield f()
    else:
        for i in range(limit): yield f()
class repeatFrom(BaseCli):
    def __init__(self, limit:int=None):
        """Yields from a list. If runs out of elements, then do it again for
``limit`` times. Example::

    # returns [1, 2, 3, 1, 2]
    [1, 2, 3] | repeatFrom() | head(5) | deref()
    # returns [1, 2, 3, 1, 2, 3]
    [1, 2, 3] | repeatFrom(2) | deref()

:param limit: if None, then repeats indefinitely"""
        super().__init__(); self.limit = limit
    def __ror__(self, it:Iterator[T]) -> Iterator[T]:
        super().__ror__(it); it = list(it)
        if self.limit is None:
            while True: yield from it
        else:
            for i in range(self.limit): yield from it