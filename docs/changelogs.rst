
Changelogs
==========

`0.1.13 </0.1.13>`_
-------------------

Background stuff:

- Removed walrus operator library-wide, so that it can be used with Python < 3.8

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Added :class:`~filt.breakIf`, :class:`~filt.isFile`
- Replaced :class:`~inp.infiniteF` with :class:`~structural.repeatF`
- Replaced :class:`~structural.infiniteFrom` with :class:`~structural.repeatFrom`
- Replaced :class:`~utils.dereference` with :class:`~utils.deref`
- Replaced :class:`ctx.dereference` with :class:`ctx.deref`
- Modified :class:`~modifier.applyMp` to use ``dill`` to deserialize everything
- Modified :class:`~utils.to1Str` so that it returns a string, instead of yielding
- Modified :class:`~utils.toStr` so that it can accept an optional column
- Modified :class:`~structural.splitList` so that it accepts \*args
- Removed :class:`~modifier.applySingle`, but retain :class:`~modifier.applyS`

.. currentmodule:: k1lib.callbacks

DL:

- Added class :class:`~k1lib.CaptureStdout`
- Patched :class:`torch.Tensor` with :meth:`~torch.Tensor.crissCross`,
  :meth:`~torch.Tensor.histBounds` and :meth:`~torch.Tensor.histScaled`

`0.1.12 </0.1.12>`_
-------------------

Background stuff:

- Removed docs's generated ``fonts`` folder, as it takes 8MB and isn't even used. Should now be sustainable for 100 versions on github pages.

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Removed wrapping ``__ror__`` operator if ``__init__`` is not defined, to make things performant.
- Added speed analysis in the `cli tutorial <tutorials.html>`_.
- Added :meth:`init.BaseCli.__call__`, :class:`~modifier.consume`, :meth:`ctx.ctx`, :class:`ctx.f`, :class:`~structural.peekF`, :class:`~structural.expandE`, :meth:`utils.dereference.__invert__`, :class:`~filt.unique`, :class:`~filt.notIn`, :class:`~modifier.sortF`, :class:`~utils.toMax`, :class:`~utils.toMin`, :class:`~filt.union`, :meth:`~inp.ls`, :meth:`~filt.instanceOf`, :class:`~modifier.randomize`
- Removed :class:`ctx.identity`
- Added shortcuts to :meth:`ctx.setC` and :meth:`ctx.getC`
- Made :meth:`~structural.headerIdx` context-aware
- Put :class:`ctx.Promise` dereferencing at :meth:`init.BaseCli.__ror__`, instead of dynamic patching at :mod:`k1lib.bioinfo.cli` construction time
- Get rid of :class:`~output.stdout` style inconsistencies. Previously, it looks like ``[1, 2] | stdout``, now it looks like ``[1, 2] | stdout()``.
- Added multiprocessing capabilities with :class:`~modifier.applyMp`
- Added ``maxDepth`` option for :class:`~utils.dereference`
- Added ``includeLast`` option to :class:`~structural.batched`
- Added ``float("inf")`` option to ``bs`` parameter of :class:`~structural.batched`
- Fixed :class:`~structural.permute` to be able to take in generator for rows.
- Fixed :class:`~output.stdout` to be able to display non-iterable inputs
- Fixed :class:`~utils.dereference` so that it will handle poking errors
- Fixed :class:`~structural.count` so that it can deal with list. Used to throw unhashable type: 'list'
- Added more flexibility with :meth:`~modifier.toFloat`, :meth:`~modifier.toInt` and :class:`~modifier.sort`

.. currentmodule:: k1lib.callbacks

DL:

- Added classes :class:`~k1lib.AutoIncrement`, :class:`~k1lib.Wrapper`
- Added functions :meth:`~k1lib.positionalEncode`, :meth:`~k1lib.debounce`
- Fixed :class:`~k1lib.executeNb`'s ``_globals`` doc-backref problem. Also clears plot automatically after executing a cell now.

`0.1.11 </0.1.11>`_
-------------------

Background stuff:

- Added testing section for unit tests (simple assert statements inside the notebooks)

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Added numpy/torch checks to :class:`~utils.dereference`
- Renamed :class:`~structural.sample` to :class:`~structural.peek`
- Added :class:`~structural.infiniteFrom`, :class:`~structural.joinStreamsRandom`,
  :class:`~structural.batched`, :class:`~structural.collate`, :class:`~structural.splitList`
- Added :class:`~inp.infiniteF`
- Added :class:`~utils.toTensor`
- Replaced :class:`~structural.infinite` in favor of :class:`~structural.repeat`
- Updated all cli tools to use ``super().__init__()``
- Added :mod:`~k1lib.bioinfo.cli.ctx` module, with :class:`~ctx.Promise`,
  :class:`~ctx.enum`, :class:`~ctx.identity` classes, and :meth:`~ctx.getC`,
  :meth:`~ctx.setC` methods

.. currentmodule:: k1lib.callbacks

DL:

- Added :class:`k1lib.data.CyclicRandomSampler` and :class:`k1lib.data.DatasetWithSampler`
- Added highlight feature in :meth:`callbacks.Callbacks.checkpointGraph`
- Added :meth:`k1lib.viz.Carousel.pop`, :meth:`k1lib.viz.Carousel.__getitem__`
- Added :meth:`k1lib.Learner.sample`
- Disallow :meth:`k1lib.executeNb` to execute lines that starts with "!", also
  removed parameter ``catchErrors``, as it's quite useless
- Added :meth:`k1lib.Object`

`0.1.10 </0.1.10>`_
-------------------

Background stuff:

- Added notebook regression tests
- Added tutorials automated building tool
- Added :class:`k1lib.ignoreWarnings`
- Tutorials part moved to official docs (rather than .md files on github)
- Added `covid tutorial <tutorials.html>`_

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Reintroduced :class:`~structural.permute`, as :class:`~filt.rows` is inadequate
- Added :class:`~utils.lengths`, :class:`~modifier.applySingle`
- Exposed :class:`~init.serial`, :class:`~init.oneToMany`, :class:`~init.manyToMany`,
  and :class:`~init.manyToManySpecific`

.. currentmodule:: k1lib.callbacks

DL:

- Added :class:`confusionMatrix.ConfusionMatrix` and :meth:`k1lib.viz.confusionMatrix`
- Added :meth:`callbacks.Callbacks.checkpointGraph`
- Added :meth:`torch.nn.modules.Module.paramsContext`
- Modified :class:`k1lib.Object` to allow setting ``getdoc`` field
- Added :meth:`k1lib.viz.Carousel.saveBytes`, :meth:`k1lib.viz.Carousel.saveFile`,
  :meth:`k1lib.viz.Carousel.saveGraphviz`, and handle different image formats much
  better now

`0.1.9 </0.1.9>`_
-----------------

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Added :class:`k1lib.Domain` class
- Added ``__invert__`` option for :class:`~filt.rows` and :class:`~filt.columns` by
  incorporating :class:`k1lib.Domain`
- Sped up :class:`~filt.rows` significantly
- Removed cli tool :class:`~filt.every` as :class:`~filt.rows` is good enough
- Added ``__invert__`` option for :class:`~filt.head`. As a result, removed
  :class:`~filt.nhead`
- Added :meth:`~grep.grep.till` mechanism to :class:`~grep.grep` cli tool
- Added :mod:`~k1lib.bioinfo.cli.gb` cli module to deal with genbank file format
- Added :meth:`~structural.tableFromList` as alias of :meth:`~structural.listToTable`
- Renamed :class:`~utils.avg` to :class:`~utils.toAvg`
- Added :class:`~utils.toSum`

.. currentmodule:: k1lib.callbacks

DL:

- Added Callbacks tab completion to :class:`k1lib.Learner` and :class:`~callbacks.Callbacks`
- Refactored :class:`lossLandscape.LossLandscape` to :class:`landscape.Landscape`
  that can be used by any other callbacks, right now it's :class:`~loss_accuracy.Loss`
  and :class:`~loss_accuracy.Accuracy`
- Added :meth:`callbacks.Callback.pause` to help with :class:`~loss_accuracy.Accuracy`'s
  :class:`~landscape.Landscape`

`0.1.8 </0.1.8>`_
-----------------

- Fixed installation bug where readme.md would be absent, and setup.py won't work
  at all.

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Huge revamp of how tables are treated. Before, row elements are in a single string,
  separated by a delimiter. Now each row is a full fledged list
- Added :class:`~grep.grepToTable`, :class:`~structural.joinList`,
  :class:`~filt.contains`, :class:`~structural.table`, :class:`~structural.stitch`,
  :class:`~structural.listToTable`, :class:`~structural.insertColumn` cli tools
- Removed :class:`~structural.joinRows` but still keep :class:`~structural.joinStreams`
  as "joinRows" is not really obvious
- Removed :class:`~structural.permute` as :class:`~filt.columns` is pretty much identical
- Renamed :class:`~filt.inside` to :class:`~filt.inSet`
- Cut out nested functionality from :class:`~grep.grep` to :class:`~grep.grepToTable`

`0.1.7 </0.1.7>`_
------------------

Interface with external modules:

- Swapped out ``register_backward_hook`` with :meth:`~torch.nn.Module.register_full_backward_hook`
  in :class:`~k1lib.callbacks.hookModule.HookModule` callback
- Added ``torch.nn.Module.preserveDevice()`` context manager

.. currentmodule:: k1lib.callbacks.callbacks

Callbacks:

- Changed :meth:`Callbacks.suspend` to take in names only
- Added :meth:`Callbacks.suspendClasses` to take in classes
- Changed :meth:`Callbacks.suspendEvaluation` to :meth:`Callbacks.suspendEval`, also
  added functionality for white and black lists
- Ripped out complex :meth:`Callback.__getattr__` mechanism (that automatically searches
  the parent learner for missing attributes) to improve speed
- Added :mod:`k1lib.callbacks.core` callbacks :class:`~k1lib.callbacks.core.CoreNormal`
  and :class:`~k1lib.callbacks.core.CoreRNN`
- Added more plot decorators for :class:`~k1lib.callbacks.profilers.memory.MemoryProfiler`,
  including backward-forward separator with their text
- Changed :class:`~k1lib.callbacks.lossLandscape.LossLandscape` callback so that it
  follows the common flow structure. Before, it implements a whole new ``cbs(...)``
  schema that essentially duplicated the loop inside of :class:`k1lib.Learner`

.. currentmodule:: k1lib

Learner:

- Implemented grace stop handling for :class:`Learner`. Before, if someone throws
  :exc:`CancelRunException` while executing a batch, then it will immediately jump
  to the end of the run. Changed it so that it will be caught in the batch loop,
  execute checkpoints ``cancelBatch`` and ``endBatch`` and rethrow it. Same thing
  with :exc:`CancelEpochException`
- Moved loss function from being a core functionality inside :class:`Learner`
  to an external callback, so that adapting multiple loss functions are possible
- Added :meth:`Learner.__call__`

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Added :class:`~filt.isValue`, :class:`~filt.intersection`,
  :class:`~structural.AA_`, :class:`~structural.infinite`,
  :class:`~utils.dereference` cli tools
- Modified :class:`~inp.cat` to be able to take in file name by pipe
- Added new joining operator "+" between :class:`init.BaseCli`

.. currentmodule:: k1lib.callbacks.callbacks

Style changes:

- Changed :attr:`Callbacks.learner` to :attr:`Callbacks.l`
- Changed :attr:`Callback.learner` to :attr:`Callbacks.l`
- Removed :mod:`k1lib.eqn` from :mod:`k1lib.imports`'s namespace

0.1.6
----------------

I don't really keep track of things 0.1.6 and before, so nothing here really.
