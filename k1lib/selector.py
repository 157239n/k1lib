# AUTOGENERATED FILE! PLEASE DON'T EDIT
"""
This module is for selecting a subnetwork using CSS so that you can do special
things to them. Checkout the tutorial section for a walkthrough. This is exposed
automatically with::

   from k1lib.imports import *
   selector.select # exposed
"""
from torch import nn; import k1lib, re, torch
from k1lib import cli
from typing import List, Tuple, Dict, Union, Any, Iterator, Callable
from contextlib import contextmanager; from functools import partial
__all__ = ["ModuleSelector", "preprocess", "select"]
def preprocess(selectors:str, defaultProp="*") -> List[str]:
    r"""Removes all quirkly features allowed by the css
language, and outputs nice lines. Example::

    # returns ["a:f", "a:g,h", "b:g,h", "t:*"]
    selector.preprocess("a:f; a, b: g,h; t")

:param selectors: single css selector string. Statements separated
    by "\\n" or ";"
:param defaultProp: default property, if statement doesn't have one"""
    # filtering unwanted characters and quirky spaces
    lines = [e for l in selectors.split("\n") for e in l.split(";")]
    selectors = [re.sub("(^\s+)|(\s+$)", "", re.sub("\s\s+", " ", line)).replace(" >", ">").replace("> ", ">").replace(" :", ":").replace(": ", ":").replace(" ,", ",").replace(", ", ",").replace(";", "\n").replace(" \n", "\n").replace("\n ", "\n") for line in lines if line != ""]
    # adding "*" to all selectors with no props specified
    selectors = [selector if ":" in selector else f"{selector}:{defaultProp}" for selector in selectors]
    # expanding comma-delimited selectors
    return [f"{segment}:{selector.split(':')[1]}" for selector in selectors for segment in selector.split(":")[0].split(",")]
def _getParts(s:str): return [a for elem in s.split(":")[0].split(">") if elem for a in elem.split(" ") if a]
def _getProps(s:str): return [elem for elem in s.split(":")[1].split(",") if elem]
_idxAuto = k1lib.AutoIncrement()
class ModuleSelector: # empty methods so that Sphinx generates the docs in order
    props:List[str]
    """Properties of this :class:`ModuleSelector`"""
    idx:int
    """Unique id of this :class:`ModuleSelector` in the entire script. May be useful
for module recognition"""
    nn:"torch.nn.Module"
    """The associated :class:`torch.nn.Module` of this :class:`ModuleSelector`"""
    def __init__(self, parent:"ModuleSelector", name:str, nn:"torch.nn.Module"):
        self.parent = parent; self.name = name; self.nn = nn
        self._children:Dict["ModuleSelector"] = {}
        self.props:List[str] = []; self.depth:int = 0
        self.directSelectors:List[str] = []
        self.indirectSelectors:List[str] = []
        self.displayF:Callable[["ModuleSelector"], str] = lambda mS: ', '.join(mS.props)
        self.idx = _idxAuto()
    def deepestDepth(self): pass
    def highlight(self, prop:str):
        """Highlights the specified prop when displaying the object."""
        self.displayF = lambda self: (k1lib.fmt.txt.red if prop in self else k1lib.fmt.txt.identity)(', '.join(self.props))
        return self
    def __call__(self, *args, **kwargs):
        """Calls the internal :class:`torch.nn.Module`"""
        return self.nn(*args, **kwargs)
    def __contains__(self): pass
    def named_children(self): pass
    def children(self): pass
    def named_modules(self): pass
    def modules(self): pass
    def directParams(self): pass
    def parse(self): pass
    def apply(self): pass
    def clearProps(self): pass
    @property
    def displayF(self):
        """Function to display each ModuleSelector's lines.
Default is just::

    lambda mS: ", ".join(mS.props) """
        return self._displayF
    @displayF.setter
    def displayF(self, f):
        def applyF(self): self._displayF = f
        self.apply(applyF)
    def __getattr__(self, attr):
        if attr.startswith("_"): raise AttributeError(attr)
        if attr in self._children: return self._children[attr]
        return self.directParams[attr]
    def __getitem__(self, idx): return getattr(self, str(idx))
    @staticmethod
    def sample() -> "ModuleSelector":
        """Create a new example :class:`ModuleSelector` that has a bit of
hierarchy to them, with no css."""
        return nn.Sequential(nn.Linear(3, 4), nn.Sequential(nn.Conv2d(3, 8, 3, 2), nn.ReLU(), nn.Linear(5, 6)), nn.Linear(7, 8)).select("")
    def hookF(self): pass
    def hookFp(self): pass
    def hookB(self): pass
    def freeze(self): pass
    def unfreeze(self): pass
