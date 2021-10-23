from .atom import *
from .atom import _a
from .substance import *
from .system import *
from .parseM import *

__all__ = [
    "Atom", "substances", "NoFreeElectrons", "OctetFull",
    "alkane", "alcohol", "sameEmpirical",
    "System", "settings",
    "parse"
]

for ___a in __all__:
    try: globals()[___a].__module__ = "k1lib.mo"
    except: pass
