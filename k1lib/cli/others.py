# AUTOGENERATED FILE! PLEASE DON'T EDIT
"""
This is for pretty random clis that's scattered everywhere.
"""
__all__ = ["crissCross"]
from typing import Callable, Iterator, Any, Union, List
from k1lib.cli import BaseCli; from k1lib import cli
import torch
def crissCross():
    """Like the monkey-patched function :meth:`torch.crissCross`.
Example::

    # returns another Tensor
    [torch.randn(3, 3), torch.randn(3)] | crissCross()"""
    return cli.applyS(lambda x: torch.crissCross(*x))