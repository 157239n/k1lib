# AUTOGENERATED FILE! PLEASE DON'T EDIT
"""
Some nice utils to complement :mod:`torch.nn`. This is exposed automatically
with::

   from k1lib.imports import *
   knn.Lambda # exposed
"""
from torch import nn
from typing import Callable, Any
__all__ = ["Lambda", "Identity", "LinBlock", "MultiheadAttention"]
class Lambda(nn.Module):
    def __init__(self, f:Callable[[Any], Any]):
        """Creates a simple module with a specified :meth:`forward`
function."""
        super().__init__(); self.f = f
    def forward(self, x): return self.f(x)
class Identity(Lambda):
    """Creates a module that returns the input in :meth:`forward`"""
    def __init__(self): super().__init__(lambda x: x)
class LinBlock(nn.Module):
    def __init__(self, inC, outC):
        """Linear layer with relu behind it"""
        super().__init__(); self.lin = nn.Linear(inC, outC); self.relu = nn.ReLU()
    def forward(self, x):
        return x | self.lin | self.relu
class MultiheadAttention(nn.Module):
    def __init__(self, qdim, kdim, vdim, embed, head=4, outdim=None):
        """Kinda like :class:`torch.nn.MultiheadAttention`, just simpler, shorter, and clearer.
Probably not as fast as the official version, and doesn't have masks and whatnot, but easy to read!
Example::

    xb = torch.randn(14, 32, 35) # (S, N, ), or sequence size 14, batch size 32, feature size 35
    # returns torch.Size([14, 32, 50])
    MultiheadAttention(35, 35, 35, 9, 4, 50)(xb).shape

Although you can use this right away with no mods, I really encourage you to copy and paste the
source code of this and modify it to your needs.

:param qdim: Basic query, key and value dimensions
:param embed: a little different from :class:`torch.nn.MultiheadAttention`, as this is after splitting into heads
:param outdim: if not specified, then equals to ``embed * head``"""
        super().__init__()
        self.embed = embed; self.head = head; outdim = outdim or embed*head
        self.qdim = qdim; self.wq = nn.Linear(qdim, head*embed)
        self.kdim = kdim; self.wk = nn.Linear(kdim, head*embed)
        self.vdim = vdim; self.wv = nn.Linear(vdim, head*embed)
        self.outLin = nn.Linear(head*embed, outdim)
        self.softmax = nn.Softmax(-1)
    def forward(self, query, key=None, value=None):
        """If ``key`` or ``value`` is not specified, just default to ``query``."""
        if key is None: key = query
        if value is None: value = query
        S, N, *_ = key.shape; F = self.embed; head = self.head
        q = self.wq(query); k = self.wk(key); v = self.wv(value)
        S1 = q.shape[0]
        if q.shape[1] != k.shape[1]: q = q.expand(-1, k.shape[1], -1).contiguous()
        q = q.view(S1, -1, F).transpose(0, 1)
        k = k.view(S, -1, F).transpose(0, 1)
        v = v.view(S, -1, F).transpose(0, 1)
        mat = self.softmax((q / math.sqrt(F)) @ k.transpose(1, 2))
        return self.outLin((mat @ v).transpose(0, 1).reshape(S1, N, head*F))