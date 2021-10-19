# k1lib

PyTorch is awesome, and it provides a very effective way to execute ML code fast. What it lacks is surrounding infrastructure to make general debugging and discovery process better. Other more official wrapper frameworks sort of don't make sense to me, so this is an attempt at recreating a robust suite of tools that makes sense.

Also, there's the package `k1lib.bioinfo` which contains nice bioinformatics tools. What does this have to do with PyTorch? Nothing really. In fact, I tried to develop `k1lib.bioinfo` without any dependencies from the main library. I just bunched them together cause I'm lazy to manage 2 separate libraries.

## Installation

Just do this:

```bash
pip install k1lib
```

Then in a notebook, do this:

```python
from k1lib.imports import *
```

## Some details

- Repo: https://github.com/157239n/k1lib/
- Docs: https://k1lib.github.io

## Contacts?

If you found bugs, open a new issue on the repo itself. If you want to have a chat, then email me at 157239q@gmail.com
