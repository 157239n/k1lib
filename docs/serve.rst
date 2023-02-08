k1lib.serve module
------------------

This module is for quickly serving Python functions in an interactive website, so that
you can build interfaces for your experiments real quick. Let's say you have a
function in the file "a.py"::

   def endpoint(a:int=3, b:float=4, c:bool=True) -> float:
      if c: return a + b
      else: return a * b

You want to be able to expose a nice interactive interface so that you can present to
everyone, or to be used in other systems, then you can do something like this::

   cbs = k1.Callbacks()
   cbs.add(serve.FromPythonFile("a.py"))
   cbs.add(serve.BuildPythonFile(port=5138))
   cbs.add(serve.StartServer())
   cbs.add(serve.GenerateHtml(htmlFile="index.html"))

   serve.serve(cbs)

This will start up a local server at the specified port (this case 5138), and dumps a
``index.html`` file in the current folder. Opening it up will give you this interface:

.. image:: images/serve.png

That's pretty much it. You can add in your own callbacks, to enable further integration
with your systems. You can also customize the given callbacks more.

An example of all supported data types and interfaces::

   def endpoint(a:int=3, b:float=5.2, c:str="short string", d:serve.text(True)="paragraph",
                e:bool=True, f:range(3, 21)=6, g:serve.slider(1, 2)=1.2,
                h:PIL.Image.Image=someImg, i:bytes=someBinaryData,
                j:["opt 1", "opt 2"]="opt 1") -> float:
      pass

And how they're displayed:

- ``int, float, str, serve.text(True)``: text box. Could be multiline for :class:`~k1lib.serve.main.text` case
- ``bool``: checkbox
- ``range(3, 21)``: discrete slider
- ``serve.slider(1, 2)``: continuous slider
- ``PIL.Image.Image```: file upload. If return value is this then will just display the image directly
- ``bytes``: file upload
- ``["opt 1", "opt 2"]``: dropdown menu

See a few demo examples at https://mlexps.com/ (at the very bottom of the page)

.. automodule:: k1lib.serve.main
   :members:
   :undoc-members:
   :show-inheritance:
