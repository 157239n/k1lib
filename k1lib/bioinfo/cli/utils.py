# AUTOGENERATED FILE! PLEASE DON'T EDIT
"""
This is for all short utilities that has the boilerplate feeling
"""
from k1lib.bioinfo.cli.init import patchDefaultDelim, BaseCli, settings
import k1lib.bioinfo.cli as cli
from typing import overload, Iterator, Any, List
__all__ = ["size", "shape", "item", "identity",
           "toInt", "toFloat", "toStr", "to1Str", "toNumpy",
           "toList", "wrapList", "toIter", "toRange",
           "equals", "reverse", "ignore",
           "avg", "headerIdx"]
class size(BaseCli):
    def __init__(self, idx=None, delim:str=None):
        """Returns number of rows and columns in the input.

:param idx: if idx is None return (rows, columns). If 0 or 1, then rows
    or columns"""
        self.idx = idx; self.delim = patchDefaultDelim(delim)
    def __ror__(self, it:Iterator[str]):
        if self.idx == 0: # get rows only
            rows = 0
            for line in it: rows += 1
            return rows
        if self.idx == 1: # get #columns only
            return len(next(it).split(self.delim))
        columns = -1; rows = 0
        for line in it:
            if columns == -1:
                try: columns = len(line.split(self.delim))
                except AttributeError: columns = None
            rows += 1
        if columns == -1: columns = None
        return rows, columns
shape = size
class item(BaseCli):
    """Returns the first row"""
    def __ror__(self, it:Iterator[str]):
        return next(iter(it))
class identity(BaseCli):
    """Yields whatever the input is. Useful for multiple streams"""
    def __ror__(self, it:Iterator[Any]):
        yield from it
class toFloat(BaseCli):
    """Converts every row into a float. Excludes non numbers if not in strict
mode (`bioinfoSettings`_)."""
    def __ror__(self, it:Iterator[str]) -> Iterator[float]:
        if not settings["strict"]: it = it | cli.isNumeric()
        for line in it: yield int(line)
class toInt(BaseCli):
    """Converts every row into an integer. Excludes non numbers if not in strict
mode (`bioinfoSettings`_)."""
    def __ror__(self, it:Iterator[str]) -> Iterator[int]:
        if not settings["strict"]: it = it | cli.isNumeric()
        for line in it: yield int(line)
class toStr(BaseCli):
    def __init__(self):
        """Converts every line (possibly just a number) to a string."""
    def __ror__(self, it:Iterator[str]):
        for line in it: yield str(line)
class to1Str(BaseCli):
    def __init__(self, delim:str=None):
        """Merges all strings into 1, with `delim` in the middle"""
        self.delim = patchDefaultDelim(delim)
    def __ror__(self, it:Iterator[str]):
        yield self.delim.join(it | toStr())
class toNumpy(BaseCli):
    """Converts generator to numpy array"""
    def __ror__(self, it:Iterator[float]):
        import numpy as np
        return np.array(list(it))
class toList(BaseCli):
    """Converts generator to list. `list()` would do the
same, but this is just to maintain the style"""
    def __ror__(self, it:Iterator[Any]) -> List[Any]:
        return list(it)
class wrapList(BaseCli):
    """Wraps inputs inside a list"""
    def __ror__(self, it:Any) -> List[Any]:
        return [it]
class toIter(BaseCli):
    """Converts object to iterator. `iter()` would do the
same, but this is just to maintain the style"""
    def __ror__(self, it) -> Iterator[Any]:
        return iter(it)
class toRange(BaseCli):
    """Returns iter(range(len(it))), effectively"""
    def __ror__(self, it:Iterator[Any]) -> Iterator[int]:
        for i, _ in enumerate(it): yield i
class _EarlyExp(Exception): pass
class equals:
    """Checks if all incoming columns/streams are identical"""
    def __ror__(self, streams:Iterator[Iterator[str]]):
        streams = list(streams)
        for row in zip(*streams):
            sampleElem = row[0]
            try:
                for elem in row:
                    if sampleElem != elem: yield False; raise _EarlyExp()
                yield True
            except _EarlyExp: pass
class reverse(BaseCli):
    """Prints last line first, first line last"""
    def __ror__(self, it:Iterator[str]) -> List[str]:
        return reversed(list(it))
class ignore(BaseCli):
    """Just executes everything, ignoring the output"""
    def __ror__(self, it:Iterator[Any]):
        for _ in it: pass
class avg(BaseCli):
    """Calculates average of list of numbers"""
    def __ror__(self, it:Iterator[float]):
        it = list(it)
        if not settings["strict"] and len(it) == 0: return float("nan")
        return sum(it) / len(it)
def headerIdx(delim:str=None):
    """Cuts out first line, put an index column next to it, and prints it out"""
    return item() | wrapList() | cli.split(delim) | cli.insertIdColumn(delim) | cli.display(None, delim)