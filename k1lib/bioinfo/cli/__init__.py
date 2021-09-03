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

from . import ctx as _ctx
class _CtxModule: # add shortcut functionality to getC and setC
    def __init__(self, _dict): self.__dict__.update(_dict)
    def __getitem__(self, ctx:str) -> _ctx.Promise: return self.getC(ctx)
    def __setitem__(self, ctx:str, value): self.setC(ctx, value)
ctx = _CtxModule(_ctx.__dict__)

# bio specific
from .entrez import *
from .bio import *
from . import mgi

# file formats
from . import kxml
from . import kcsv
from . import sam
from . import gb
