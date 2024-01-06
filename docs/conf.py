# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import datetime
from k1lib.imports import *
sys.path.insert(0, os.path.abspath('./'))
sys.path.insert(0, os.path.abspath('../k1lib'))


# -- Project information -----------------------------------------------------

project = 'k1lib'
copyright = f'{datetime.datetime.now().year}, Quang Ho'
author = 'Quang Ho'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
sys.path.append(os.path.abspath("./_ext"))
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_autorun",
    "sphinx_toolbox.collapse",
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'custom_directive',
    'todo',
]

autodoc_member_order = 'bysource'


def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        if (doc := obj.__doc__) is None:
            return True
        return doc.strip() == ""
    if name in {"__ror__", "__invert__"}:
        return False
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**/.ipynb_checkpoints',
                    '.ipynb_checkpoints', '**/_*', '_*', "literals/*", "literals/**/*"]


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'  # 'alabaster'
html_theme_options = {"navigation_depth": 20}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'torch': ('https://pytorch.org/docs/master/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
    'graphviz': ('https://graphviz.readthedocs.io/en/stable/', None),
    'PIL': ('https://pillow.readthedocs.io/en/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'websockets': ('https://websockets.readthedocs.io/en/stable/', None),
    'ray': ('https://docs.ray.io/en/latest/', None),
}

# generating literals

with open("literals/settings.rst", "w") as f:
    with k1lib.captureStdout() as out:
        print(k1lib.settings.__repr__())
    f.write(".. code-block:: text\n\n" +
            "\n".join([f"   {e}" for e in out.value]))

# executing some Python code and injecting the results in



# --- cli tables


def _genColumn(l):
    n = (l | shape(0).all() | toMax()) + 2
    tmp = "{:" + str(n) + "s}"
    for e in l:
        yield "| " + tmp.format(e) + " |"


def genColumn(l, pad=0):
    res = _genColumn(l)
    h = next(res)
    n = len(h)-2
    yield "+" + "-"*n + "+"
    yield h
    yield "+" + "="*n + "+"
    for e in res:
        yield e
        yield "+" + "-"*n + "+"
    for i in range(pad//2):
        yield "|" + " "*n + "|"
        yield "+" + "-"*n + "+"


def combineColumns(_ls):
    lens = _ls | shape(0).all()
    maxLen = lens | toMax()
    return _ls | apply(lambda x: genColumn(x, (maxLen-len(x))*2)) | transpose() | join("").all()\
        | op().replace("-++-", "-+-").replace("=++=", "=+=").replace(" || ", " | ").all() | deref()


toCliTable = apply("k1lib.cli." + op())\
    | apply(lambda x: [x, sys.modules[x], sys.modules[x].__all__]) | ~sortF(lambda x: len(x[2])) | apply(op().split(".")[-1], 0)\
    | apply(~aS(lambda x, m, zs: [x, *zs | apply(lambda z: f":class:`~{x}.{z}`" if inspect.isclass(getattr(m, z)) else f":meth:`~{x}.{z}`")]))\
    | batched(5, True) | apply(combineColumns) | apply(insert("", begin=False)) | joinStreams()

["filt", "conv", "grep", "init", "inp", "kxml", "modifier", "nb", "output",
    "structural", "trace", "utils", "typehint", "optimizations"] | toCliTable | file("literals/cli-tables.rst")
["bio", "cif", "mgi", "gb", "sam"] | toCliTable | file(
    "literals/cli-bio-tables.rst")

# --- cli optimization tables

fns = k1.cli.__dict__.items() | instanceOf(type(k1), 1) | cut(1) | apply(lambda m: m.__all__ | apply("getattr(m, x)") | filt("type(x) == type") | filt("issubclass(x, BaseCli)")) | joinStreams() | aS(set) | deref()
hasNpAllOpts = fns | filt(lambda x: len(x._all_array_opt.__code__.co_code) > 4).split() | deref()
hasNpOpts = fns | iden() & apply(aS("x.__ror__.__code__.co_names") | aS(lambda x: ["np", "torch", "arrayTypes"] | inSet(x) | shape(0))) | transpose() | filt(op()>0, 1).split() | cut(0).all() | deref()
".. code-block::\n" | file("literals/cli-accel.rst")
[hasNpAllOpts, hasNpOpts] | item().all() | intersection(full=True) | insert([hasNpAllOpts[1], hasNpOpts[1]] | intersection(), False) | aS(lambda x: [x.__module__.split(".")[-1], x.__name__] | join(".")).all(2) | sort(None, False).all() | wrapList() | insert(["`array | cli` and `array | cli.all(int)` capability", "`array | cli.all(int)` capability alone", "`array | cli` capability alone", "No array acceleration"]) | transpose() | apply("f'========== {x}'", 0) | apply(batched(3, True), 1) | transpose() | iden() + (~pretty() | join("\n").all()) | transpose() | join("\n").all() | join("\n\n") | op().split("\n") | apply(lambda x: f"   {x}") | join("\n") >> file("literals/cli-accel.rst")

