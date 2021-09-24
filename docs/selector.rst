
k1lib.selector module
---------------------

This module is mainly used internally, although end users can enjoy some of its
benefits too. The idea is to create a tree structure exactly like the given
:class:`torch.nn.Module` module. With the exact tree structure, we can then select
specific parts of the module, for any purposes that we'd like, hence the main
class's name is :class:`~k1lib.selector.ModuleSelector`.

Let's say you have a Network architecture like this::

   class DynamicGate(nn.Module):
      def __init__(self, hiddenDim):
         super().__init__()
         self.lin = nn.Linear(hiddenDim, 1)
         self.sigmoid = nn.Sigmoid()
      def forward(self, x1): return self.sigmoid(self.lin(x1))

   class SkipBlock(nn.Module):
      def __init__(self, hiddenDim=10, gate:type=None):
         super().__init__()
         def gen(): return nn.Linear(hiddenDim, hiddenDim), nn.LeakyReLU()
         self.seq = nn.Sequential(*gen(), *gen(), *gen())
         self.gate = gate(hiddenDim) if gate != None else None
      def forward(self, x):
         if self.gate == None: return self.seq(x) + x
         else:
               r = self.gate(x)
               return r*x + (1-r)*self.seq(x)

   class Network(nn.Module):
      def __init__(self, hiddenDim=10, blocks=1, block:type=SkipBlock, gate:type=DynamicGate):
         super().__init__()
         layers = []
         layers += [nn.Linear(1, hiddenDim), nn.LeakyReLU()]
         for i in range(blocks): layers += [block(hiddenDim, gate)]
         layers += [nn.Linear(hiddenDim, 1)]
         self.bulk = nn.Sequential(*layers)
      def forward(self, x):
         return self.bulk(x)

New network::

   n = Network(); print(n)

Output:

.. code-block:: text

   Network(
      (bulk): Sequential(
         (0): Linear(in_features=1, out_features=10, bias=True)
         (1): LeakyReLU(negative_slope=0.01)
         (2): SkipBlock(
            (seq): Sequential(
               (0): Linear(in_features=10, out_features=10, bias=True)
               (1): LeakyReLU(negative_slope=0.01)
               (2): Linear(in_features=10, out_features=10, bias=True)
               (3): LeakyReLU(negative_slope=0.01)
               (4): Linear(in_features=10, out_features=10, bias=True)
               (5): LeakyReLU(negative_slope=0.01)
            )
            (gate): DynamicGate(
               (lin): Linear(in_features=10, out_features=1, bias=True)
               (sigmoid): Sigmoid()
            )
         )
         (3): Linear(in_features=10, out_features=1, bias=True)
      )
   )

Creating simple selector::

   selector = k1lib.selector.select(n, """
   SkipBlock > #seq: propA, propB
   SkipBlock LeakyReLU, #gate > #lin: propC
   #bulk > #0
   """); print(selector)

Output:

.. code-block:: text

   ModuleSelector:
   root: Network                       
      bulk: Sequential                
         0: Linear                  all
         1: LeakyReLU                    
         2: SkipBlock                
            seq: Sequential         propA, propB
               0: Linear               
               1: LeakyReLU         propC    
               2: Linear               
               3: LeakyReLU         propC    
               4: Linear               
               5: LeakyReLU         propC    
            gate: DynamicGate       
               lin: Linear          propC    
               sigmoid: Sigmoid        
         3: Linear 

So essentially, this is kinda similar to CSS selectors. "#a" will selects any
module with name "a". "b" will selects any module with class name "b". Inheritance
operators, like "a b" (indirect child) and "a > b" (direct child) works the same as
in CSS too.

.. note::

   You can also use the asterisk "*" to select everything. So, ``#a > *`` will match
   all child of module with name "a", and ``#a *`` will select everything
   recursively under it. In fact, when you first create :class:`k1lib.Learner`,
   the css is "*" to select everything by default

For each selection sentences, you can attach specific properties to it. If no
properties are specified, then the property "all" will be used. You can then get
a list of selected modules::

   for m in selector.modules("propA"):
      print(type(m.nnModule))

Output:

.. code-block:: text

   <class 'torch.nn.modules.linear.Linear'>
   <class 'torch.nn.modules.container.Sequential'>

Here, it selects any modules with properties "propA" or "all"

There are other methods that are analogues of :class:`torch.nn.Module` like
:meth:`~k1lib.selector.ModuleSelector.named_children` and whatnot.

.. automodule:: k1lib.selector
   :members:
   :undoc-members:
   :show-inheritance:
