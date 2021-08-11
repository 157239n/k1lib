k1lib.imports module
--------------------

.. automodule:: k1lib.imports

   .. autoclass:: k1lib.imports._OptionalImports
      :members: __call__, __contains__
      :undoc-members:
      :show-inheritance:

      This class is supposed to be a singleton, with the object at
      :attr:`k1lib.imports.OptionalImports`. The idea is, you can create libraries
      that has function funcA, which uses numpy. However, you don't want to declare
      your library that it depends on numpy, so if the user does not have numpy, you
      can print something out
