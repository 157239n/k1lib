.. module:: k1lib.callbacks.profilers

profilers module
=================================

These are subcallbacks reachable by :class:`~k1lib.callbacks.profiler.Profiler`.
When you try to access a subcallback (like ``computation``), like this::

   l = k1lib.Learner.sample()
   l.cbs.add(Cbs.Profiler())
   l.Profiler.computation # accessing the field

\.\.\.Profiler will temporarily attaches a specific subcallback, runs it, stores
data, and then detachs it, so that you can only access it via ``l.Profiler.computation``
later on. Subsequent accesses don't actually run the subcallback again, but just
displays the cached value.

computation module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.profilers.computation
   :members:
   :show-inheritance:

io module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.profilers.io
   :members:
   :show-inheritance:

memory module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.profilers.memory
   :members:
   :show-inheritance:

time module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.profilers.time
   :members:
   :show-inheritance:
