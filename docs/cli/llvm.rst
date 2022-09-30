
LLVM optimizer tutorial
========================

.. currentmodule:: k1lib.cli

Since version 1.0, k1lib has an awesome compiler and optimizer that looks
a lot like LLVM, a compiler infrastructure project created by Chris Lattner
to unify all compilers. The idea is to define an intermediate representation
(IR) that look like this::

  @.str = internal constant [14 x i8] c"hello, world\0A\00"

  declare i32 @printf(i8*, ...)

  define i32 @main(i32 %argc, i8** %argv) nounwind {
  entry:
      %tmp1 = getelementptr [14 x i8], [14 x i8]* @.str, i32 0, i32 0
      %tmp2 = call i32 (i8*, ...) @printf( i8* %tmp1 ) nounwind
      ret i32 0
  }

This is a "Hello World" program written in LLVM IR. Think of the IR as a
flavor of assembly, but better, clearer, and is sort of abstract (does
not follow any particular instruction set). Then, you can design **frontends**,
which are programs that takes in code files in some language like C, C++, Go, etc,
and spits out the IR. You can also design **passes**, essentially programs that
takes in IR, do some analysis/optimization and spits out a different IR. Do
this enough times and your code will become super optimized. Then you can design
**backends**, which are programs that take in IR and spits out binary in the
targeted instruction set.

.. note::

  LLVM stands for "Low Level Virtual Machine", but the project has evolved so much
  that this terminology kinda becomes meaningless. For more details on how it works,
  check these links out:

  - http://www.aosabook.org/en/llvm.html
  - https://blog.gopheracademy.com/advent-2018/llvm-ir-and-go/

Basic usage
-----------

Same idea here. Let's say you have code to count the number of lines in a text file::

  "file.txt" | cat() | shape(0)

This is pretty straightforward. ``cat()`` reads the file line by line, and ``shape(0)``
returns the total number of lines. You can then do something like this::

  # returns `tOpt` object, but it behaves as if it's the true output
  "file.txt" | tOpt() | cat() | shape(0)
  # returns the actual output (this case a single int), for when you need it directly
  "file.txt" | tOpt() | cat() | shape(0) | yieldT

It will actually get optimized into this::

  # returns int, the number of lines in the file
  None | cmd(f"wc -l file.txt") | item() | op().split(" ")[0].ab_int()

This does not read the file at all. Instead, it executes the ``wc`` program (word count)
in the terminal, parses ``wc``'s output and return the number of lines. Because ``wc``
is coded in C, it's super fast, around 6x faster than ``cat() | shape(0)``.

Normally, you'd use it in this form instead::

  # returns the optimized cli
  f = "file.txt" | tOpt() | cat() | shape(0) | tOpt
  # then you can do this to pass it through as usual
  "other file.txt" | f

Basically, you're giving the optimizer an example input, it works
its magic and spits out an optimized cli. Let's see another example
involving tensors::

  t = torch.tensor([[1, 2, 3], [4, 5, 6]])
  # returns [[tensor([1, 2, 3])], [tensor([4, 5, 6])]]
  torch.randn(2, 3) | unsqueeze(1) | deref()
  # returns `tOpt` object that behaves like the below tensor
  torch.randn(2, 3) | tOpt() | unsqueeze(1) | deref()
  # returns tensor([[[1, 2, 3]], [[4, 5, 6]]])
  torch.randn(2, 3) | tOpt() | unsqueeze(1) | yieldT

This is desirable because operations on PyTorch tensors are much faster than
operations on lists of lists of tensors. So, you can create analysis/optimization
passes that takes in clis, analyze what the user really wants and outputs a more
optimized clis.

In the following section, you'll be learning how the type hint system works,
how exactly do you create these passes and a few examples of them

Type hint system
----------------

So, there's a quite strict type hint system across all clis located at
:mod:`k1lib.cli.typehint`. The idea is to deduce type hint info after a cli if
given the input's type hint, like this::

  t = tList(int) # type hint, a list of integers
  f = item();
  # returns int, output type hint
  f._typehint(t)

There are several default type hint objects:

- tBase: base hint class
- tAny: matches any value/object
- tList: list of a specific type. Eg: ``tList(tAny())`` represents a list of generic
  objects, and ``tList(str)`` represents a list of strings
- tIter: iterator of a specific type. Same as tList, but you can't get the length
  of it
- tSet: set of a specific type. Again, same as tList
- tCollection: iterator of many types. Eg: ``tCollection(int, float)`` matches a list
  like ``[2, 2.3]``.
- tNpArray: Numpy array with specific dtype and rank
- tTensor: PyTorch Tensor with specific dtype and rank

There are a few convenience combined types:

- tListIter: a tuple of tList and tIter
- tListSet: a tuple of tList and tSet
- tListIterSet: a tuple of tList, tIter and tSet
- tArrayTypes: a tuple of tNpArray and tTensor

There are a few utilities:

- inferType: infer the type of a specific object. ``inferType(range(3))`` returns
  ``tList(int)``
- tLowest: gets the common type of all input types. ``assert tLowest(tIter(float), tList(int))`` returns
  ``tIter(float)``
- tCheck: cli used to verify the integrity of type hints automatically
- tOpt: cli used to optimize everything

This type hint system is almost mandatory because you just wouldn't be able to do
lots of optimizations without knowing some specifics on how your data looks like.

Creating optimization pass
--------------------------

Full code for this example pass looks like this::

  def o1(cs, ts, metadata):
    return [cs[1], cs[0]]
  tOpt.addPass(o1, [toList, head])

What this optimization does is that it detects whether you're prematurely creating a
list or not. Here, you're telling the system to run your pass if it encounters
``toList() | head()`` somewhere. ``cs`` is a list of instantiated clis, and ``ts`` is
a list of input type hints for each of the clis. Then, you should return a list of
new clis if you're able to optimize it, or ``None`` if you can't.

How about an example that actually utilizes the type hints::

  def oUnsqueeze(cs, ts, metadata):
    a = cs[0]; t = ts[0]; i = 0;
    if not isinstance(t, tArrayTypes): return None
    while isinstance(a, cli.apply) and a.normal: i += 1; a = a.f
    if not isinstance(a, cli.wrapList): return None
    t = t.__class__(t.child, t.rank+1 if t.rank is not None else None)
    if isinstance(t, tNpArray): return [cli.aS(lambda x: np.expand_dims(x, i)).hint(t)]
    else: return [cli.aS(lambda x: x.unsqueeze(i)).hint(t)]
  tOpt.addPass(oUnsqueeze, [cli.apply], 4)

This detects whether the input is a Numpy array or PyTorch tensor, and apply the
respective unsqueeze operation instead of the normal ``wrapList().all(dim)`` that
breaks the array/tensor up.

