
Changelogs
==========

`0.8 </0.8>`_
-------------

.. currentmodule:: k1lib.callbacks

DL:

- Exposed :mod:`k1lib.viz` automatically, and improve :meth:`~k1lib.viz.mask` so
  that it smoothes out highlighted regions.
- Added :meth:`~k1lib.perlin3d`.
- Monkey patched :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.march`,
  :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.surface`, :meth:`~matplotlib.pyplot.k3d`,
  :meth:`~torch.loglinspace`, :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.point`,
  :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.line`, :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plane`,
  :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.aspect`.
- Renamed :meth:`~callbacks.Callbacks.append` to :meth:`~callbacks.Callbacks.add`.
- Removed ``with-`` semantics for :meth:`~callbacks.Callback`. Use :attr:`~callbacks.Cbs` instead.
- Changed :meth:`~k1lib.selector.ModuleSelector.__contains__` so that it handles ``*``
  differently.

.. currentmodule:: k1lib.cli

Cli:

- Modified :class:`~utils.shape` so that it can detect multiple dimensions now, not
  just 2.
- Added :meth:`~structural.activeSamples.extend`, :meth:`~structural.activeSamples.fullness`.
- Added :class:`~modifier.applyCached`.
- Brought back :meth:`~structural.table`.
- Removed :meth:`~filt.startswith` and :meth:`~filt.endswith`, as ``filt(op().startswith())``
  does the same thing.

`0.7 </0.7>`_
-------------

.. currentmodule:: k1lib.callbacks

DL:

- Added ``metab`` as extra metadata from dataloaders to :class:`~k1lib.Learner` in
  the core training loop and modified :class:`~recorder.Recorder` to
  return it if available.
- Added ``n`` option to :class:`~k1lib.AutoIncrement`.
- Added :meth:`~k1lib.viz.mask`.
- Removed :meth:`k1lib.stats`, replaced it with :meth:`torch.Tensor.stats` directly
- Added :class:`~k1lib.cli.modifier.op` option to :class:`~k1lib.schedule.Fn`.
- Added :meth:`torch.Tensor.hasInfs`
- Made :class:`~lossFunctions.shorts.LossNLLCross` integrates with
  :class:`~lossFunctions.accuracy.AccF` instead.
- Made :class:`~lossFunctions.accuracy.AccF` integrates with :class:`~confusionMatrix.ConfusionMatrix`.
- Made :class:`~confusionMatrix.ConfusionMatrix` resilient against nans and infs,
  and fixed norm strategy (tensor rows divide by max rows, instead of tensor columns
  divide by max rows, like before).

.. currentmodule:: k1lib.cli

Cli:

- Added :class:`~filt.mask`, :meth:`~structural.unsqueeze`.
- Made :class:`~modifier.op` compatible with lots of other cli tools, so you can do
  stuff like ``filt(op() > 3, 1)``.
- Removed :class:`~structural.split`, as ``op().split().all() | joinStreams()`` does
  the same thing. This is longer, so I kinda want to put it back in, but the name
  is incredibly oxymoronic.
- Removed :meth:`~structural.listToTable` and its alias :meth:`~structural.tableFromList`,
  as they are too simple, and the new ``unsqueeze(1)`` does the same thing.
- Removed ``args`` option in :class:`~modifier.applyMp`, as it feels clunky.
- Removed :class:`~inp.cats` as ``cat().all()`` does the same job.
- Sped up :class:`~modifier.op` to have roughly same performance as
  :class:`~modifier.apply`. As a consequence, removed [:class:`~modifier.lstrip`,
  :class:`~modifier.rstrip`, :class:`~modifier.strip`, :class:`~modifier.upper`,
  :class:`~modifier.lower`] clis as stuff like ``op().upper().all()`` does the same
  and I want to simplify the collection of cli tools.
- Completely removed :mod:`k1lib.cli.ctx` module, as the performance sacrifices are
  too much, and it doesn't add a lot of useful features.
- Renamed :class:`utils.to1Str` to :class:`~utils.join` as that is more intuitive.
- Removed :class:`structural.table`, as ``op().split().all()`` does the same thing

`0.6 </0.6>`_
-------------

DL:

- Added :class:`~k1lib.knn.LinBlock`, :class:`~k1lib.Absorber`.
- Added __module__ impersonation for :class:`~k1lib.wrapMod`.
- Renamed :class:`~k1lib.callbacks.lossFunctions.shorts.LossLambda` to :class:`~k1lib.callbacks.lossFunctions.shorts.LossF`
- Renamed :meth:`torch.nn.Module.preserveDevice` to :meth:`torch.nn.Module.deviceContext`
  and add preserve buffers capability.
- Added :meth:`torch.nn.Module.gradContext`.

.. currentmodule:: k1lib.selector

:class:`k1lib.selector.ModuleSelector`:

- Renamed :meth:`filter` to :meth:`preprocess`.
- Added :meth:`~ModuleSelector.hookFp`, :meth:`~ModuleSelector.hookF`, and
  :meth:`~ModuleSelector.hookB`.
- Removed :meth:`~ModuleSelector.selected`, as :meth:`~ModuleSelector.__call__`
  does the same thing and is more intuitive
- Added ``prop`` option to :meth:`~ModuleSelector.named_children`
  and :meth:`~ModuleSelector.children`.
- Removed callback :class:`~k1lib.callbacks.frozen.Frozen` as
  :meth:`~ModuleSelector.freeze` and :meth:`~ModuleSelector.unfreeze` does the job
  and is much more robust.
- Added :meth:`~ModuleSelector.freeze` and :meth:`~ModuleSelector.unfreeze`
- Removed :meth:`~ModuleSelector.copy`, as you can just grab another selector
  straight from the model real quick.
- Removed :meth:`~ModuleSelector.parameters`, as you can always access the
  associated :class:`torch.nn.Module` inside and get params from there.

.. currentmodule:: k1lib.cli

Cli:

- Added ``raiseError`` option in :class:`~output.intercept`.
- Added multi argument capabilities to :meth:`~init.BaseCli.__call__`.
- Added :class:`~modifier.op`.
- Changed default param ``ignoreTensors`` of :class:`~utils.deref` to True.
- Ignores :class:`~torch.nn.Module` by default in :class:`~utils.deref`.

`0.5 </0.5>`_
-------------

.. currentmodule:: k1lib.callbacks

DL:

- Renamed :mod:`k1lib.format` to :mod:`k1lib.fmt`, and exposed it automatically.
- Renamed :mod:`~k1lib.fmt.computation` to :mod:`~k1lib.fmt.comp`,
  :mod:`~k1lib.fmt.computationRate` to :mod:`~k1lib.fmt.compRate`.
- Added :meth:`~k1lib.fmt.sizeOf`
- Exposed :mod:`~k1lib.selector` automatically.
- Deleted :mod:`k1lib.website`
- Fixed infinity elements in :class:`landscape.Landscape`'s plots.
- Split :class:`~loss_accuracy.Accuracy`'s accuracy calculating part into
  :class:`~lossFunctions.accuracy.AccF`.

.. currentmodule:: k1lib.cli

Cli:

- Added chained mode to :class:`~utils.item`
- Fixed ignoreTensor mechanic in :class:`~utils.deref`
- Added prefetch mode in :class:`~modifier.applyMp`
- Added :class:`~modifier.applyMpBatched` that executes lots of transformations in
  a single job.
- Added :meth:`~modifier.applyMp.clearPools` and :meth:`~modifier.applyMp.pools`.
- Added bytes reading and writing to :class:`~inp.cat` :class:`~output.file`.
- Added :class:`~structural.activeSamples`.
- Removed aliases :class:`~structural.splitColumns` and :class:`~structural.joinColumns`.
- Removed :class:`~structural.stitch`, as ``to1Str().all()`` does the same thing.

`0.4 </0.4>`_
-------------

This update moves things around a lot. The actual coding experience stays the same,
but a lot of links \< 0.4 will be broken in 0.4 docs. Go to 0.3 docs if you wish to
follow links.

.. currentmodule:: k1lib.callbacks

