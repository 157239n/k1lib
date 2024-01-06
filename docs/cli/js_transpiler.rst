
JS transpiler tutorial
========================

.. currentmodule:: k1lib.cli.kjs

Since version 1.5, k1lib has the ability to transpile clisfrom Python into JS
code, ready to be built into an interface. Here're some examples:

Basic example
-------------

.. pyexec:: html True Compiled_JS_function

  data = repeatF(lambda: random.randint(10, 99), 20) | deref()
  jsFunc = data | (toJsFunc(("term", int, 5)) | head("term"))
  jsFunc

.. pyexec:: html True Html_output

  jsFunc.interface("jsone")

In this example, ``data`` is a list of 20 random numbers. You can then pipe
it into a :class:`toJsFunc`-captured block (review `capturing concept here <index.html#capturing-operators>`_).
Every operation that's captured will be transpiled into JS. and bundled into a
:class:`JsFunc`. Then you can inject that function anywhere you
want in your application. A lot of times, you'd want to display a search interface
right away, so you can use the :meth:`JsFunc.interface` function, which can
display the interface right within your notebook. If you want to inject into your
custom site, then the entire html can be accessed at ``jsFunc._repr_html_()``

The arguments of :class:`toJsFunc` are the argument names for the JS function that
you can use anywhere within the Python clis. Try playing around with the search
box of the "Html output" section.

Clis that take in functions
---------------------------

This also works with clis that are expected to take in a function, like
:class:`~k1lib.cli.modifier.apply` or :class:`~k1lib.cli.filt.filt`:

.. pyexec:: html True Compiled_JS_function

  jsFunc = range(10) | deref() | (toJsFunc() | apply("x**2"))
  jsFunc

.. pyexec:: html True Html_output

  jsFunc.interface("json")

More example, this time taking in a js argument:

.. pyexec:: html True Compiled_JS_function

  jsFunc = range(10) | deref() | (toJsFunc(("divisor", int, 3)) | filt("x % divisor == 1"))
  jsFunc

.. pyexec:: html True Html_output

  jsFunc.interface("json")

It can be crazy complicated, yet still works:

.. pyexec:: html True Compiled_JS_function

  c = 6 * 2
  jsFunc = range(10) | deref() | (toJsFunc() | apply("parseFloat((x//3 + c) ** 4)"))
  jsFunc

.. pyexec:: html True Html_output

  jsFunc.interface("json")

If you noticed, the transpiled JS code for ``(x//3 + 6) ** 4`` is actually
``Math.pow((Math.floor(x/3)+6), 4)``. The transpiler understands your code
written in Python, and translates operations like ``a ** b`` into ``Math.pow(a, b)``
automatically. How cool is that! And as demonstrated in the previous example,
you can also use JS variables too (``divisor``), instead of just Python variables.

Notice how it also figures out that ``c`` must be a Python variable, so the
transpiler will auto convert that to json and injects it into the JS code. Also
notice how you can freely mix JS and Python code a little bit. For basic operations,
use Python syntax, while for function calling, you can use JS functions.

Lambda functions with lots of variables and :class:`~k1lib.cli.modifier.op` works too:

.. pyexec:: html True Compiled_JS_function

  jsFunc = range(10) | deref() | (toJsFunc() | insertIdColumn() | ~apply("lambda x,y: x*y"))
  jsFunc

.. pyexec:: html True Html_output

  jsFunc.interface("json")

.. pyexec:: html True Compiled_JS_function

  jsFunc = range(10) | deref() | (toJsFunc() | apply(op()**2))
  jsFunc

.. pyexec:: html True Html_output

  jsFunc.interface("json")

Let's see a more complex example:

Lots of moving parts
--------------------

.. pyexec:: html True Compiled_JS_function

  data = repeatF(lambda: random.randint(1000, 9999), 100) | deref()
  f1 = grep("${term}") | apply(str) | batched(5, True) | head(10)
  f2 = pretty() | join("\n") | aS(fmt.pre)
  jsFunc = data | (toJsFunc("term") | f1 | f2)
  jsFunc

.. pyexec:: html True Html_output

  jsFunc.interface("html")

Just a reminder, you can specify :class:`toJsFunc` at any point in
the pipeline. As long as the data you pipe into the :class:`toJsFunc`-captured
block can be converted into json, you're good.

.. pyexec:: html True Compiled_JS_function

  data = range(10) | deref()
  jsFunc = data | (toJsFunc() | filt("x%3 == 0") & filt("x%2 == 0"))
  jsFunc

.. pyexec:: html True Html_output

  jsFunc.interface("json")

Custom transpiler logic
-----------------------

You can write transpiler logic for any custom class/functions that you desire!
Let's imagine the use case to be writing a function that calculates the factorial
sequence, where an initial number is multiplied by increments of itself, and
getting the first n elements out of it. Let's see an example using classes:

.. pyexec:: html True Compiled_JS_function

  class Factorio(BaseCli): # yes, the spelling is not the math func, but the game. But I love Factorio so
      def __init__(self, n):
          self.n = n
      def __ror__(self, start):
          value = start
          for i in range(self.n):
              yield value
              value *= start+i+1
      def _jsF(self, meta):
          fIdx = f"f_{random.randint(0, 1_000_000)}_{round(time.time())}"
          vIdx = f"f_{random.randint(0, 1_000_000)}_{round(time.time())}"
          return f"""
    const {fIdx} = ({vIdx}) => {{
        const ans = []; let value = {vIdx};
        for (let i = 0; i < {self.n}; i++) {{
            ans.push(value);
            value = value * ({vIdx} + i + 1);
        }}
        return ans;
    }};
          """, fIdx
  
  2 | Factorio(5) | deref() # returns [2, 6, 24, 120, 720]

  jsFunc = 2 | (toJsFunc(("size", int, 3)) | Factorio("size"))
  jsFunc

.. pyexec:: html True Html_output

  jsFunc.interface()

You can also write transpiler functions for any functions you want. Let's write
one for the inverse square root function:

.. pyexec:: html True Compiled_JS_function

  def inv_sqrt(x, numerator=1):
      return numerator/math.sqrt(x)
  def _jsF_inv_sqrt(meta, numerator=1):
      fIdx = f"f_{random.randint(0, 1_000_000)}_{round(time.time())}"
      vIdx = f"f_{random.randint(0, 1_000_000)}_{round(time.time())}"
      return f"const {fIdx} = ({vIdx}) => {{ return {numerator}/Math.sqrt({vIdx}); }}", fIdx
  settings.cli.kjs.jsF[inv_sqrt] = _jsF_inv_sqrt

  inv_sqrt(4) # returns number close to 0.5

  jsFunc = range(1, 10) | deref() | (toJsFunc(("someNum", int, 1)) | apply(inv_sqrt, numerator="someNum") | apply(round, ndigits=2))
  jsFunc

.. pyexec:: html True Html_output

  jsFunc.interface("json")

If your function is really simple and exists in JS natively, you can simplify it way down:

.. pyexec:: html True Html_output

  settings.cli.kjs.jsF[math.sqrt] = lambda meta: ("", "Math.sqrt")

  range(10) | deref() | (toJsFunc() | apply(math.sqrt) | apply(round, ndigits=2)) | op().interface("json")




