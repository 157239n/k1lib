# AUTOGENERATED FILE! PLEASE DON'T EDIT
import torch, k1lib, math, numpy as np
from torch import nn; from k1lib import cli
from typing import List, Tuple, ContextManager
from contextlib import contextmanager
__all__ = ["dummy"]
def dummy():
    """Does nothing. Only here so that you can read source code of this file and
see what’s up."""
    pass
@k1lib.patch(nn.Module)
def importParams(self:nn.Module, params:List[nn.Parameter]):
    """Given a list of :class:`torch.nn.parameter.Parameter`/:class:`torch.Tensor`,
update the current :class:`torch.nn.Module`'s parameters with it'"""
    for oldParam, newParam in zip(self.parameters(), params):
        oldParam.data = newParam.data.clone()
@k1lib.patch(nn.Module)
def exportParams(self:nn.Module) -> List[torch.Tensor]:
    """Gets the list of :class:`torch.Tensor` data"""
    return [param.data.clone() for param in self.parameters()]
class ParamsContext:
    def __init__(self, m:nn.Module): self.m = m
    def __enter__(self): self.params = self.m.exportParams(); return self.params
    def __exit__(self, *ignored): self.m.importParams(self.params)
@k1lib.patch(nn.Module)
@contextmanager
def paramsContext(self:nn.Module):
    """A nice context manager for :meth:`importParams` and :meth:`exportParams`.
Returns the old parameters on enter context. Example::

    m = nn.Linear(2, 3)
    with m.paramsContext() as oldParam:
        pass # go wild, train, mutate `m` however much you like
    # m automatically snaps back to the old param

Small reminder that this is not foolproof, as there are some :class:`~torch.nn.Module`
that stores extra information not accessible from the model itself, like
:class:`~torch.nn.BatchNorm2d`."""
    params = self.exportParams()
    try: yield
    finally: self.importParams(params)
@k1lib.patch(nn.Module)
def getParamsVector(model:nn.Module) -> List[torch.Tensor]:
    """For each parameter, returns a normal distributed random tensor
with the same standard deviation as the original parameter"""
    answer = []
    for param in model.parameters():
        a = torch.randn(param.shape).to(param.device)
        b = param.std() if param.numel() > 1 else 1
        answer.append(a * b)
    return answer
from k1lib.cli import apply, deref, op, item
@k1lib.patch(nn.Module)
@contextmanager
def deviceContext(self:nn.Module, buffers:bool=True) -> ContextManager:
    """Preserves the device of whatever operation is inside this.
Example::

    import torch.nn as nn
    m = nn.Linear(3, 4)
    with m.deviceContext():
        m.cuda() # moves whole model to cuda
    # automatically moves model to cpu

This is capable of preserving buffers' devices too. But it might be unstable.
:class:`~torch.nn.parameter.Parameter` are often updated inline, and they keep
their old identity, which makes it easy to keep track of which device the parameters
are on. However, buffers are rarely updated inline, so their identities change all
the time. To deal with this, this does something like this::

    devices = [buf.device for buf in self.buffers()]
    yield # entering context manager
    for buffer, device in zip(self.buffers(), devices):
        buffer.data = buffer.data.to(device=device)

This means that while inside the context, if you add a buffer anywhere to the
network, buffer-device alignment will be shifted and wrong. So, register all
your buffers (aka Tensors attached to :class:`~torch.nn.Module`) outside this context
to avoid headaches, or set ``buffers`` option to False.

If you don't know what I'm talking about, don't worry and just leave as default.

:param buffers: whether to preserve device of buffers (regular Tensors attached
    to :class:`~torch.nn.Module`) or not."""
    pDevs = self.parameters() | apply(lambda t: (t, t.device)) | deref()
    if buffers: pbDevs = pbDevs = self.modules() |\
        apply(lambda m: (m, m | op().buffers(recurse=False) | op().device.all() | deref())) | deref(maxDepth=1)
    try: yield
    finally:
        for p, dev in pDevs: p.data = p.data.to(device=dev)
        if buffers:
            for m, bDevs in pbDevs:
                for buf, dev in zip(m.buffers(recurse=False), bDevs):
                    buf.data = buf.data.to(device=dev)
