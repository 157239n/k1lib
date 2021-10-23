
Context tutorial
================

.. currentmodule:: k1lib.cli

The idea for the :mod:`k1lib.cli.ctx` is that anywhere inside the stream, you can save something to a "context" dictionary. And then later on, in another callback, you can use the object saved.

Remember you have to do this first before actually be able to use this module::

    cliSettings["useCtx"] = True

This module is not yet to the point where I'd call it ready yet
