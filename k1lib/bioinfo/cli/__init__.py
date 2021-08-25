from .init import settings as bioinfoSettings
from .init import *

# common utils
from .filt import *
from .grep import *
from .inp import *
from .modifier import *
from .output import *
from .structural import *
from .utils import *
from . import ctx

# bio specific
from .entrez import *
from .bio import *
from . import mgi

# file formats
from . import kxml
from . import kcsv
from . import sam
from . import gb

def _indirect():
    import functools
    from ._ctx import Promise
    def actualRor(self, it):
        if not self._ind_resolved: # short circuits
            if not self._ind_initial_scan_finished:
                self._ind_initial_scan_finished = True
                # scan for promises
                for k in [k for k in self.__dict__ if isinstance(getattr(self, k), Promise)]:
                    setattr(self, f"_promise_{k}", v := getattr(self, k)); v = v()
            a = [k for k in self.__dict__ if k.startswith("_promise_")]
            if len(a) == 0: self._ind_resolved = True
            for k in a: setattr(self, k[9:], getattr(self, k)())
        return self._internal_ror_(it)
    a = set([v for v in globals().values() if isinstance(v, type) and issubclass(v, BaseCli)])
    for e in a:
        e._internal_ror_ = e.__ror__
        e.__ror__ = actualRor
_indirect()