@k1lib.patch(nn.Module)
@contextmanager
def gradContext(self):
    """Preserves the requires_grad attribute.
Example::

    m = nn.Linear(2, 3)
    with m.gradContext():
        m.weight.requires_grad = False
    # returns True
    m.weight.requires_grad

It's worth mentioning that this does not work with buffers (Tensors attached to
:class:`torch.nn.Module`), as buffers are not meant to track gradients!"""
    grads = [(p, p.requires_grad) for p in self.parameters()]
    try: yield
    finally:
        for p, grad in grads: p.requires_grad_(grad)
@k1lib.patch(nn.Module)
def __ror__(self, x):
    """Allows piping input to :class:`torch.nn.Module`, to match same style as
the module :mod:`k1lib.cli`. Example::

    # returns torch.Size([5, 3])
    torch.randn(5, 2) | nn.Linear(2, 3) | cli.shape()"""
    return self(x)
@k1lib.patch(nn.Module, name="nParams")
@property
def nParams(self):
    """Get the number of parameters of this module.
Example::

    # returns 9, because 6 (2*3) for weight, and 3 for bias
    nn.Linear(2, 3).nParams
"""
    return sum([p.numel() for p in self.parameters()])
@k1lib.patch(torch)
@k1lib.patch(torch.Tensor)
def crissCross(*others:Tuple[torch.Tensor]) -> torch.Tensor:
    """Concats multiple 1d tensors, sorts it, and get evenly-spaced values. Also
available as :meth:`torch.crissCross` and :meth:`~k1lib.cli.others.crissCross`.
Example::

    a = torch.tensor([2, 2, 3, 6])
    b = torch.tensor([4, 8, 10, 12, 18, 20, 30, 35])
    
    # returns tensor([2, 3, 6, 10, 18, 30])
    a.crissCross(b)
    
    # returns tensor([ 2,  4,  8, 10, 18, 20, 30, 35])
    a.crissCross(*([b]*10)) # 1 "a" and 10 "b"s
    
    # returns tensor([ 2,  2,  3,  6, 18])
    b.crissCross(*([a]*10)) # 1 "b" and 10 "a"s

Note how in the second case, the length is the same as tensor b, and the contents
are pretty close to b. In the third case, it's the opposite. Length is almost
the same as tensor a, and the contents are also pretty close to a."""
    return torch.cat([o.flatten() for o in others]).sort()[0][::len(others)]
@k1lib.patch(torch.Tensor)
def histBounds(self:torch.Tensor, bins=100) -> torch.Tensor:
    r"""Flattens and sorts the tensor, then get value of tensor at regular
linspace intervals. Does not guarantee bounds' uniqueness. Example::

    # Tensor with lots of 2s and 5s
    a = torch.Tensor([2]*5 + [3]*3 + [4] + [5]*4)
    # returns torch.tensor([2., 3., 5.])
    a.histBounds(3).unique()

The example result essentially shows 3 bins: :math:`[2, 3)`, :math:`[3, 5)` and
:math:`[5, \infty)`. This might be useful in scaling pixels so that networks handle
it nicely. Rough idea taken from fastai.medical.imaging."""
    sortedTensor = self.flatten().sort()[0]
    ls = torch.linspace(0, 1, bins); ls[-1] = 1-1e-6
    bigLs = (ls * len(sortedTensor)).long()
    return sortedTensor[bigLs]
@k1lib.patch(torch.Tensor)
def histScaled(self:torch.Tensor, bins=100, bounds=None) -> torch.Tensor:
    """Scale tensor's values so that the values are roughly spreaded out in range
:math:`[0, 1]` to ease neural networks' pain. Rough idea taken from
fastai.medical.imaging. Example::

    # normal-distributed values
    a = torch.randn(1000)
    # plot #1 shows a normal distribution
    plt.hist(a.numpy(), bins=30); plt.show()
    # plot #2 shows almost-uniform distribution
    plt.hist(a.histScaled().numpy()); plt.show()

Plot #1:

.. image:: images/histScaledNormal.png

Plot #2:

.. image:: images/histScaledUniform.png

:param bins: if ``bounds`` not specified, then will scale according to a hist
    with this many bins
:param bounds: if specified, then ``bins`` is ignored and will scale according to
    this. Expected this to be a sorted tensor going from ``min(self)`` to
    ``max(self)``."""
    if bounds is None: bounds = self.histBounds(bins).unique()
    else: bounds = bounds.unique()
    out = np.interp(self.numpy().flatten(), bounds, np.linspace(0, 1, len(bounds)))
    return torch.tensor(out).reshape(self.shape)
