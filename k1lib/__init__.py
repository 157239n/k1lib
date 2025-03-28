from pkg_resources import get_distribution as _get_distribution
try: __version__ = _get_distribution("k1lib").version
except: pass

from ._hidden.hiddenFile import hiddenF
from ._basics import *
from ._perlin import *
from ._baseClasses import *
from ._context import *
from . import cli
from ._higher import *
from ._monkey import *

from . import fmt;      fmt      = wrapMod(fmt)
from . import knn;      knn      = wrapMod(knn)
from . import selector; selector = wrapMod(selector)
from .callbacks import Callback, Callbacks, Cbs
from . import callbacks
from ._learner import *
from . import schedule; schedule = wrapMod(schedule)
from . import viz;      viz      = wrapMod(viz)
from . import _k1a;
from . import k1ui;     k1ui     = wrapMod(k1ui)
from . import serve;
from . import p5;       p5       = wrapMod(p5)
from . import selen;    selen    = wrapMod(selen)
from . import kws;      kws      = wrapMod(kws)
from . import kast;     kast     = wrapMod(kast)
from . import serpent;  serpent  = wrapMod(serpent)
from . import trans;
from . import kcom;     kcom     = wrapMod(kcom)
from . import kop;      kop      = wrapMod(kop)
from . import kph;      kph      = wrapMod(kph)
from . import kstr;     kstr     = wrapMod(kstr)


#from . import gE
from . import eqn;      eqn      = wrapMod(eqn)

from ._advanced import *
from . import zircon;   zircon   = wrapMod(zircon)

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

