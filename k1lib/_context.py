# AUTOGENERATED FILE! PLEASE DON'T EDIT
import io, sys, warnings, time, k1lib
from contextlib import contextmanager
from functools import partial
__all__ = ["captureStdout", "ignoreWarnings", "timer", "attrContext"]
@contextmanager
def captureStdout() -> k1lib.Wrapper:
    """Captures every print() statement. Taken from https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call.
Example::

    with k1lib.captureStdout() as outer:
        print("something")
        with k1lib.captureStdout() as inner:
            print("inside inner")
        print("else")
    # prints "['something', 'else']"
    print(outer.value)
    # prints "['inside inner']"
    print(inner.value)

Note that internally, this replaces :data:`sys.stdout` as :class:`io.StringIO`, so
might not work property if you have fancy :class:`bytes` stuff going on. Also,
carriage return (``\\r``) will erase the line, so multi-line overlaps might not
show up correctly.

If you wish to still print stuff out, you can do something
like this::

    with k1lib.captureStdout() as out:
        print("abc") # gets captured
        out.print("def") # not captured, will actually print out
"""
    _stdout = sys.stdout; sys.stdout = _stringio = io.StringIO()
    w = k1lib.Wrapper([])
    w.print = partial(print, file=_stdout)
    try: yield w
    finally:
        w.value = [l.split("\r")[-1] for l in _stringio.getvalue().split("\n")]
        sys.stdout = _stdout
@contextmanager
def ignoreWarnings():
    """Context manager to ignore every warning.
Example::

    import warnings
    with k1lib.ignoreWarnings():
        warnings.warn("some random stuff") # will not show anything"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield
@contextmanager
def timer():
    """Times generic code.
Example::

    with k1lib.timer() as t:
        time.sleep(1.1)
    # prints out float close to 1.1
    print(t())

The with- statement will actually return a :class:`~k1lib.Wrapper` with value
None. The correct time will be deposited into it after the code block ends."""
    w = k1lib.Wrapper(None)
    beginTime = time.time()
    try: yield w
    finally: w.value = time.time() - beginTime
@contextmanager
def attrContext(var, **kwargs):
    """Temporarily sets variable's attribute to something else.
Example::

    class A: pass
    a = A()
    a.b = 3
    print(a.b) # prints "3"
    with k1lib.attrContext(a, b=4, c=5):
        print(a.b, a.c) # prints "4 5"
    print(a.b, a.c) # prints "3 None"
"""
    oldValues = dict()
    for k, v in kwargs.items():
        oldValues[k] = getattr(var, k, None)
        setattr(var, k, v)
    try: yield
    finally:
        for k, v in oldValues.items():
            setattr(var, k, v)