# AUTOGENERATED FILE! PLEASE DON'T EDIT
"""
This module is for dealing with xml stuff
"""
import k1lib.bioinfo.cli as _cli
import xml.etree.ElementTree as _ET
import copy as _copy
from typing import Iterator as _Iterator
class node(_cli.init.BaseCli):
    """Turns lines into a single node"""
    def __ror__(self, it:_Iterator[str]) -> _Iterator[_ET.Element]:
        yield _ET.fromstring("".join(it))
def _maxDepth(node, maxDepth:int, depth:int=0):
    if depth >= maxDepth:
        while len(node) > 0: del node[0]
    for n in node: _maxDepth(n, maxDepth, depth+1)
    return node
class maxDepth(_cli.init.BaseCli):
    def __init__(self, depth:int=None, copy:bool=True):
        """Filters out too deep nodes

:param depth: max depth to include in
:param copy: whether to limit the nodes itself, or limit a copy"""
        self.depth = depth or float("inf")
        self.copy = copy
    def __ror__(self, nodes:_Iterator[_ET.Element]) -> _Iterator[_ET.Element]:
        for node in nodes:
            if self.copy: node = _copy.deepcopy(node)
            yield _maxDepth(node, self.depth)
def _tag(node, tag:str):
    if node.tag == tag: yield node
    else:
        for n in node: yield from _tag(n, tag)
class tag(_cli.init.BaseCli):
    def __init__(self, tag:str):
        """Finds all tags that have a particular name. If
found, then don't search deeper"""
        self.tag = tag
    def __ror__(self, nodes:_Iterator[_ET.Element]) -> _Iterator[_ET.Element]:
        for node in nodes: yield from _tag(node, self.tag)
def _pretty(node, depth:int=0, indents=[]):
    attr = "".join([f" {k}=\"{v}\"" for k, v in node.attrib.items()])
    if len(node) == 0:
        yield indents[depth] + f"<{node.tag}{attr}/>"
    else:
        yield indents[depth] + f"<{node.tag}{attr}>"
        for n in node: yield from _pretty(n, depth+1, indents)
        yield indents[depth] + f"</{node.tag}>"
class pretty(_cli.init.BaseCli):
    def __init__(self, indent:str=None):
        self.indent = _cli.init.patchDefaultIndent(indent)
    def __ror__(self, it:_Iterator[_ET.Element]) -> _Iterator[str]:
        indents = [i*self.indent for i in range(100)]
        for node in it: yield from _pretty(node, indents=indents)
class display(_cli.init.BaseCli):
    def __init__(self, depth:int=3, lines:int=20):
        """Convenience method for getting head, make it pretty and print it out"""
        self.depth = depth; self.lines = lines
    def __ror__(self, it:_Iterator[_ET.Element], lines=10):
        if self.depth is not None: it = it | maxDepth(self.depth)
        it = it | pretty()
        if self.lines is not None: it = it | _cli.head(self.lines)
        it > _cli.stdout