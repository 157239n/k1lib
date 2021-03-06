# AUTOGENERATED FILE! PLEASE DON'T EDIT
"""
This is for all short utilities that converts from 1 data type to another. They
might feel they have different styles, as :class:`toFloat` converts object iterator to
float iterator, while :class:`toPIL` converts single image url to single PIL image,
whereas :class:`toSum` converts float iterator into a single float value.

The general convention is, if the intended operation sounds simple (convert to floats,
strings, types, ...), then most likely it will convert iterator to iterator, as you
can always use the function directly if you only want to apply it on 1 object.

If it sounds complicated (convert to PIL image, tensor, ...) then most likely it will
convert object to object. Lastly, there are some that just feels right to input
an iterator and output a single object (like getting max, min, std, mean values)."""
__all__ = ["toStr", "toNumpy", "toTensor", "toList", "toSet", "toIter", "toRange",
           "toSum", "toProd", "toAvg", "toMean", "toMax", "toMin", "toPIL", "toImg",
           "toRgb", "toRgba", "toBin", "toIdx", "toDict", "toDictF",
           "toFloat", "toInt"]
import re, k1lib, torch, math, numpy as np
from k1lib.cli.init import BaseCli, Table, Row, T; import k1lib.cli as cli
from collections import deque; from typing import Iterator, Any, List, Set, Tuple, Dict, Callable, Union
settings = k1lib.settings.cli
class toStr(BaseCli):
    def __init__(self, column:int=None):
        """Converts every line to a string.
Example::

    # returns ['2', 'a']
    [2, "a"] | toStr() | deref()
    # returns [[2, 'a'], [3, '5']]
    assert [[2, "a"], [3, 5]] | toStr(1) | deref()"""
        super().__init__(); self.column = column
    def __ror__(self, it:Iterator[str]):
        c = self.column
        if c is None:
            for line in it: yield str(line)
        else:
            for row in it:
                yield [e if i != c else str(e) for i, e in enumerate(row)]
class toNumpy(BaseCli):
    def __init__(self):
        """Converts generator to numpy array. Essentially ``np.array(list(it))``"""
        super().__init__()
    def __ror__(self, it:Iterator[float]) -> np.array:
        return np.array(list(it))
class toTensor(BaseCli):
    def __init__(self, dtype=torch.float32):
        """Converts generator to :class:`torch.Tensor`. Essentially
``torch.tensor(list(it))``.

Also checks if input is a PIL Image. If yes, turn it into a :class:`torch.Tensor`
and return."""
        self.dtype = dtype
    def __ror__(self, it:Iterator[float]) -> torch.Tensor:
        try:
            import PIL; pic=it
            if isinstance(pic, PIL.Image.Image): # stolen from torchvision ToTensor transform
                mode_to_nptype = {'I': np.int32, 'I;16': np.int16, 'F': np.float32}
                img = torch.from_numpy(np.array(pic, mode_to_nptype.get(pic.mode, np.uint8), copy=True))
                if pic.mode == '1': img = 255 * img
                img = img.view(pic.size[1], pic.size[0], len(pic.getbands()))
                return img.permute((2, 0, 1)).contiguous().to(self.dtype) # put it from HWC to CHW format
        except: pass
        return torch.tensor(list(it)).to(self.dtype)
class toList(BaseCli):
    def __init__(self):
        """Converts generator to list. :class:`list` would do the
same, but this is just to maintain the style"""
        super().__init__()
    def __ror__(self, it:Iterator[Any]) -> List[Any]: return list(it)
class toSet(BaseCli):
    def __init__(self):
        """Converts generator to set. :class:`set` would do the
same, but this is just to maintain the style"""
        super().__init__()
    def __ror__(self, it:Iterator[T]) -> Set[T]: return set(it)
class toIter(BaseCli):
    def __init__(self):
        """Converts object to iterator. `iter()` would do the
same, but this is just to maintain the style"""
        super().__init__()
    def __ror__(self, it:List[T]) -> Iterator[T]: return iter(it)
def _toRange(it):
    for i, _ in enumerate(it): yield i
class toRange(BaseCli):
    def __init__(self):
        """Returns iter(range(len(it))), effectively"""
        super().__init__()
    def __ror__(self, it:Iterator[Any]) -> Iterator[int]:
        try: return range(len(it))
        except: return _toRange(it)
settings.add("arrayTypes", (torch.Tensor, np.ndarray), "default array types used to accelerate clis")
class toSum(BaseCli):
    def __init__(self):
        """Calculates the sum of list of numbers. Can pipe in :class:`torch.Tensor` or :class:`numpy.ndarray`.
Example::

    # returns 45
    range(10) | toSum()"""
        super().__init__()
    def __ror__(self, it:Iterator[float]):
        if isinstance(it, settings.arrayTypes): return it.sum()
        return sum(it)
class toProd(BaseCli):
    def __init__(self):
        """Calculates the product of a list of numbers. Can pipe in :class:`torch.Tensor` or :class:`numpy.ndarray`.
Example::

    # returns 362880
    range(1,10) | toProd()"""
        super().__init__()
    def __ror__(self, it):
        if isinstance(it, settings.arrayTypes): return it.prod()
        else: return math.prod(it)
class toAvg(BaseCli):
    def __init__(self):
        """Calculates average of list of numbers. Can pipe in :class:`torch.Tensor` or :class:`numpy.ndarray`.
Example::

    # returns 4.5
    range(10) | toAvg()
    # returns nan
    [] | toAvg()"""
        super().__init__()
    def __ror__(self, it:Iterator[float]):
        if isinstance(it, settings.arrayTypes): return it.mean()
        s = 0; i = -1
        for i, v in enumerate(it): s += v
        i += 1
        if not k1lib.settings.cli.strict and i == 0: return float("nan")
        return s / i
toMean = toAvg
class toMax(BaseCli):
    def __init__(self):
        """Calculates the max of a bunch of numbers. Can pipe in :class:`torch.Tensor` or :class:`numpy.ndarray`.
Example::

    # returns 6
    [2, 5, 6, 1, 2] | toMax()"""
        super().__init__()
    def __ror__(self, it:Iterator[float]) -> float:
        if isinstance(it, settings.arrayTypes): return it.max()
        return max(it)
class toMin(BaseCli):
    def __init__(self):
        """Calculates the min of a bunch of numbers. Can pipe in :class:`torch.Tensor` or :class:`numpy.ndarray`.
Example::

    # returns 1
    [2, 5, 6, 1, 2] | toMin()"""
        super().__init__()
    def __ror__(self, it:Iterator[float]) -> float:
        if isinstance(it, settings.arrayTypes): return it.min()
        return min(it)
class toPIL(BaseCli):
    def __init__(self):
        """Converts a path to a PIL image.
Example::

    ls(".") | toPIL().all() | item() # get first image"""
        import PIL; self.PIL = PIL
    def __ror__(self, path) -> "PIL.Image.Image":
        return self.PIL.Image.open(path)
toImg = toPIL
class toRgb(BaseCli):
    def __init__(self):
        """Converts greyscale/rgb PIL image to rgb image.
Example::

    # reads image file and converts it to rgb
    "a.png" | toPIL() | toRgb()"""
        import PIL; self.PIL = PIL
    def __ror__(self, i):
        rgbI = self.PIL.Image.new("RGB", i.size)
        rgbI.paste(i); return rgbI
class toRgba(BaseCli):
    def __init__(self):
        """Converts random PIL image to rgba image.
Example::

    # reads image file and converts it to rgba
    "a.png" | toPIL() | toRgba()"""
        import PIL; self.PIL = PIL
    def __ror__(self, i):
        rgbI = self.PIL.Image.new("RGBA", i.size)
        rgbI.paste(i); return rgbI
class toBin(BaseCli):
    def __init__(self):
        """Converts integer to binary string.
Example::

    # returns "101"
    5 | toBin()"""
        super().__init__()
    def __ror__(self, it): return bin(int(it))[2:]
class toIdx(BaseCli):
    def __init__(self, chars:str):
        """Get index of characters according to a reference.
Example::

    # returns [1, 4, 4, 8]
    "#&&*" | toIdx("!#$%&'()*+") | deref()"""
        self.chars = {v:k for k, v in enumerate(chars)}
    def __ror__(self, it):
        chars = self.chars
        for e in it: yield chars[e]
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
        super().__init__(fs=[keyF, valueF]); self.keyF = keyF or (lambda s: s)
        self.valueF = valueF or (lambda s: s)
    def __ror__(self, keys:Iterator[Any]) -> Dict[Any, Any]:
        keyF = self.keyF; valueF = self.valueF
        return {keyF(key):valueF(key) for key in keys}
def _toop(toOp, c, force, defaultValue):
    return cli.apply(toOp, c) | (cli.apply(lambda x: x or defaultValue, c) if force else cli.filt(cli.op() != None, c))
def _toFloat(e) -> Union[float, None]:
    try: return float(e)
    except: return None
class toFloat(BaseCli):
    def __init__(self, *columns, mode=2):
        """Converts every row into a float. Example::

    # returns [1, 3, -2.3]
    ["1", "3", "-2.3"] | toFloat() | deref()
    # returns [[1.0, 'a'], [2.3, 'b'], [8.0, 'c']]
    [["1", "a"], ["2.3", "b"], [8, "c"]] | toFloat(0) | deref()

With weird rows::

    # returns [[1.0, 'a'], [8.0, 'c']]
    [["1", "a"], ["c", "b"], [8, "c"]] | toFloat(0) | deref()
    # returns [[1.0, 'a'], [0.0, 'b'], [8.0, 'c']]
    [["1", "a"], ["c", "b"], [8, "c"]] | toFloat(0, force=True) | deref()

This also works well with :class:`torch.Tensor` and :class:`numpy.ndarray`,
as they will not be broken up into an iterator::

    # returns a numpy array, instead of an iterator
    np.array(range(10)) | toFloat()

:param columns: if nothing, then will convert each row. If available, then
    convert all the specified columns
:param mode: different conversion styles
    - 0: simple ``float()`` function, fastest, but will throw errors if it can't be parsed
    - 1: if there are errors, then replace it with zero
    - 2: if there are errors, then eliminate the row"""
        self.columns = columns; self.mode = mode;
    def __ror__(self, it):
        columns = self.columns; mode = self.mode
        if len(columns) == 0:
            if isinstance(it, np.ndarray): return it.astype(float)
            if isinstance(it, torch.Tensor): return it.float()
            if mode == 0: return it | cli.apply(float)
            return it | _toop(_toFloat, None, mode == 1, 0.0)
        else: return it | cli.init.serial(*(_toop(_toFloat, c, mode == 1, 0.0) for c in columns))
def _toInt(e) -> Union[int, None]:
    try: return int(float(e))
    except: return None
class toInt(BaseCli):
    def __init__(self, *columns, mode=2):
        """Converts every row into an integer. Example::

    # returns [1, 3, -2]
    ["1", "3", "-2.3"] | toInt() | deref()

:param columns: if nothing, then will convert each row. If available, then
    convert all the specified columns
:param mode: different conversion styles
    - 0: simple ``float()`` function, fastest, but will throw errors if it can't be parsed
    - 1: if there are errors, then replace it with zero
    - 2: if there are errors, then eliminate the row

See also: :meth:`toFloat`"""
        self.columns = columns; self.mode = mode;
    def __ror__(self, it):
        columns = self.columns; mode = self.mode
        if len(columns) == 0:
            if isinstance(it, np.ndarray): return it.astype(int)
            if isinstance(it, torch.Tensor): return it.int()
            if mode == 0: return it | cli.apply(int)
            return it | _toop(_toInt, None, mode == 1, 0.0)
        else: return it | cli.init.serial(*(_toop(_toInt, c, mode == 1, 0.0) for c in columns))