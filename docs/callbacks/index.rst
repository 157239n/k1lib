.. module:: k1lib.callbacks

k1lib.callbacks module
=======================

.. toctree::
   :maxdepth: 1

   lossFunctions
   profilers

callbacks module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.callbacks

   .. attribute:: Cbs

      :class:`~k1lib.Object` of all available callbacks. Automatically exposed, so
      you can do this::

         from k1lib.imports import *
         cbs = k1lib.Callbacks().append(Cbs.Beep())
         cbs("endRun") # plays a beep sound

   .. autoclass:: Callback
      :members:
      :show-inheritance:

   .. autoclass:: Timings
      :members:
      :undoc-members:
      :show-inheritance:

   .. autoclass:: Callbacks
      :members:
      :undoc-members:
      :special-members: __contains__, __call__, __getitem__, __iter__, __len__, 
      :show-inheritance:

confusionMatrix module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.confusionMatrix
   :members:
   :show-inheritance:

core module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.core
   :members:
   :show-inheritance:

hookModule module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.hookModule
   :members:
   :show-inheritance:

hookParam module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.hookParam
   :members:
   :show-inheritance:

limits module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.limits
   :members:
   :show-inheritance:

landscape module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.landscape
   :members:
   :show-inheritance:

loss\_accuracy module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.loss_accuracy
   :members:
   :show-inheritance:

paramFinder module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.paramFinder
   :members:
   :show-inheritance:

profiler module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.profiler
   :members:
   :show-inheritance:

progress module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.progress
   :members:
   :show-inheritance:

recorder module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.recorder
   :members:
   :show-inheritance:

shorts module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: k1lib.callbacks.shorts
   :members:
   :show-inheritance:
