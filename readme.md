# k1lib

PyTorch is awesome, and it provides a very effective way to execute ML code fast. What it lacks is surrounding infrastructure to make general debugging and discovery process better. Other more official wrapper frameworks sort of don't make sense to me, so this is an attempt at recreating a robust suite of tools that makes sense.

Also, there's the package `k1lib.cli` which contains nice cli tools originally intended to replace the bash/awk/perl bioinformatics workflow. What does this have to do with PyTorch and DL? Originally nothing, but over time stuff like `batched` and `stagger` appeared which has largely replaced PyTorch data loaders.

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

Read over some tutorials in the docs to get the feel of how things work.

## Contacts?

If you found bugs, open a new issue on the repo itself. If you want to have a chat, then email me at 157239q@gmail.com
