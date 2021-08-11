.. module:: k1lib

k1lib package
=============

Subpackages
-----------

.. toctree::
   :maxdepth: 1

   bioinfo/index
   callbacks/index

Submodules
----------

.. toctree::
   :maxdepth: 1

   data
   eqn
   format
   graphEqn
   imports
   nn
   schedule
   selector
   viz
   website

Installation
------------

Quickest way to install is to just do this::

   pip install k1lib

This package has very few dependencies, and all of them are very commonly used. If
you're installing this for the bioinformatics tools (:mod:`k1lib.bioinfo`), and don't care about anything
related to deep learning, you can do this::

   pip install --no-deps k1lib

Module contents
---------------

.. autoclass:: k1lib.Learner
   :members:
   :undoc-members:
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

.. class:: torch.nn.modules.Module

   These are extra helper methods monkey-patched to :class:`torch.nn.Module`

   .. automethod:: torch.nn.modules.Module.importParams
   .. automethod:: torch.nn.modules.Module.exportParams
   .. automethod:: torch.nn.modules.Module.getParamsVector

.. autoexception:: k1lib.CancelRunException
.. autoexception:: k1lib.CancelEpochException
.. autoexception:: k1lib.CancelBatchException

.. autofunction:: k1lib.textToHtml
.. autofunction:: k1lib.clearLine
.. autofunction:: k1lib.tab
.. autofunction:: k1lib.isNumeric
.. autofunction:: k1lib.close
.. autofunction:: k1lib.stats
.. autofunction:: k1lib.patch
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
.. autofunction:: k1lib.polyfit
.. autofunction:: k1lib.derivative
.. autofunction:: k1lib.optimize
.. autofunction:: k1lib.inverse
.. autofunction:: k1lib.integrate
