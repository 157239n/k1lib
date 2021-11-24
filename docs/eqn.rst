.. module:: k1lib.eqn

k1lib.eqn module
----------------

The idea of this module looks something like this::

   from k1lib.imports import *
   settings.eqn.eqnPrintExtras = False

   s = k1lib.eqn.System("""
   # comments like this are okay. This section's for buying things
   10 cent -> 1 kWh
   1.5 dollar -> 1000 H2O
   12 dollar -> O2
   1.4 dollar -> CH4
   
   # conversions
   100 cent -> 1 dollar
   1 MJ -> 0.27 kWh
   """);

   # parsing extra equations down the line
   s.parse("1 H2O + 16 MJ -> 0.11 H2 + 0.88 O2")

Essentially, you can create a system of equations. Here, all the chemicals are in
kilograms, so you can buy 1 kg oxygen for 12 dollars. Then, you can get equations
relating to a specific term::

   s.O2

Output:

.. code-block:: text

   Consumers:


   Producers:
   1. H2O + 16 MJ -> 0.11 H2 + 0.88 O2
   2. 12 dollar -> O2

Then, you can pick out a single equation that has another unique term "dollar"::

   print(s.O2.dollar) # outputs "O2 -> 12 dollar"

This will return the flipped equation, going from "O2" to "dollar", because the
expression looks like ``s.O2.dollar``. You can go in the reverse order if you want
to::

   print(s.dollar.O2) # outputs "12 dollar -> O2"

For complex case where ``s.dollar.O2`` can have multiple answers, use
:meth:`Eqns.pick` instead. You can also do random math on these equations::

   print(s.dollar.O2 * 5 + s.dollar.CH4) # outputs "61.4 dollar -> 5 O2 + CH4"

You can also "combine" multiple equations together like this::

   print(s.cent.dollar @ s.dollar.O2) # outputs "100 cent -> 0.083 O2"

This looks for common terms between the 2 equations, in this case "dollar". It
then tries to add these 2 equations together so that "dollar" cancels out. "0.083"
is a hideous number. To bring it to 1kg, you can multiply the equation by
``1/0.083``. This is sort of tedious, depends a lot on the original equation's
values, so you can just do it like this instead::

   # outputs "1200 cent -> O2", rounds the last term to 1
   print(round(s.cent.dollar @ s.dollar.O2))
   # outputs "1200 cent -> O2", rounds specific term to 1
   print(round(s.cent.dollar @ s.dollar.O2, "O2"))
   # outputs "3600 cent -> 3 O2", rounds the last term to value
   print(round(s.cent.dollar @ s.dollar.O2, 3))
   # outputs "12000 cent -> 10 O2", rounds specific term to specific value
   print(round(s.cent.dollar @ s.dollar.O2, ["O2", 10]))

So, using this module, you can do quick back-of-the-envelope calculations for
anything you want, like comparing between making your own oxygen, or buying oxygen
tanks from outside::

   # outputs "12 dollar -> O2"
   print(s.dollar.O2)
   # outputs "0.493 dollar -> 0.125 H2 + O2"
   print(round(s.dollar.cent @ s.cent.kWh @ s.kWh.MJ @ (s.dollar.H2O @ s.H2O.O2)))

So yeah, apparently, it's much, much cheaper to make your own oxygen from
electrolysis than buying it from outside. Makes me wonder why hospitals still buy
oxygen tanks.

This module can definitely be improved. Right now, chemicals are implicitly in
kilograms, but what if you want to convert between mol and kg? This module doesn't
really provide the facilities for that. Main reason is I'm lazy to implement, and
it sounds more trouble than its worth. I still use this module for all kinds of
chemical flow analysis, and it works out fine for me, so there're really no
incentives to do this.

.. autoclass:: k1lib.eqn.Eqn
   :members: __init__, save, __contains__, __getattr__, __getitem__, __iter__,
      __len__, __hash__, copy, sharedTerms, join, __matmul__, round, __round__
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.eqn.Eqns
   :members: __init__, __getitem__, __getattr__, pick, __dir__
   :undoc-members:
   :show-inheritance:

.. autoclass:: k1lib.eqn.System
   :members: __init__, spellCheck, __getitem__, __len__, __getattr__, __dir__
   :undoc-members:
   :show-inheritance:
