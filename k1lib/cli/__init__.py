from k1lib import wrapMod as _wrapMod

_scatteredClis = [] # everywhere else in the system can add objects here, and k1lib.imports will make all of them available.
def scatteredClis(): return [c.__name__ for c in _scatteredClis]

from .init import *
from .typehint import *

# common utils
from .filt import *
from .grep import *
from .inp import *
from .modifier import *
from .output import *
from .structural import *
from .conv import *
from .utils import *

# bio/chem specific
from .bio import *
from .mol import *
from . import mgi;  mgi  = _wrapMod(mgi)
from . import cif;  #cif  = _wrapMod(cif)

# file formats
from . import kxml; kxml = _wrapMod(kxml)
from . import kcsv; kcsv = _wrapMod(kcsv)
from . import sam;  sam  = _wrapMod(sam)
from . import gb;   gb   = _wrapMod(gb)
from . import nb;   nb   = _wrapMod(nb)

from .optimizations import *
from .trace import * # has to be last, to wait for others to load up

