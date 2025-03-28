# AUTOGENERATED FILE! PLEASE DON'T EDIT HERE. EDIT THE SOURCE NOTEBOOKS INSTEAD
"""
This module allows you to make and combine a bunch of schedules, and setup the
optimizer so that it changes hyperparameter values based on the schedule. Highly
recommend you check out the `tutorials section <tutorials.html>`_ on this.
This is exposed automatically with::

   from k1lib.imports import *
   schedule.Fn # exposed
"""
import math, k1lib; import k1lib.cli as cli
plt = k1lib.dep.plt
import numpy as np
from itertools import accumulate
from k1lib.callbacks import Cbs, Callback
from typing import List, Callable, Union
__all__ = ["Fn", "linear", "smooth", "hump", "exp", "ParamScheduler"]
class Fn:                                                                        # Fn
    def __init__(self, f:Callable[[float], float], param:str=None):              # Fn
        """Creates a new schedule based on some custom function.
Example::

    s = schedule.Fn(lambda x: x**2)
    s(0.2) # returns 0.04

    # you can also use this as a decorator
    @schedule.Fn
    def s(x):
        return x**2

:param f: function (domain should always in [0, 1]), can be :class:`~k1lib.cli.modifier.op`
:param param: (optional) Parameter to schedule (e.g "lr") if using :class:`ParamScheduler`""" # Fn
        if isinstance(f, cli.op): f.op_solidify()                                # Fn
        self.f = f; self.param = param; self.progress = None                     # Fn
        self.domain = k1lib.Range(0, 1)                                          # Fn
    def __call__(self, x:float):                                                 # Fn
        """Get the current value."""                                             # Fn
        return self.f(x)                                                         # Fn
    def _startBatch(self, paramGroup:dict, progress:float):                      # Fn
        self.progress = progress                                                 # Fn
        paramGroup[self.param] = self(progress)                                  # Fn
    @property                                                                    # Fn
    def value(self): return self.f(self.progress)                                # Fn
    def __mul__(self, x): self.domain *= x; return self                          # Fn
    def __rmul__(self, x): self.domain *= x; return self                         # Fn
    def __truediv__(self, x): self.domain /= x; return self                      # Fn
    def __rtruediv__(self, x): self * (1.0/x); return self                       # Fn
    def __radd__(self, v):                                                       # Fn
        if isinstance(v, int): return self                                       # Fn
        return NotImplemented                                                    # Fn
    def __add__(self, s:Union["Fn", str]) -> "Fn":                               # Fn
        """If given :class:`Fn`, then combines the 2 schedules together.
If it's a string, then sets the current param to it."""                          # Fn
        if isinstance(s, Fn): return CombinedSchedule(self, s)                   # Fn
        self.param = s; return self                                              # Fn
    def iter(self, n:int):                                                       # Fn
        """Returns an n-step iterator evenly divided in range [0, 1].
Example::

    s = schedule.Fn(lambda x: x+2)
    list(s.iter(6)) # returns [2.0, 2.2, 2.4, 2.6, 2.8, 3.0]"""                  # Fn
        for e in np.linspace(0, 1, n): yield self(e)                             # Fn
    def modifyOutput(self, f:Callable[[float], float]) -> "Fn":                  # Fn
        """Returns a new :class:`Fn` that has its output modified.
Example::

    s = Fn(lambda x: x+2)
    s.modifyOutput(lambda x: x**2) # now s's function is (x+2)**2"""             # Fn
        return Fn(lambda x: f(self.f(x)), self.param)                            # Fn
@k1lib.patch(Fn)                                                                 # Fn
def __repr__(self):                                                              # __repr__
    plt.figure(dpi=100); c = dict(color="tab:green")                             # __repr__
    x = np.linspace(*self.domain, 1000); y = [self.f(x) for x in x]; plt.plot(x, y) # __repr__
    y = self(0); plt.plot(0, y, "o", **c); plt.annotate("(0, {:.1e})".format(y), (0, y)) # __repr__
    y = self(1); plt.plot(1, y, "o", **c); plt.annotate("(1, {:.1e})".format(y), (1, y)) # __repr__
    x = self.progress                                                            # __repr__
    if x is not None:                                                            # __repr__
        blur = not (x in k1lib.Range(0.1, 0.9))                                  # __repr__
        y = self(x); plt.plot(x, y, "o", **c, alpha=(0.5 if blur else 1))        # __repr__
        if not blur: plt.annotate("({:.1e}, {:.1e})".format(x, y), (x, y))       # __repr__
    plt.show()                                                                   # __repr__
    return f"""'{self.param}' schedule. Can...
- s.progress: to get last recorded progress
- s.value: to get last recorded hyper parameter's value
- s(0.3): to get value of schedule at 30% progress"""                            # __repr__
class CombinedSchedule(Fn):                                                      # CombinedSchedule
    def __init__(self, s1, s2):                                                  # CombinedSchedule
        split = s1.domain.stop / (s1.domain.delta + s2.domain.delta)             # CombinedSchedule
        s1r = k1lib.Range(0, split); s2r = k1lib.Range(split, 1)                 # CombinedSchedule
        def f(x):                                                                # CombinedSchedule
            if x < split: return s1.f(s1r.toUnit(x))                             # CombinedSchedule
            else: return s2.f(s2r.toUnit(x))                                     # CombinedSchedule
        super().__init__(f, s1.param or s2.param)                                # CombinedSchedule