@k1lib.patch(nn.Module)
def select(model:"torch.nn.Module", css:str="*") -> "k1lib.selector.ModuleSelector":
    """Creates a new ModuleSelector, in sync with a model.
Example::

    mS = selector.select(nn.Linear(3, 4), "#root:propA")

Or, you can do it the more direct way::

    mS = nn.Linear(3, 4).select("#root:propA")

:param model: the :class:`torch.nn.Module` object to select from
:param css: the css selectors"""
    root = ModuleSelector(None, "root", model)
    root.parse(preprocess(css)); return root
@k1lib.patch(ModuleSelector, name="apply")
def _apply(self, f:Callable[[ModuleSelector], None]):
    """Applies a function to self and all child :class:`ModuleSelector`"""
    f(self)
    for child in self._children.values(): child.apply(f)
@k1lib.patch(ModuleSelector, name="parse")
def _parse(self, selectors:Union[List[str], str]) -> ModuleSelector:
    """Parses extra selectors. Clears all old selectors, but retain
the props. Returns self. Example::

    mS = selector.ModuleSelector.sample().parse("Conv2d:propA")
    # returns True
    "propA" in mS[1][0]

:param selectors: can be the preprocessed list, or the unprocessed css string"""
    if isinstance(selectors, str): selectors = preprocess(selectors)
    self.directSelectors = []; self.indirectSelectors = []
    ogSelectors = selectors
    if self.parent != None:
        selectors = [] + selectors + self.parent.indirectSelectors + self.parent.directSelectors
        self.indirectSelectors += self.parent.indirectSelectors
        self.depth = self.parent.depth + 1
    for selector in selectors:
        parts = _getParts(selector)
        matches = parts[0] == self.nn.__class__.__name__ or parts[0] == "#" + self.name or parts[0] == "*"
        if len(parts) == 1:
            if matches: self.props += _getProps(selector)
        else:
            a = selector.find(">"); a = a if a > 0 else float("inf")
            b = selector.find(" "); b = b if b > 0 else float("inf")
            direct = a < b
            if matches:
                if direct: self.directSelectors.append(selector[a+1:])
                else: self.indirectSelectors.append(selector[b+1:])
    for name, mod in self.nn.named_children():
        if name not in self._children:
            self._children[name] = ModuleSelector(self, name, mod)
        self._children[name].parse(ogSelectors)
    self.props = list(set(self.props)); return self
@k1lib.patch(ModuleSelector)
def __contains__(self, prop:str=None) -> bool:
    """Whether this :class:`ModuleSelector` has a specific prop.
Example::

    # returns True
    "b" in nn.Linear(3, 4).select("*:b")
    # returns False
    "h" in nn.Linear(3, 4).select("*:b")
    # returns True, "*" here means the ModuleSelector has any properties at all
    "*" in nn.Linear(3, 4).select("*:b")"""
    if "*" in self.props: return True
    if prop in self.props: return True
    if prop == "*" and len(self.props) > 0: return True
    return False
@k1lib.patch(ModuleSelector)
def named_children(self, prop:str=None) -> Iterator[Tuple[str, ModuleSelector]]:
    """Get all named direct childs.

:param prop: Filter property. See also: :meth:`__contains__`"""
    if prop is None: return self._children.items()
    return ((k, v) for k, v in self._children.items() if prop in v)
@k1lib.patch(ModuleSelector)
def children(self, prop:str=None) -> Iterator[ModuleSelector]:
    """Get all direct childs.

:param prop: Filter property. See also: :meth:`__contains__`"""
    return (x for _, x in self.named_children(prop))
@k1lib.patch(ModuleSelector, "directParams")
@property
def directParams(self) -> Dict[str, nn.Parameter]:
    """Dict params directly under this module"""
    return {name: param for name, param in self.nn.named_parameters() if "." not in name}
