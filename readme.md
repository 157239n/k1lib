# k1lib

PyTorch is awesome, and it provides a very effective way to execute ML code fast. What
it lacks is surrounding infrastructure to make general debugging and discovery process
better. Other more official wrapper frameworks sort of don't make sense to me, so this
is an attempt at recreating a robust suite of tools that makes sense.

This is more than just an ML library though. A prominent feature is the set of "cli tools" originally intended to replace the bash/awk/perl bioinformatics workflow. It essentially allows you to pipe inputs into functions, which returns an output which can be piped into other functions. Using these tools, you can literally perform complex operations in multiple dimensions in 2-3 lines of code that would normally take >100 lines. It's also super flexible, operates on multiple dimensions and not locked in, as you can change the dataflow in quite a fundamental level in ~5 minutes. Check over the basics of it here: [cli](https://k1lib.com/latest/cli/index.html)

## Installation

Just do this:

```bash
pip install k1lib[all]
```

This will install all extra dependencies, except for `k1a`, which is a supplementary library to accelerate functionalities within this library. If you can't install the optional extra dependencies for some reason then do this:

```bash
pip install k1lib
```

Then in a notebook, do this:

```python
from k1lib.imports import *
```

I've found importing all symbols work best for my day-to-day use, and it makes
cli tools more pleasant to use. However, if you're those diehard programmers
who sworn to never import all, then you can just do `import k1lib` instead.
Still, look over the `k1lib.imports` module to know what you should import.

This library has very few required dependencies, and all of them are very commonly used

## Some details

- Repo: https://github.com/157239n/k1lib/
- Docs: https://k1lib.com

Read over some tutorials in the docs to get a feel of how things work.

## Contacts?

If you found bugs, open a new issue on the repo itself. If you want to have a chat, then email me at 157239q@gmail.com

If you want to get an overview of how the repo is structured, read [contributing.md](contributing.md)
