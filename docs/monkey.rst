
Monkey patched classes
======================

These are functionalities added to other libraries, or "monkey-patched" them. How
is this possible? Check out :meth:`k1lib.patch`.

.. automodule:: k1lib._monkey
    :members: dummy

Python builtins
--------------------------------------------------

.. automethod:: builtins.str.splitCamel

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
.. automethod:: torch.Tensor.positionalEncode
.. automethod:: torch.Tensor.clearNan
.. automethod:: torch.Tensor.hasNan
.. automethod:: torch.Tensor.hasInfs

Module :mod:`torch`
--------------------------------------------------

.. automethod:: torch.loglinspace
.. automethod:: torch.sameStorage

Class :class:`graphviz.Digraph`
-------------------------------------

.. automethod:: graphviz.dot.Digraph.__call__

Class :class:`graphviz.Graph`
-------------------------------------

.. automethod:: graphviz.dot.Graph.__call__

Class :class:`mpl_toolkits.mplot3d.axes3d.Axes3D`
--------------------------------------------------

.. automethod:: mpl_toolkits.mplot3d.axes3d.Axes3D.march
.. automethod:: mpl_toolkits.mplot3d.axes3d.Axes3D.surface
.. automethod:: mpl_toolkits.mplot3d.axes3d.Axes3D.plane
.. automethod:: mpl_toolkits.mplot3d.axes3d.Axes3D.point
.. automethod:: mpl_toolkits.mplot3d.axes3d.Axes3D.line

Module :mod:`matplotlib.pyplot`
--------------------------------------------------

.. automethod:: matplotlib.pyplot.k3d
.. automethod:: matplotlib.pyplot.animate
.. automethod:: matplotlib.pyplot.getFig

Module :mod:`ray`
--------------------------------------------------

.. automethod:: ray.progress