@k1lib.patch(ModuleSelector)
def named_modules(self, prop:str=None) -> Iterator[Tuple[str, ModuleSelector]]:
    """Get all named child recursively.
Example::

    modules = list(nn.Sequential(nn.Linear(3, 4), nn.ReLU()).select().named_modules())
    # return 3
    len(modules)
    # return tuple ('0', <ModuleSelector of Linear>)
    modules[1]

:param prop: Filter property. See also: :meth:`__contains__`"""
    if prop != None:
        yield from ((name, m) for name, m in self.named_modules() if prop in m)
        return
    yield self.name, self
    for child in self._children.values(): yield from child.named_modules()
@k1lib.patch(ModuleSelector)
def modules(self, prop:str=None) -> Iterator[ModuleSelector]:
    """Get all child recursively.

:param prop: Filter property. See also: :meth:`__contains__`"""
    for name, x in self.named_modules(prop): yield x
@k1lib.patch(ModuleSelector)
def clearProps(self) -> "ModuleSelector":
    """Clears all existing props of this and all descendants
:class:`ModuleSelector`. Example::

    # returns False
    "b" in nn.Linear(3, 4).select("*:b").clearProps()"""
    def applyF(self): self.props = []
    self.apply(applyF); return self
@k1lib.patch(ModuleSelector, name="deepestDepth")
@property
def deepestDepth(self):
    """Deepest depth of the tree. If self doesn't
have any child, then depth is 0"""
    if len(self._children) == 0: return 0
    return 1 + max([child.deepestDepth for child in self._children.values()])
@k1lib.patch(ModuleSelector)
def __repr__(self, intro:bool=True, header:Union[str, Tuple[str]]="", footer="", tabs:int=None):
    """
    :param intro: whether to include a nice header and footer info
    :param header:
        str: include a header that starts where `displayF` will start
        Tuple[str, str]: first one in tree, second one in displayF section
    :param footer: same thing with header, but at the end
    :param header: include a header that starts where `displayF` will start
    :param tabs: number of tabs at the beginning. Best to leave this empty
    """
    if tabs == None: tabs = 5 + self.deepestDepth
    answer = "ModuleSelector:\n" if intro else ""
    if header:
        h1, h2 = ("", header) if isinstance(header, str) else header
        answer += h1.ljust(tabs*4, " ") + h2 + "\n"
    answer += f"{self.name}: {self.nn.__class__.__name__}".ljust(tabs*4, " ")
    answer += self.displayF(self) + ("\n" if len(self._children) > 0 else "")
    answer += self._children.values() | cli.apply(lambda child: child.__repr__(tabs=tabs-1, intro=False).split("\n")) | cli.joinStreams() | cli.tab() | cli.join("\n")
    if footer:
        f1, f2 = ("", footer) if isinstance(footer, str) else footer
        answer += "\n" + f1.ljust(tabs*4, " ") + f2
    if intro: answer += f"""\n\nCan...
- mS.deepestDepth: get deepest depth possible
- mS.nn: get the underlying nn.Module object
- mS.apply(f): apply to self and all descendants
- "HookModule" in mS: whether this module has a specified prop
- mS.highlight(prop): highlights all modules with specified prop
- mS.parse([..., ...]): parses extra css
- mS.directParams: get Dict[str, nn.Parameter] that are directly under this module"""
    return answer
def _strTensor(t): return "None" if t is None else f"{t.shape}"
def strTensorTuple(ts):
    if len(ts) > 1:
        shapes = "\n".join(f"- {_strTensor(t)}" for t in ts)
        return f"tensors ({len(ts)} total) shapes:\n{shapes}"
    else:
        return f"tensor shape: {_strTensor(ts[0])}"
@k1lib.patch(ModuleSelector)
@contextmanager
def hookF(self, f:Callable[[ModuleSelector, "torch.nn.Module", Tuple[torch.Tensor], torch.Tensor], None]=None, prop:str="*"):
    """Context manager for applying forward hooks.
Example::

    def f(mS, i, o):
        print(i, o)

    m = nn.Linear(3, 4)
    with m.select().hookF(f):
        m(torch.randn(2, 3))

:param f: hook callback, should accept :class:`ModuleSelector`, inputs and output
:param prop: filter property of module to hook onto. If not specified, then it will print out input and output tensor shapes."""
    if f is None: f = lambda mS, i, o: print(f"Forward hook {m}:\n" + ([f"Input  {strTensorTuple(i)}", f"Output tensor shape: {o.shape}"] | cli.tab() | cli.join("\n")))
    g = lambda m, i, o: f(self, i, o)
    handles = [m.nn.register_forward_hook(g) for m in self.modules(prop)]
    try: yield
    finally:
        for h in handles: h.remove()
