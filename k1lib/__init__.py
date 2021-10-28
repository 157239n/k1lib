from pkg_resources import get_distribution as _get_distribution
__version__ = _get_distribution("k1lib").version

from ._hidden.hiddenFile import hiddenF
from ._basics import *
from ._baseClasses import *
from . import cli
from ._higher import *
from ._monkey import *

from . import fmt;      fmt      = wrapMod(fmt)
from . import knn;      knn      = wrapMod(knn)
from . import kdata;    kdata    = wrapMod(kdata)
from . import selector; selector = wrapMod(selector)
from .callbacks import Callback, Callbacks, Cbs
from . import callbacks
from ._learner import *
from . import schedule; schedule = wrapMod(schedule)
from . import viz;      viz      = wrapMod(viz)

#from . import gE
from . import eqn

class _Mo(wrapMod):
    def __init__(self, mod): super().__init__(mod); self._MoWrap_dirs = ["registerSubstance"]
    def registerSubstance(self, name:str, _f):
        setattr(_Mo, name, property(lambda self: _f())); self._MoWrap_dirs.append(name)
    def __dir__(self): return super().__dir__() + self._MoWrap_dirs
from . import _mo; mo = _Mo(_mo)
for _name, _f in _mo._a.items(): mo.registerSubstance(_name, _f)

from . import imports
