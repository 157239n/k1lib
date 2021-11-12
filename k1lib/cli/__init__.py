from k1lib import wrapMod as _wrapMod

_scatteredClis = [] # everywhere else in the system can add objects here, and k1lib.imports will make all of them available.
def scatteredClis(): return [c.__name__ for c in _scatteredClis]

from .init import *

# common utils
from .filt import *
from .grep import *
from .inp import *
from .modifier import *
from .output import *
from .structural import *
from .utils import *
from .others import *

# bio specific
from .entrez import *
from .bio import *
from . import mgi;  mgi  = _wrapMod(mgi)

# file formats
from . import kxml; kxml = _wrapMod(kxml)
from . import kcsv; kcsv = _wrapMod(kcsv)
from . import sam;  sam  = _wrapMod(sam)
from . import gb;   gb   = _wrapMod(gb)

from .trace import * # has to be last, to wait for others to load up
