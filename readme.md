# k1lib

This library enables piping in Python, and has a lot of prebuilt functionalities
to support this workflow.

## Installation

```bash
  pip install k1lib[all]
```

This will install lots of heavy dependencies like PyTorch. If you want to install
the leanest version of the library, do this instead::

```bash
  pip install k1lib
```

To use it in a notebook, do this::

```python
  from k1lib.imports import *
```

Check out the source code for "k1lib.imports" if you're curious what it's
importing. If you hate \* imports for whatever reason, you can import cli
tools individually, like this::

```python
  from k1lib.cli import ls, cat, grep, apply, batched, display
```

## Examples

```python
# returns [0, 1, 4, 9, 16], kinda like map
range(5) | apply(lambda x: x**2) | deref()

# plotting the function y = x^2
x = np.linspace(-2, 2); y = x**2
plt.plot(x, y)         # normal way
[x, y] | ~aS(plt.plot) # pipe way

# plotting the functions y = x**2, y = x**3, y = x**4
x = np.linspace(-2, 2)
[2, 3, 4] | apply(lambda exp: [x, x**exp]) | ~apply(plt.plot) | deref()

# loading csv file and displaying first 10 rows in a nice table
cat("abc.csv") | apply(lambda x: x.split(",")) | display()

# searching for "gene_name: ..." lines in a file and display a nice overview of just the gene names alone
cat("abc.txt") | grep("gene_name: ") | apply(lambda x: x.split(": ")[1]) | batched(4) | display()

# manipulate numpy arrays and pytorch tensors
a = np.random.randn(3, 4, 5)
a | transpose()     | shape() # returns (4, 3, 5)
a | transpose(0, 2) | shape() # returns (5, 4, 3)

# loading images from categories and splitting them into train and valid sets. Image url: dataset/categoryA/image1.jpg
train, valid = ls("dataset") | apply(ls() | splitW()) | transpose() | deref()
# shape of output is (train/valid, category, image url). It was (category, train/valid, image url) before going through transpose()

# executing task in multiple processes
range(10_000_000) | batched(1_000_000) | applyMp(toSum()) | toSum()
# this splits numbers from 0 to 10M into 10 batches, and then sum each batch in parallel, and then sum the results of each batch

# executing task in multiple processes on multiple computers
range(10_000_000) | batched(1_000_000) | applyCl(toSum()) | toSum()
```

You can combine these "cli tools" together in really complex ways to do really complex
manipulation really fast and with little code. Hell, you can even create a full blown
PyTorch dataloader from scratch where you're in control of every detail, operating in 7
dimensions, in multiple processes on multiple nodes, in just 6 lines of code. Check over
the basics of it here: :mod:`k1lib.cli`.

After doing that, you can check out the tutorials to get a large overview of how everything
integrates together nicely.

## Some details

- Repo: https://github.com/157239n/k1lib/
- Docs: https://k1lib.com

## Contacts?

If you found bugs, open a new issue on the repo itself. If you want to have a chat, then email me at 157239q@gmail.com

If you want to get an overview of how the repo is structured, read [contributing.md](contributing.md)