@k1lib.patch(ModuleSelector)
@contextmanager
def hookFp(self, f=None, prop:str="*"):
    """Context manager for applying forward pre hooks.
Example::

    def f(mS, i):
        print(i)

    m = nn.Linear(3, 4)
    with m.select().hookFp(f):
        m(torch.randn(2, 3))

:param f: hook callback, should accept :class:`ModuleSelector` and inputs
:param prop: filter property of module to hook onto. If not specified, then it will print out input tensor shapes."""
    if f is None: f = lambda mS, i: print(f"Forward pre hook {m}:\n" + ([f"Input {strTensorTuple(i)}"] | cli.tab() | cli.join("\n")))
    g = lambda m, i: f(self, i)
    handles = [m.nn.register_forward_pre_hook(g) for m in self.modules(prop)]
    try: yield
    finally:
        for h in handles: h.remove()
@k1lib.patch(ModuleSelector)
@contextmanager
def hookB(self, f=None, prop:str="*"):
    """Context manager for applying backward hooks.
Example::

    def f(mS, i, o):
        print(i, o)

    m = nn.Linear(3, 4)
    with m.select().hookB(f):
        m(torch.randn(2, 3)).sum().backward()

:param f: hook callback, should accept :class:`ModuleSelector`, grad inputs and outputs
:param prop: filter property of module to hook onto. If not specified, then it will print out input tensor shapes."""
    if f is None: f = lambda mS, i, o: print(f"Backward hook {m}:\n" + ([f"Input  {strTensorTuple(i)}", f"Output {strTensorTuple(o)}"] | cli.tab() | cli.join("\n")))
    g = lambda m, i, o: f(self, i, o)
    handles = [m.nn.register_full_backward_hook(g) for m in self.modules(prop)]
    try: yield
    finally:
        for h in handles: h.remove()
from contextlib import ExitStack
@contextmanager
def _freeze(self, value:bool, prop:str):
    modules = [m for m in self.modules(prop)]
    with ExitStack() as stack:
        for m in self.modules(prop):
            stack.enter_context(m.nn.gradContext())
            m.nn.requires_grad_(value)
        try: yield
        finally: pass
@k1lib.patch(ModuleSelector)
def freeze(self, prop:str="*"):
    """Returns a context manager that freezes (set requires_grad to False) parts of
the network. Example::

    l = k1lib.Learner.sample()
    w = l.model.lin1.lin.weight.clone() # weights before
    with l.model.select("#lin1").freeze():
        l.run(1)
    # returns True
    (l.model.lin1.lin.weight ==  w).all()"""
    return _freeze(self, False, prop)
@k1lib.patch(ModuleSelector)
def unfreeze(self, prop:str="*"):
    """Returns a context manager that unfreezes (set requires_grad to True) parts of
the network. Example::

    l = k1lib.Learner.sample()
    w = l.model.lin1.lin.weight.clone() # weights before
    with l.model.select("#lin1").freeze():
        with l.model.select("#lin1 > #lin").unfreeze():
            l.run(1)
    # returns False
    (l.model.lin1.lin.weight ==  w).all()"""
    return _freeze(self, True, prop)
class CutOff(nn.Module):
    def __init__(self, net, m):
        super().__init__()
        self.net = net; self.m = m; self._lastOutput = None
        def f(m, i, o): self._lastOutput = o
        self.handle = self.m.register_forward_hook(f)
    def forward(self, *args, **kwargs):
        self._lastOutput = None
        self.net(*args, **kwargs)
        return self._lastOutput
    def __del__(self): self.handle.remove()
@k1lib.patch(ModuleSelector)
def cutOff(self) -> nn.Module:
    """Creates a new network that returns the selected layer's output.
Example::

    xb = torch.randn(10, 2)
    m = nn.Sequential(nn.Linear(2, 5), nn.Linear(5, 4), nn.Linear(4, 6))
    m0 = m.select("#0").cutOff(); m1 = m.select("#1").cutOff()
    # returns (10, 6)
    m(xb).shape
    # returns (10, 5)
    m0(xb).shape == torch.Size([10, 5])
    # returns (10, 4)
    m1(xb).shape == torch.Size([10, 4])"""
    return CutOff(self.nn, self.modules("*") | cli.item() | cli.op().nn)