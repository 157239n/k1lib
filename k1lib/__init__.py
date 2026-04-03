__version__ = "1.8"

from ._hidden.hiddenFile import hiddenF
from ._basics import *
from ._perlin import *
from ._baseClasses import *
from ._context import *
from . import cli
from ._higher import *
from ._monkey import *

from . import fmt, knn, selector
from .callbacks import Callback, Callbacks, Cbs
from . import callbacks
from ._learner import *
from . import schedule, viz, _k1a, k1ui, serve, p5, kast, serpent, trans, kcom, kop, kph, kstr, kgis, assets, web, eqn

from ._advanced import *
from . import zircon

class _Mo(wrapMod):
    def __init__(self, mod): super().__init__(mod); self._MoWrap_dirs = ["registerSubstance"]
    def registerSubstance(self, name:str, _f):
        setattr(_Mo, name, property(lambda self: _f())); self._MoWrap_dirs.append(name)
    def __dir__(self): return super().__dir__() + self._MoWrap_dirs
from . import _mo; mo = _Mo(_mo)
for _name, _f in _mo._a.items(): mo.registerSubstance(_name, _f)

import os
try:
    _fn = os.path.expanduser("~/.k1lib/startup.py")
    if os.path.exists(_fn) and os.path.isfile(_fn):
        with open(_fn) as _f: exec(_f.read())
except: pass

