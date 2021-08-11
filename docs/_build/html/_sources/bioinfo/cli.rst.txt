.. module:: k1lib.bioinfo.cli

k1lib.bioinfo.cli package
=========================

The main idea of this package is to emulate the terminal, but doing all of that inside Python itself. So this bash statement:

.. code-block:: console

   cat file.txt | head -5 > headerFile.txt

Turns into this statement::

   cat("file.txt") | head(5) > file("headerFile.txt")

Here, "cat", "head" and "file" are all classes extended
from :class:`~k1lib.bioinfo.cli.init.BaseCli`. All of
them implements the "reverse or" operation, or __ror__.
Essentially, these 2 statements are equivalent::

   3 | obj
   obj.__ror__(3)

Also, a lot of these tools assume that we are operating
on a table. So this table:

+------+------+------+
| col1 | col2 | col3 |
+======+======+======+
| 1    | 2    | 3    |
+------+------+------+
| 4    | 5    | 6    |
+------+------+------+

Is equivalent to this list::

   ["col1\tcol2\tcol3", "1\t2\t3", "4\t5\t6"]

Essentially, each row is a single string, and each
elements in a row are separated by a delimiter. You can
set the default delimiter using :attr:`k1lib.bioinfo.cli.bioinfoSettings` like this::

   bioinfoSettings["defaultDelim"] = ","

Also, the expected way to use these tools is to import everything directly into the
current environment, like this::

   from k1lib.bioinfo.cli import *

Besides operating on string iterators alone, this package can also be extra meta,
and operate on streams of strings, or streams of streams of anything. I think this
is one of the most powerful concept of the cli workflow. If this interests you,
check over this:

.. toctree::
   :maxdepth: 1

   streams

Submodules
----------

+-------------------------------------+---------------------------------+-------------------------------+
|    :mod:`k1lib.bioinfo.cli.bio`     | :mod:`k1lib.bioinfo.cli.entrez` | :mod:`k1lib.bioinfo.cli.mgi`  |
+=====================================+=================================+===============================+
| :mod:`k1lib.bioinfo.cli.filt`       | :mod:`k1lib.bioinfo.cli.grep`   | :mod:`k1lib.bioinfo.cli.init` |
+-------------------------------------+---------------------------------+-------------------------------+
| :mod:`k1lib.bioinfo.cli.input`      | :mod:`k1lib.bioinfo.cli.kcsv`   | :mod:`k1lib.bioinfo.cli.kxml` |
+-------------------------------------+---------------------------------+-------------------------------+
| :mod:`k1lib.bioinfo.cli.modifier`   | :mod:`k1lib.bioinfo.cli.output` | :mod:`k1lib.bioinfo.cli.sam`  |
+-------------------------------------+---------------------------------+-------------------------------+
| :mod:`k1lib.bioinfo.cli.structural` | :mod:`k1lib.bioinfo.cli.utils`  |                               |
+-------------------------------------+---------------------------------+-------------------------------+

k1lib.bioinfo.cli.bio module
----------------------------

.. automodule:: k1lib.bioinfo.cli.bio
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.entrez module
-------------------------------

.. automodule:: k1lib.bioinfo.cli.entrez
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.mgi module
-------------------------------

.. automodule:: k1lib.bioinfo.cli.mgi
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.filt module
-----------------------------

.. automodule:: k1lib.bioinfo.cli.filt
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.grep module
-----------------------------

.. automodule:: k1lib.bioinfo.cli.grep
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.init module
-----------------------------

.. autoattribute:: k1lib.bioinfo.cli.bioinfoSettings

   Main settings of :mod:`k1lib.bioinfo.cli`. When using::

      from k1lib.bioinfo.cli import *

   You can just set the settings like this::

      bioinfoSettings["defaultIndent"] = "\t"

   There are a few settings: _`bioinfoSettings`

   - defaultDelim: default delimiter used in-between columns when creating tables
   - defaultIndent: default indent used for displaying nested structures
   - lookupImgs: whether to automatically look up images when exploring something
   - oboFile: gene ontology obo file location
   - strict: whether strict mode is on. Turning it on can help you debug stuff, but
     could also be a pain to work with

.. automodule:: k1lib.bioinfo.cli.init
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.input module
------------------------------

.. automodule:: k1lib.bioinfo.cli.input
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.kcsv module
-----------------------------

.. automodule:: k1lib.bioinfo.cli.kcsv
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.kxml module
-----------------------------

.. automodule:: k1lib.bioinfo.cli.kxml
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.modifier module
---------------------------------

.. automodule:: k1lib.bioinfo.cli.modifier
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.output module
-------------------------------

.. automodule:: k1lib.bioinfo.cli.output
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.sam module
----------------------------

.. automodule:: k1lib.bioinfo.cli.sam
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.structural module
-----------------------------------

.. automodule:: k1lib.bioinfo.cli.structural
   :members:
   :undoc-members:
   :show-inheritance:

k1lib.bioinfo.cli.utils module
------------------------------

.. automodule:: k1lib.bioinfo.cli.utils
   :members:
   :undoc-members:
   :show-inheritance:
