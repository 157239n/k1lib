
Monkey patched classes
======================

See also: :meth:`k1lib.patch`

.. class:: torch.nn.modules.Module

   .. automethod:: torch.nn.modules.Module.importParams
   .. automethod:: torch.nn.modules.Module.exportParams
   .. automethod:: torch.nn.modules.Module.paramsContext
   .. automethod:: torch.nn.modules.Module.getParamsVector
   .. automethod:: torch.nn.modules.Module.preserveDevice

.. class:: torch.Tensor

   .. automethod:: torch.Tensor.crissCross
   .. automethod:: torch.Tensor.histBounds
   .. automethod:: torch.Tensor.histScaled
   .. automethod:: torch.Tensor.clearNan
   .. automethod:: torch.Tensor.hasNan

.. class:: graphviz.dot.Digraph

   .. automethod:: graphviz.dot.Digraph.__call__

.. class:: graphviz.dot.Graph

   .. automethod:: graphviz.dot.Graph.__call__
