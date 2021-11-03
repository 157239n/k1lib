
Monkey patched classes
======================

These are functionalities added to other libraries, or "monkey-patched" them. How
is this possible? Check out :meth:`k1lib.patch`.

.. automodule:: k1lib._monkey
    :members: dummy

Class :class:`torch.nn.Module`
-------------------------------

.. automethod:: torch.nn.modules.Module.getParamsVector
.. automethod:: torch.nn.modules.Module.importParams
.. automethod:: torch.nn.modules.Module.exportParams
.. automethod:: torch.nn.modules.Module.paramsContext
.. automethod:: torch.nn.modules.Module.deviceContext
.. automethod:: torch.nn.modules.Module.gradContext
.. automethod:: torch.nn.modules.Module.__ror__
.. automethod:: torch.nn.modules.Module.select
.. autoattribute:: torch.nn.modules.Module.nParams

Class :class:`torch.Tensor`
----------------------------

.. automethod:: torch.Tensor.crissCross
.. automethod:: torch.Tensor.histBounds
.. automethod:: torch.Tensor.histScaled
.. automethod:: torch.Tensor.clearNan
.. automethod:: torch.Tensor.hasNan
.. automethod:: torch.Tensor.hasInfs

Class :class:`graphviz.dot.Digraph`
-------------------------------------

.. automethod:: graphviz.dot.Digraph.__call__

Class :class:`graphviz.dot.Graph`
-------------------------------------

.. automethod:: graphviz.dot.Graph.__call__
