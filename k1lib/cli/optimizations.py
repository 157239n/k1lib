# AUTOGENERATED FILE! PLEASE DON'T EDIT
"""This is for optimizing the hell out of cli tools. Optimizations
that focus around a specific cli should be included close to their
definitions, so this is for optimizations that unusually span multiple
clis, and serve as examples of how to create optimization passes.

See over the `LLVM optimizer tutorial <llvm.html>`_ for more background."""
import k1lib.cli as cli
from k1lib.cli.typehint import *
from k1lib.cli.init import yieldT
from collections import defaultdict
import k1lib

__all__ = ["dummy"]
def dummy():
    """Does nothing. Only here so that you can read the source code"""
#tOpt.clearPasses(); tOpt.n = 10
def setHints(cs, ts, metadata):
    s = cs[0]; t = ts[0]; #print(f"hints {metadata} - {[c.__class__.__name__ for c in s.clis]}")
    for c in s.clis: c._inHint = t; t = c._typehint(t) or tAny(); c._outHint = t
tOpt.addPass(setHints, [cli.serial], 14) # for adding extra hints to cli objects
def oUnwrapSerial(cs, ts, metadata):
    if len(metadata["route"]) < 2: return None
    s = metadata["route"][-2]
    if s == "apply" or s == "mtmS" or s == "oneToMany": return None
    #print(f"unwrap serial {metadata} {[c.__class__.__name__ for c in cs[0].clis]}")
    return cs[0].clis
tOpt.addPass(oUnwrapSerial , [cli.serial], 1) # for unwrapping serial
tOpt.addPass(lambda cs, ts, _: [cs[1], cs[0]], [cli.toList, cli.head]) # for swapping heads around
def stripSerial(c):
    if c is None: return None
    while isinstance(c, cli.serial) and len(c.clis) == 1: c = c.clis[0]
    return c
def prepareSerial(c): # basically prepares input clis so that they can be recursively optimized by `apply` and `mtmS`
    c = stripSerial(c); return cli.serial(c) if isinstance(c, cli.serial) else cli.serial(cli.serial(c))
def oApply(cs, ts, metadata): # for going into apply
    a = cs[0]; t = ts[0]; #print(f"apply {metadata} {cs} {ts} {a.f.clis}")
    if a.column is None and isinstance(a.f, cli.BaseCli):
        metadata["route"].append("apply");
        res = stripSerial(cli.typehint.serialOpt(prepareSerial(a.f), t.item(), metadata))
        metadata["route"].pop(); #print(f"res: {res}")
        if res is not None: return [cli.apply(res)]
    return None
tOpt.addPass(oApply, [cli.apply])
def oMtmS(cs, ts, metadata):
    m = cs[0]; n = len(m.clis); newClis = []; atLeastOnce = False
    ts = m._inpTypeHintExpand(ts[0])
    metadata["route"].append("mtmS")
    for c, t in zip(m.clis, ts):
        res = stripSerial(cli.typehint.serialOpt(prepareSerial(c), t, metadata))
        if res is not None: atLeastOnce = True
        newClis.append(res)
    metadata["route"].pop()
    if atLeastOnce: return [cli.mtmS(*newClis)]
tOpt.addPass(oMtmS, [cli.mtmS])
def oOneToMany(cs, ts, metadata):
    o = cs[0]; t = ts[0]; atLeastOnce = False; newClis = []
    metadata["route"].append("oneToMany")
    for c in o.clis:
        res = stripSerial(cli.typehint.serialOpt(prepareSerial(c), t, metadata))
        if res is not None: atLeastOnce = True
        newClis.append(res)
    metadata["route"].pop()
    if atLeastOnce: return [cli.oneToMany(*newClis)]
tOpt.addPass(oOneToMany, [cli.oneToMany])
def basics():
    tOpt.addPass(oApply, [cli.apply])
    tOpt.addPass(oMtmS, [cli.mtmS])
    tOpt.addPass(oOneToMany, [cli.oneToMany])
def oFileLength(cs, ts, _):
    c, s = cs;
    if s.idx != 0: return None
    return [cli.aS(lambda fn: None | cli.cmd(f"wc -l {fn}") | cli.item() | cli.op().split(" ")[0].ab_int())]
tOpt.addPass(oFileLength, [cli.cat().__class__, cli.shape], 9)