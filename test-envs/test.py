import sys
print(f"\n\n\n\n---------------------- {sys.version}")
from k1lib.imports import *
print(k1lib.now())
print(range(10) | apply(op()**2) | deref())

