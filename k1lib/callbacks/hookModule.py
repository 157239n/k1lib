# AUTOGENERATED FILE! PLEASE DON'T EDIT
from k1lib.callbacks import Callback, Callbacks
import k1lib; from k1lib import squeeze
import torch; import torch.nn as nn
from functools import partial
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Iterator, Union, Any, Callable
__all__ = ["HookModule"]
class Handles:
    def __init__(self):
        self.forward = None; self.backward = None
    def remove(self):
        if self.active:
            self.forward.remove(); self.forward = None
            self.backward.remove(); self.backward = None
    @property
    def active(self):
        if self.forward != None and self.backward != None: return True
        elif self.forward == None and self.backward == None: return False
        raise Exception("Supposed to be unreachable")
class Data(k1lib.Object):
    def __init__(self):
        super().__init__(); self.withAutoDeclare(lambda: [])
class ModuleData:
    def __init__(self): self.forward = Data(); self.backward = Data()
    def _plot(self, axes, field:str, rangeSlice:slice):
        forwardData = self.forward[field]; step = rangeSlice.step or 1
        backwardData = self.backward[field]
        fR, bR = k1lib.Range.proportionalSlice(len(forwardData), len(backwardData), rangeSlice)
        axes[0].plot(fR.range_[::step], forwardData[fR.slice_][::step], alpha=0.5)
        axes[1].plot(bR.range_[::step], backwardData[bR.slice_][::step], alpha=0.5)
    def __repr__(self):
        return """Module's saved data. can...
- d.forward: to get data stored during forward pass
- d.backward: to get data stored during backward pass"""
Fn = Callable[[Data, nn.Module, Tuple[torch.Tensor], Tuple[torch.Tensor]], None]
class Function:
    def __init__(self, f:Fn, name=None):
        self.f = f; self.name = name or "f(<no name>)"
    def __call__(self, *args, **kwargs):
        self.f(*args, **kwargs)
def hook(fns:List[Function], *args): [fn(*args) for fn in fns]
class Module:
    def __init__(self, module:nn.Module):
        self.nnModule = module
        self.handles = Handles()
        self.data = ModuleData()
        self.name = module.__class__.__name__
    def registerHooks(self, forwardFns:List[Function], backwardFns:List[Function]):
        self.handles.forward = self.nnModule.register_forward_hook(partial(hook, forwardFns, self.data.forward))
        self.handles.backward = self.nnModule.register_backward_hook(partial(hook, backwardFns, self.data.backward))
        return self
    def unregisterHooks(self): self.handles.remove()
    def __repr__(self):
        return f"""Module `{self.name}`. Use...
- m.data: to get data stored
- m.nnModule: to get actual nn.Module object
- m.plot("means", "stds"): to plot simple statistics"""
@k1lib.patch(Callback.cls)
class HookModule(Callback):
    """Hooks into selected modules in the network, and
execute functions like .mean(), .std(). This is fairly
complicated, and I highly recommend displaying this
callback in a cell for more info"""
    def __init__(self, persistent:bool=False):
        """
:param persistent: whether to save results across
    runs. If false, then can execute `.reset()` to
    reset everything"""
        super(HookModule, self).__init__()
        self.modules:List[Module] = []
        self.forwardFns:List[Function] = []
        self.backwardFns:List[Function] = []
        self.cleanFns = []; self.persistent = persistent
    def reset(self):
        """Intended to be called by end user only, to reset
        everything if choose to persist results across runs."""
        self._end(); self._start()
    def startRun(self):
        if (not self.persistent) or (len(self.modules) == 0): self._start()
    def _registerHooks(self):
        for module in self.modules:
            module.registerHooks(self.forwardFns, self.backwardFns)
    def _unregisterHooks(self):
        for module in self.modules: module.unregisterHooks()
    def endRun(self):
        if not self.persistent: self._end()
    def suspend(self):
        self.actuallyRestore = len(self) == 0 or self[0].handles.active
        if self.actuallyRestore: self._unregisterHooks()
    def restore(self):
        if self.actuallyRestore:
            self._registerHooks()
            self.actuallyRestore = False
    def __getitem__(self, idx):
        if type(idx) == int: return self.modules[idx]
        answer = HookModule(self.persistent)
        answer.modules = self.modules[idx]
        return answer
    def __len__(self): return len(self.modules)
    def __repr__(self):
        f = '\n'.join([f'  - {fn.name or str(fn)}' for fn in self.forwardFns])
        f = "" if f == "" else f"Forward hooks:\n{f}\n"
        b = '\n'.join([f'  - {fn.name or str(fn)}' for fn in self.backwardFns])
        b = "" if b == "" else f"Backward hooks:\n{b}\n"
        n = '\n'.join([f'  {i}. {data.name}' for i, data in enumerate(self)])
        excludes = {"withForwardHook", "withBackwardHook", "withHook", "withCheckpoint"}
        withs = '\n'.join([f"- m.{key}()" for key in dir(self) if key.startswith("with") and key not in excludes])
        return f"""{super()._reprHead} with {len(self)} modules:\n{n}\n{f}{b}
Use...
- m.plot("means", "stds"): to plot simple statistics
- m[i]: to get a specific module
- m[a:b]: to get a new HookModule with selected modules
- m.css("..."): to select a specific subset of modules only
- m.withHook(hookCb): to hook a specific callback function
- m.clearHooks(): to clear all hooks
{super()._reprCan}

Built-in `with-` functions:\n{withs}"""
@k1lib.patch(HookModule)
def _start(self):
    self.modules = []
    for nnModule, sel in zip(self.model.modules(), self.selector.modules()):
        if sel.selected("HookModule"): self.modules.append(Module(nnModule))
    self._registerHooks()
@k1lib.patch(HookModule)
def _end(self):
    for module in self.modules:
        for cleanFn in self.cleanFns:
            cleanFn(module.data)
    self._unregisterHooks()
@k1lib.patch(HookModule)
def withForwardHook(self, hook:Fn, name:str=None):
    """Adds a hook to the forward pass. See :func:`~k1lib.callbacks.hookModule.HookModule.withHook`"""
    self.forwardFns += [Function(hook, name)]; return self
@k1lib.patch(HookModule)
def withBackwardHook(self, hook:Fn, name:str=None):
    """Adds a hook to the backward pass. See :func:`~k1lib.callbacks.hookModule.HookModule.withHook`"""
    self.backwardFns += [Function(hook, name)]; return self
@k1lib.patch(HookModule)
def withHook(self, hook:Fn, name:str=None):
    """Adds a hook to both the forward and backward pass.

:param hook: this function is expected to take in these parameters: **(data, module, inp, out)**

    :data: the injected dependency for you to store stuff.
        Initially, `data.max` is an empty list, and you can
        append to it directly, like this::

            data.max.append() # okay

        Later on, you can do things like::

            HookModule[i].forward.max

        and get the data you saved from the hook.
    :module: the module this function hooks into. Please
        refer to :func:`torch.nn.Module.register_forward_hook()` to
        know more.
    :inp: input (or grad of input) to the module
    :out: output (or grad of output) to the module
:param name: custom name for the function for nice displaying

See also: m.withForwardHook(), m.withBackwardHook()"""
    return self.withForwardHook(hook, name).withBackwardHook(hook, name)
@k1lib.patch(HookModule)
def clearHooks(self):
    self._unregisterHooks()
    self.forwardFns = []; self.backwardFns = []
    self.cleanFns = []; return self
def meanCb(data, m, inp, out):
    data.means.append(squeeze(out).data.mean().item())
@k1lib.patch(HookModule)
def withMeanRecorder(self):
    """Records mean"""
    return self.withHook(meanCb, "mean")
def stdCb(data, m, inp, out):
    data.stds.append(squeeze(out).data.std().item())
@k1lib.patch(HookModule)
def withStdRecorder(self):
    """Records standard deviation"""
    return self.withHook(stdCb, "std")
def minCb(data, m, inp, out):
    data.mins.append(squeeze(out).data.min().item())
@k1lib.patch(HookModule)
def withMinRecorder(self):
    """Records min"""
    return self.withHook(minCb, "min")
def maxCb(data, m, inp, out):
    data.maxs.append(squeeze(out).data.max().item())
@k1lib.patch(HookModule)
def withMaxRecorder(self):
    """Records max"""
    return self.withHook(maxCb, "max")
@k1lib.patch(HookModule)
def css(self, css:str):
    answer = HookModule()
    selector = k1lib.selector.select(self.model, css)
    d = {m.nnModule: m for m in self.modules}
    for nnModule, sel in zip(self.model.modules(), selector.modules()):
        if sel.selected("HookModule") and sel.nnModule in d:
            answer.modules.append(d[sel.nnModule])
    return answer
def plotF(modules:HookModule, fields:List[str], rangeSlice:slice):
    fig, axes = plt.subplots(len(fields), 2, figsize=(10, 3*len(fields)), dpi=100)
    axes = axes.reshape((-1, 2))
    for axs, field in zip(axes, fields):
        for module in modules:
            module.data._plot(axs, field, rangeSlice)
        axs[0].set_title(f"Forward {field}")
        axs[1].set_title(f"Backward {field}")
    plt.figlegend([f"{i}. {module.name}" for i, module in enumerate(modules)], loc='center right')
@k1lib.patch(HookModule)
@k1lib.patch(Module)
def plot(self, *fields:List[str]):
    """Plots every simple (1 number saved/pass/module) fields.

:param fields: list of fields to plot. If none, then
    will automatically find all simple fields"""
    modules = [self] if isinstance(self, Module) else self
    if len(modules) == 0: raise Exception("No modules to plot!")
    if len(fields) == 0:
        fields = []; forwardData = modules[0].data.forward
        for field in forwardData.state.keys():
            if field.startswith("_"): continue
            fieldData = forwardData[field]
            if type(fieldData) == list and k1lib.isNumeric(fieldData[0]):
                fields.append(field)
    return k1lib.viz.SliceablePlot(partial(plotF, modules, fields))
@k1lib.patch(Callbacks, docs=HookModule)
def withHookModule(self, persistent=True):
    return self.append(HookModule(persistent).withMeanRecorder().withStdRecorder())