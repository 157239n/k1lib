Base module
=============

.. attribute:: k1lib.settings

This is actually an object of type :class:`~k1lib.Settings`:

.. include:: literals/settings.rst

Also, this is exposed automatically, so something like this works::

   settings.svgScale = 0.6

Classes
--------

- :class:`k1lib.Learner`
- :class:`k1lib.Object`
- :class:`k1lib.Range`
- :class:`k1lib.Domain`
- :class:`k1lib.AutoIncrement`
- :class:`k1lib.Wrapper`
- :class:`k1lib.Every`
- :class:`k1lib.RunOnce`
- :class:`k1lib.MaxDepth`
- :class:`k1lib.MovingAvg`
- :class:`k1lib.Absorber`
- :class:`k1lib.Settings`
- :class:`k1lib.UValue`

.. autoclass:: k1lib.Learner
   :members:
   :undoc-members:
   :special-members: __call__
   :show-inheritance:

.. autoclass:: k1lib.Object
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.Range
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __getitem__

.. autoclass:: k1lib.Domain
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.AutoIncrement
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __call__

.. autoclass:: k1lib.Wrapper
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.Every
   :members:
   :undoc-members:
   :special-members: __call__
   :show-inheritance:

.. autoclass:: k1lib.RunOnce
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.MaxDepth
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.MovingAvg
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.Absorber
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.Settings
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.UValue
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.wrapMod
   :members:
   :undoc-members:
   :show-inheritance:

Context managers
------------------

- :class:`k1lib.captureStdout`
- :class:`k1lib.ignoreWarnings`
- :class:`k1lib.timer`
- :class:`k1lib.attrContext`

.. autoclass:: k1lib.captureStdout
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.ignoreWarnings
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.timer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.attrContext
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
-------------

These exceptions are used within :class:`~k1lib.Learner` to cancel things early on.
If you raise :class:`~k1lib.CancelBatchException` while passing through the model,
the :class:`~k1lib.Learner` will catch it, run cleanup code (including checkpoint
``endBatch`` ), then proceeds as usual.

If you raise something more major, like :class:`~k1lib.CancelRunException`,
:class:`~k1lib.Learner` will first catch it at batch level, run clean up code, then
rethrow it. :class:`~k1lib.Learner` will then recatch it at the epoch level, run
clean up code, then rethrow again. Same deal at the run level.

.. autoexception:: k1lib.CancelRunException
.. autoexception:: k1lib.CancelEpochException
.. autoexception:: k1lib.CancelBatchException

Functions
-----------

.. autofunction:: k1lib.isNumeric
.. autofunction:: k1lib.patch
.. autofunction:: k1lib.wraps
.. autofunction:: k1lib.squeeze
.. autofunction:: k1lib.raiseEx
.. autofunction:: k1lib.numDigits
.. autofunction:: k1lib.limitLines
.. autofunction:: k1lib.limitChars
.. autofunction:: k1lib.showLog
.. autofunction:: k1lib.beep
.. autofunction:: k1lib.dontWrap
.. autofunction:: k1lib.debounce
.. autofunction:: k1lib.scaleSvg
.. autofunction:: k1lib.pValue
.. autofunction:: k1lib.now
.. autofunction:: k1lib.pushNotification
.. autofunction:: k1lib.dep
.. autofunction:: k1lib.ticks
.. autofunction:: k1lib.perlin3d
.. autofunction:: k1lib.graph
.. autofunction:: k1lib.digraph

Higher order functions
----------------------

.. autofunction:: k1lib.polyfit
.. autofunction:: k1lib.derivative
.. autofunction:: k1lib.optimize
.. autofunction:: k1lib.inverse
.. autofunction:: k1lib.integral
