Base module
=============

Classes
--------

- :class:`k1lib.Learner`
- :class:`k1lib.Object`
- :class:`k1lib.Range`
- :class:`k1lib.Domain`
- :class:`k1lib.AutoIncrement`
- :class:`k1lib.Wrapper`
- :class:`k1lib.Every`
- :class:`k1lib.Absorber`
- :class:`k1lib.CaptureStdout`
- :class:`k1lib.ignoreWarnings`

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

.. autoclass:: k1lib.Absorber
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.CaptureStdout
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.ignoreWarnings
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.wrapMod
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
-------------

.. autoexception:: k1lib.CancelRunException
.. autoexception:: k1lib.CancelEpochException
.. autoexception:: k1lib.CancelBatchException

Functions
-----------

.. autofunction:: k1lib.textToHtml
.. autofunction:: k1lib.clearLine
.. autofunction:: k1lib.tab
.. autofunction:: k1lib.isNumeric
.. autofunction:: k1lib.close
.. autofunction:: k1lib.patch
.. autofunction:: k1lib.wraps
.. autofunction:: k1lib.squeeze
.. autofunction:: k1lib.raiseEx
.. autofunction:: k1lib.smooth
.. autofunction:: k1lib.numDigits
.. autofunction:: k1lib.limitLines
.. autofunction:: k1lib.limitChars
.. autofunction:: k1lib.showLog
.. autofunction:: k1lib.beep
.. autofunction:: k1lib.executeNb
.. autofunction:: k1lib.dontWrap
.. autofunction:: k1lib.positionalEncode
.. autofunction:: k1lib.debounce
.. autofunction:: k1lib.perlin3d
.. autofunction:: k1lib.graph
.. autofunction:: k1lib.digraph

Higher order functions
----------------------

.. autofunction:: k1lib.polyfit
.. autofunction:: k1lib.derivative
.. autofunction:: k1lib.optimize
.. autofunction:: k1lib.inverse
.. autofunction:: k1lib.integrate