def decorate(f:Callable[[float, float, float], float]) -> Fn:                    # decorate
    """Decorator, transforms f(low, high, x) to (low, high) -> f(x)."""          # decorate
    def _f(low, high, param:str=None):                                           # decorate
        return Fn(lambda x: f(low, high, x), param)                              # decorate
    return k1lib.wraps(f)(_f)                                                    # decorate
@decorate                                                                        # decorate
def linear(low, high, x):                                                        # linear
    """Sharply goes from low to high"""                                          # linear
    return low + x * (high - low)                                                # linear
@decorate                                                                        # linear
def smooth(low, high, x):                                                        # smooth
    """Smoothly goes from low to high"""                                         # smooth
    return low + (high - low) * (1 + math.cos(math.pi * (1-x))) / 2              # smooth
def hump(low, high, param:str=None):                                             # hump
    """Smoothly rises up (30%), then down (70%)"""                               # hump
    return 0.3*smooth(0.8 * low + 0.2 * high, high) + 0.7*smooth(high, low, param) # hump
_en4 = math.e**-3                                                                # hump
@decorate                                                                        # hump
def exp(low, high, x):                                                           # exp
    """Rises/drops quickly, then rate of change gets smaller and smaller"""      # exp
    return (math.exp(-x*4+1) - _en4) / (math.e - _en4) * (low - high) + high     # exp
@k1lib.patch(Cbs)                                                                # exp
class ParamScheduler(Callback):                                                  # ParamScheduler
    """Schedules a param in parts of the network.

:param css: the selected parts of the network to schedule
:param schedules: (obvious)"""                                                   # ParamScheduler
    def __init__(self, css:str, *schedules:List[Fn]):                            # ParamScheduler
        super().__init__(); self.css = css                                       # ParamScheduler
        for i, s in enumerate(schedules):                                        # ParamScheduler
            if s.param is None: raise RuntimeError(f"Schedule {i} does not have associated parameter! Set with `s.param = 'lr'`.") # ParamScheduler
        self.schedules = {s.param:s for s in schedules}                          # ParamScheduler
        self.groupId = None; self.dependsOn = set("ProgressBar")                 # ParamScheduler
        self.initialized = False; self.prop = None                               # ParamScheduler
    def endRun(self):                                                            # ParamScheduler
        ":meta private:"                                                         # ParamScheduler
        self.initialized = False                                                 # ParamScheduler
    def __getstate__(self):                                                      # ParamScheduler
        answer = dict(self.__dict__)                                             # ParamScheduler
        if "selector" in answer: del answer["selector"]                          # ParamScheduler
        return answer                                                            # ParamScheduler
    def startBatch(self):                                                        # ParamScheduler
        if self.l.model.training and self.groupId is not None:                   # ParamScheduler
            paramGroup = self.l.opt.param_groups[self.groupId]                   # ParamScheduler
            progress = self.l.progress                                           # ParamScheduler
            for schedule in self.schedules.values():                             # ParamScheduler
                schedule._startBatch(paramGroup, progress)                       # ParamScheduler
    def __repr__(self):                                                          # ParamScheduler
        print(f"{self._reprHead}, css: \"{self.css}\", selector prop: \"{self.prop}\", schedules:") # ParamScheduler
        for schedule in self.schedules.values(): schedule.__repr__()             # ParamScheduler
        return f"""Can...
- ps.schedules["lr"]: to get the schedule for a specific param
- ps.selector: to view the selected parameters
{self._reprCan}"""                                                               # ParamScheduler
@k1lib.patch(ParamScheduler, name="startRun")                                    # ParamScheduler
def _startRun(self):                                                             # _startRun
    if not self.initialized:                                                     # _startRun
        # get all other ParamSchedulers                                          # _startRun
        pss = [cb for cb in self.l.cbs if isinstance(cb, ParamScheduler) and not cb.suspended] # _startRun
        for i, ps in enumerate(pss):                                             # _startRun
            # make sure only 1 startRun is ran across all ParamSchedulers        # _startRun
            ps.initialized = True; ps.prop = f"_ps_{i}"                          # _startRun
            ps.selector = k1lib.selector.select(self.l.model, ps.css)            # _startRun
            # sort pss based on depth, so that deeper ones gets accounted for first # _startRun
            ps._depth = next(ps.selector.modules(ps.prop)).depth                 # _startRun
        pss = sorted(pss, key=lambda ps: -ps._depth)                             # _startRun
        # clear and add param groups                                             # _startRun
        self.l.opt.param_groups = []                                             # _startRun
        allParams = set(self.l.selector.nn.parameters())                         # _startRun
        for ps in pss:                                                           # _startRun
            params = set()                                                       # _startRun
            for m in ps.selector.modules(ps.prop):                               # _startRun
                for p in m.nn.parameters():                                      # _startRun
                    if p in allParams:                                           # _startRun
                        params.add(p); allParams.remove(p)                       # _startRun
            if len(params) > 0:                                                  # _startRun
                # so that we have a way to reference the group later on          # _startRun
                ps.groupId = len(self.l.opt.param_groups)                        # _startRun
                self.l.opt.add_param_group({"prop": ps.prop, "css": ps.css, "params": list(params), **self.l.opt.defaults}) # _startRun
        self.l.opt.add_param_group({"prop": "rest", "css": "*", "params": list(allParams), **self.l.opt.defaults}) # _startRun
        for ps in pss:                                                           # _startRun
            if ps.groupId is None: continue                                      # _startRun
            params = set(self.l.opt.param_groups[ps.groupId]["params"])          # _startRun
            def applyF(mS):                                                      # _startRun
                mS.displayF = lambda s: "*" if any(p in params for p in s.directParams.values()) else "" # _startRun
            ps.selector.apply(applyF)                                            # _startRun
