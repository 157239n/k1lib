.. module:: k1lib.callbacks.lossFunctions

lossFunctions package
=====================

Package with a bunch of loss function callbacks. If you're planning to write your
own loss function classes, then you have to set l's ``loss`` and ``lossG`` fields.
``lossG`` is the original loss, still attached to the graph (hence "G"). Then,
``loss`` is just ``lossG.detach().item()``. This is so that other utilities can use
a shared detached loss value, for performance reasons.

shorts module
--------------------------------------------

.. automodule:: k1lib.callbacks.lossFunctions.shorts
   :members:
   :show-inheritance:
