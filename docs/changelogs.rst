
Changelogs
==========

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
- Modified :class:`~input.cat` to be able to take in file name by pipe
- Added new joining operator "+" between :class:`init.BaseCli`

.. currentmodule:: k1lib.callbacks.callbacks

Style changes:

- Changed :attr:`Callbacks.learner` to :attr:`Callbacks.l`
- Changed :attr:`Callback.learner` to :attr:`Callbacks.l`
- Removed :mod:`k1lib.eqn` from :mod:`k1lib.imports`'s namespace

0.1.6
----------------

I don't really keep track of things 0.1.6 and before, so nothing here really.