@k1lib.patch(torch.Tensor)
def positionalEncode(t:torch.Tensor, richFactor:float=2) -> torch.Tensor:
    r"""Position encode a tensor of shape :math:`(L, F)`, where :math:`L`
is the sequence length, :math:`F` is the encoded features. Will add the
encodings directly to the input tensor and return it.

This is a bit different from the standard implementations that ppl use.
This is exactly:

.. math:: p = \frac{i}{F\cdot richFactor}
.. math:: w = 1/10000^p
.. math:: pe = sin(w * L)

With ``i`` from range [0, F), and ``p`` the "progress". If ``richFactor`` is 1
(original algo), then ``p`` goes from 0% to 100% of the features. Example::

    import matplotlib.pyplot as plt, torch, k1lib
    plt.figure(dpi=150)
    plt.imshow(torch.zeros(100, 10).positionalEncode().T)

.. image:: images/positionalEncoding.png

:param richFactor: the bigger, the richer the features are. A lot of
    times, I observe that the features that are meant to cover huge scales
    are pretty empty and don't really contribute anything useful. So this
    is to bump up the usefulness of those features"""
    seqN, featsN = t.shape
    feats = torch.tensor(range(featsN)); w = (1/10000**(feats/featsN/richFactor))[None, :].expand(t.shape)
    times = torch.tensor(range(seqN))[:, None].expand(t.shape)
    t[:] = torch.sin(w * times); return t
@k1lib.patch(torch.Tensor)
def clearNan(self, value:float=0.0) -> torch.Tensor:
    """Sets all nan values to a specified value.
Example::

    a = torch.randn(3, 3) * float("nan")
    a.clearNan() # now full of zeros"""
    self[self != self] = value
    return self
@k1lib.patch(torch.Tensor)
def hasNan(self) -> bool:
    """Returns whether this Tensor has any nan values at all."""
    return (self != self).sum() > 0
@k1lib.patch(torch.Tensor)
def stats(self) -> Tuple[float, float]:
    return self.mean(), self.std()
inf = float("inf")
@k1lib.patch(torch.Tensor)
def hasInfs(self):
    """Whether this Tensor has negative or positive infinities."""
    return (self == inf).any() or (self == -inf).any()
@k1lib.patch(torch)
def loglinspace(a, b, n=100, **kwargs):
    """Like :meth:`torch.linspace`, but spread the values out in log space,
instead of linear space. Different from :meth:`torch.logspace`"""
    return math.e**torch.linspace(math.log(a), math.log(b), n, **kwargs)
try:
    import graphviz
    @k1lib.patch(graphviz.Digraph, "__call__")
    @k1lib.patch(graphviz.Graph, "__call__")
    def _call(self, _from, *tos, **kwargs):
        """Convenience method to quickly construct graphs.
Example::

    g = k1lib.graph()
    g("a", "b", "c")
    g # displays arrows from "a" to "b" and "a" to "c"
"""
        for to in tos: self.edge(_from, to, **kwargs)
    def digraph():
        """Convenience method for creating a new graphviz Digraph.
Example::

    g = k1lib.graph()
    g("a", "b", "c")
    g # displays arrows from "a" to "b" and "a" to "c"
"""
        return graphviz.Digraph(graph_attr={"rankdir":"TB"})
    def graph():
        """Convenience method for creating a new graphviz Graph. See also: :meth:`digraph`"""
        return graphviz.Graph(graph_attr={"rankdir":"TB"})
