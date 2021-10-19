from pkg_resources import get_distribution as _get_distribution
__version__ = _get_distribution("k1lib").version

class _wrapMod:
    def __init__(self, m):
        """Wraps around a module, and only suggest symbols in __all__ list"""
        self._wrapMod_m = m
        self.__dict__.update(m.__dict__)
        self._wrapMod_extraDirs = []
    def __dir__(self): return self._wrapMod_m.__all__ + self._wrapMod_extraDirs
    def __str__(self): return str(self._wrapMod_m)
    def __repr__(self): return str(self)

from ._hidden.hiddenFile import hiddenF
from ._basics import *
from ._baseClasses import *
from ._higher import *
from ._monkey import *

from . import format
from . import website
from . import nn
from .data import *
from . import selector
from .callbacks import Callback, Callbacks
from . import callbacks
from ._learner import *
from . import schedule; schedule = _wrapMod(schedule)
from . import viz; viz = _wrapMod(viz)

#from . import gE
from . import eqn

from . import mo as _mo
class _Mo(_wrapMod):
    def __init__(self, mod): super().__init__(mod); self._MoWrap_dirs = ["registerSubstance"]
    def registerSubstance(self, name:str, _f):
        setattr(_Mo, name, property(lambda self: _f())); self._MoWrap_dirs.append(name)
    def __dir__(self): return super().__dir__() + self._MoWrap_dirs
mo = _Mo(_mo); from . import _moparse
for _name, _f in _mo._a.items(): mo.registerSubstance(_name, _f)
    
from .bioinfo import *
from . import imports