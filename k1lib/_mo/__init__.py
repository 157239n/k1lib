"""
This module is for everything related to molecules. You can construct, explore and
simulate molecules quite easily. Check out the tutorials section for a walkthrough.
This is exposed automatically with::

   from k1lib.imports import *
   mo.C # exposed
"""


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