Molecule (:mod:`k1lib.mo`):

- Added close coulomb force calculations to simulator to make it
  more realistic (cyclohexane chair config possible now!)
- Added optional Hydrogen viewing to various functions in :mod:`~k1lib.mo`
- Fixed parsing bug where it doesn't recognize "3-methyl" group in
  "3-methylpentane".

DL:

- Don't let :class:`~k1lib.AutoIncrement`'s ``value`` property to auto increment
  internal value.
- Removed :class:`~k1lib.kdata.CyclicRandomSampler`, as ``range(n) | repeatFrom() | randomize(n)```
  does the same thing.
- Removed :class:`~k1lib.kdata.FunctionDataset`, added simpler
  :class:`~k1lib.kdata.FunctionData` as replacement.
- Removed :class:`~k1lib.kdata.DataLoader`, :class:`~k1lib.kdata.Data` and
  :class:`~k1lib.kdata.DatasetWithSampler`, as they're complex and obsolete.
- Added :meth:`~k1lib.kdata.tfImg`, :meth:`~k1lib.kdata.tfFloat`,
  :meth:`~k1lib.kdata.analyzeFloat`
- Monkey-patched :class:`torch.nn.Module` to have piping capabilities.
- Renamed :mod:`k1lib.data` to :mod:`k1lib.kdata`, and exposed it automatically in
  :mod:`~k1lib.imports`.
- Renamed :mod:`k1lib.nn` to :mod:`k1lib.knn`, and exposed it automatically.

.. currentmodule:: k1lib.cli

Bioinfo cli:

- Renamed :mod:`k1lib.bioinfo.cli` to :mod:`k1lib.cli`
- Added :meth:`~modifier.stagger` as the new interface for dataloaders.
- Added :class:`~output.intercept`, :class:`~inp.toPIL`.
- Added PIL conversion mode to :class:`utils.toTensor`
- Added Tensor shape mode in :class:`utils.shape`.
- Added :mod:`~k1lib.cli.others` module, with :meth:`~others.crissCross`
- Added Tensor mode to :class:`~utils.toSum`, :class:`~utils.toAvg`,
  :class:`~utils.toMin`, :class:`~utils.toMax` and :class:`~init.oneToMany`.
- Added alias :class:`~utils.toMean`.
- Added dtype choice to :class:`~utils.toTensor`.

`0.3 </0.3>`_
-------------

Background stuff:

- Added mo tutorial

.. currentmodule:: k1lib.callbacks

DL:

- Added :meth:`~k1lib.viz.FAnim`
- Added :mod:`~k1lib.mo` for stuff related to molecular dynamics
- Added :meth:`~k1lib.graph`, :meth:`~k1lib.digraph`, :meth:`~k1lib.AutoIncrement.__call__`
- Huge revamp of :mod:`~k1lib.schedule` to make it more intuitive. There's only 1
  main schedule object now: :class:`~k1lib.schedule.Fn`.
- Added :meth:`k1lib.wraps`, :meth:`k1lib.Object.__delitem__`, :meth:`k1lib.Range.fromRange`
- Added :class:`k1lib.Every`

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Removed :class:`~filt.notIn`, as :class:`~filt.inSet` does the job just as well
- Included cli import command in :mod:`~k1lib.imports` by default
- Modified :meth:`~modifier.toFloat` and :meth:`modifier.toInt` so they can force
  weird values to 0.
- Moved existing :class:`~structural.toDict` to :class:`~structural.toDictF`, and
  created a new :class:`~structural.toDict`.

`0.2 </0.2>`_
-------------

Pretty minor update. I just want to push this out as soon as possible

Background stuff:

- Changed versioning system so that it makes more sense
- Added osic and mp tutorials
- Added more speed analysis in the cli tutorial

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Removed ``dirs`` and ``files`` parameters in :class:`~inp.ls`, as :class:`~filt.isFile` is good enough
- Disable module :mod:`~k1lib.bioinfo.cli.ctx` by default, to improve performance
- Replaced :class:`~filt.nonEmptyStream` to :class:`~filt.empty`

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