except ImportError:
    digraph = graph = lambda: print("Module `graphviz` not found! Please install it first, something like `pip install graphviz`")
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D, art3d
    @k1lib.patch(Axes3D)
    def march(self, heatMap, level:float=0, facecolor=[0.45, 0.45, 0.75], edgecolor=None):
        """Use marching cubes to plot surface of a 3d heat map.
Example::

    plt.k3d(6).march(k1lib.perlin3d(), 0.17)

.. image:: images/march.png

A more tangible example::

    t = torch.zeros(100, 100, 100)
    t[20:30,20:30,20:30] = 1
    t[80:90,20:30,40:50] = 1
    plt.k3d().march(t.numpy())

The function name is "march" because how it works internally is by using
something called marching cubes.

:param heatMap: 3d numpy array
:param level: array value to form the surface on"""
        from skimage import measure
        verts, faces, normals, values = measure.marching_cubes(heatMap, level)
        mesh = art3d.Poly3DCollection(verts[faces])
        if facecolor is not None: mesh.set_facecolor(facecolor)
        if edgecolor is not None: mesh.set_edgecolor(edgecolor)
        self.add_collection3d(mesh)
        self.set_xlim(0, heatMap.shape[0])
        self.set_ylim(0, heatMap.shape[1])
        self.set_zlim(0, heatMap.shape[2]); return self
    @k1lib.patch(Axes3D)
    def aspect(self):
        """Use the same aspect ratio for all axes."""
        self.set_box_aspect([ub - lb for lb, ub in (getattr(self, f'get_{a}lim')() for a in 'xyz')])
    @k1lib.patch(plt)
    def k3d(size=8, labels=True):
        """Convenience function to get an :class:`~mpl_toolkits.mplot3d.axes3d.Axes3D`.

:param labels: whether to include xyz labels or not
:param size: figure size"""
        fig = plt.figure(figsize=(size,size))
        ax = fig.add_subplot(projection="3d")
        if labels:
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
        return ax
    @k1lib.patch(plt)
    def animate(azimSpeed=1, azimStart=0, elevSpeed=0.3, elevStart=0, frames=60, close=True):
        """Animates the existing 3d axes.
Example::

    plt.k3d().scatter(*np.random.randn(3, 10))
    plt.animate()

:param frames: how many frames to render? Frame rate is 30 fps
:param close: whether to close the figure (to prevent the animation and
    static plot showing at the same time) or not"""
        fig = plt.gcf()
        def f(frame):
            for ax in fig.axes:
                ax.view_init(elevStart+frame*elevSpeed, azimStart+frame*azimSpeed)
        if close: plt.close()
        return k1lib.viz.FAnim(fig, f, frames)
except: pass
try:
    @k1lib.patch(Axes3D)
    def plane(self, origin, v1, v2=None, s1:float=1, s2:float=1, **kwargs):
        """Plots a 3d plane.

:param origin: origin vector, shape (3,)
:param v1: 1st vector, shape (3,)
:param v2: optional 2nd vector, shape(3,). If specified, plots a plane created
    by 2 vectors. If not, plots a plane perpendicular to the 1st vector
:param s1: optional, how much to scale 1st vector by
:param s2: optional, how much to scale 2nd vector by
:param kwargs: keyword arguments passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface`"""
        v1 = (v1 if isinstance(v1, torch.Tensor) else torch.tensor(v1)).float()
        if v2 is None:
            v = v1
            v1 = torch.tensor([1.0, 1, -(v[0]+v[1])/v[2]])
            v2 = torch.cross(v, v1)
        v2 = (v2 if isinstance(v2, torch.Tensor) else torch.tensor(v2)).float()
        origin = (origin if isinstance(origin, torch.Tensor) else torch.tensor(origin)).float()
        x = torch.linspace(-1, 1, 50)[:,None]
        v1 = (v1[None,:]*x*s1)[:,None]
        v2 = (v2[None,:]*x*s2)[None,:]
        origin = origin[None,None,:]
        plane = (origin + v1 + v2).permute(2, 0, 1)
        self.plot_surface(*plane.numpy(), **kwargs)
except: pass
try:
    @k1lib.patch(Axes3D)
    def point(self, v, **kwargs):
        """Plots a 3d point.

:param v: point location, shape (3,)
:param kwargs: keyword argument passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.scatter`"""
        v = (v if isinstance(v, torch.Tensor) else torch.tensor(v)).float()
        self.scatter(*v, **kwargs)
    @k1lib.patch(Axes3D)
    def line(self, v1, v2, **kwargs):
        """Plots a 3d line.

:param v1: 1st point location, shape (3,)
:param v2: 2nd point location, shape (3,)
:param kwargs: keyword argument passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot`"""
        self.plot(*torch.tensor([list(v1), list(v2)]).float().T, **kwargs)
except: pass
try:
    @k1lib.patch(Axes3D)
    def surface(self, z, **kwargs):
        """Plots 2d surface in 3d. Pretty much exactly the same as
:meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface`, but fields x and y
are filled in automatically. Example::

    x, y = np.meshgrid(np.linspace(-2, 2), np.linspace(-2, 2))
    plt.k3d(6).surface(x**3 + y**3)

.. image:: images/surface.png

:param z: 2d numpy array for the heights
:param kwargs: keyword arguments passed to ``plot_surface``"""
        if isinstance(z, torch.Tensor): z = z.numpy()
        x, y = z.shape
        x, y = np.meshgrid(np.array(range(y)), np.array(range(x)))
        return self.plot_surface(x, y, z, **kwargs)
except: pass