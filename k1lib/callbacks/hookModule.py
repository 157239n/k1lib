# AUTOGENERATED FILE! PLEASE DON'T EDIT HERE. EDIT THE SOURCE NOTEBOOKS INSTEAD
from .callbacks import Callback, Callbacks, Cbs
import k1lib; from k1lib import squeeze; import k1lib.cli as cli
from functools import partial; plt = k1lib.dep.plt
from typing import List, Tuple, Dict, Iterator, Union, Any, Callable
try: import torch; import torch.nn as nn; hasTorch = True
except:
    torch = k1lib.Object().withAutoDeclare(lambda: type("RandomClass", (object, ), {}))
    nn = k1lib.Object().withAutoDeclare(lambda: type("RandomClass", (object, ), {})); hasTorch = False
__all__ = ["HookModule"]
class Handles:                                                                   # Handles
    def __init__(self):                                                          # Handles
        self.forward = None; self.backward = None                                # Handles
    def remove(self):                                                            # Handles
        if self.active:                                                          # Handles
            self.forward.remove(); self.forward = None                           # Handles
            self.backward.remove(); self.backward = None                         # Handles
    @property                                                                    # Handles
    def active(self):                                                            # Handles
        if self.forward != None and self.backward != None: return True           # Handles
        elif self.forward == None and self.backward == None: return False        # Handles
        raise Exception("Supposed to be unreachable")                            # Handles
class Data(k1lib.Object):                                                        # Data
    def __init__(self):                                                          # Data
        super().__init__(); self.withAutoDeclare(lambda: [])                     # Data
class ModuleData:                                                                # ModuleData
    def __init__(self): self.forward = Data(); self.backward = Data()            # ModuleData
    def _plot(self, axes, field:str, rangeSlice:slice, f):                       # ModuleData
        forwardData = self.forward[field]; step = rangeSlice.step or 1           # ModuleData
        backwardData = self.backward[field]                                      # ModuleData
        if len(forwardData) == 0 or len(backwardData) == 0: return               # ModuleData
        fR, bR = k1lib.Range.proportionalSlice(len(forwardData), len(backwardData), rangeSlice) # ModuleData
        axes[0].plot(fR.range_[::step] | f | cli.deref(), forwardData[fR.slice_][::step] | f | cli.deref(), alpha=0.5) # ModuleData
        axes[1].plot(bR.range_[::step] | f | cli.deref(), backwardData[bR.slice_][::step] | f | cli.deref(), alpha=0.5) # ModuleData
    def __repr__(self):                                                          # ModuleData
        return """Module's saved data. can...
- d.forward: to get data stored during forward pass
- d.backward: to get data stored during backward pass"""                         # ModuleData
_Fn = Callable[[Data, nn.Module, Tuple[torch.Tensor], Tuple[torch.Tensor]], None] # ModuleData
class Function:                                                                  # Function
    def __init__(self, f:_Fn, name=None):                                        # Function
        self.f = f; self.name = name or "f(<no name>)"                           # Function
    def __call__(self, *args, **kwargs):                                         # Function
        self.f(*args, **kwargs)                                                  # Function
def hook(every, fns:List[Function], *args):                                      # hook
    if every.value: [fn(*args) for fn in fns]                                    # hook
class Module:                                                                    # Module
    def __init__(self, module:nn.Module):                                        # Module
        self.nn = module                                                         # Module
        self.handles = Handles()                                                 # Module
        self.data = ModuleData()                                                 # Module
        self.name = module.__class__.__name__                                    # Module
    def registerHooks(self, forwardFns:List[Function], backwardFns:List[Function], every): # Module
        self.handles.forward = self.nn.register_forward_hook(partial(hook, every, forwardFns, self.data.forward)) # Module
        self.handles.backward = self.nn.register_full_backward_hook(partial(hook, every, backwardFns, self.data.backward)) # Module
        return self                                                              # Module
    def unregisterHooks(self): self.handles.remove()                             # Module
    def __repr__(self):                                                          # Module
        return f"""Module `{self.name}`. Use...
- m.data: to get data stored
- m.nn: to get actual nn.Module object
- m.plot("means", "stds"): to plot simple statistics"""                          # Module
@k1lib.patch(Cbs)                                                                # Module
class HookModule(Callback):                                                      # HookModule
    """Hooks into selected modules in the network, and
execute functions like .mean(), .std(). This is fairly
complicated, and I highly recommend displaying this
callback in a cell for more info"""                                              # HookModule
    def __init__(self, persistent:bool=False):                                   # HookModule
        """
:param persistent: whether to save results across
    runs. If false, then can execute `.reset()` to
    reset everything"""                                                          # HookModule
        super(HookModule, self).__init__()                                       # HookModule
        self.modules:List[Module] = []                                           # HookModule
        self.forwardFns:List[Function] = []                                      # HookModule
        self.backwardFns:List[Function] = []                                     # HookModule
        self.cleanFns = []; self.persistent = persistent                         # HookModule
        self.every = k1lib.Every(3)                                              # HookModule
    def reset(self):                                                             # HookModule
        """Intended to be called by end user only, to reset
        everything if choose to persist results across runs."""                  # HookModule
        self._end(); self._start()                                               # HookModule
    def persist(self):                                                           # HookModule
        """By default, data will be erased and populated on each run. If
you want the data to persist across runs, call this."""                          # HookModule
        self.persistent = True                                                   # HookModule
    def startRun(self):                                                          # HookModule
        if (not self.persistent) or (len(self.modules) == 0): self._start()      # HookModule
    def startBatch(self): self.every()                                           # HookModule
    def _registerHooks(self):                                                    # HookModule
        for module in self.modules:                                              # HookModule
            module.registerHooks(self.forwardFns, self.backwardFns, self.every)  # HookModule
    def _unregisterHooks(self):                                                  # HookModule
        for module in self.modules: module.unregisterHooks()                     # HookModule
    def endRun(self):                                                            # HookModule
        if not self.persistent: self._end()                                      # HookModule
    def suspend(self):                                                           # HookModule
        self.actuallyRestore = len(self) == 0 or self[0].handles.active          # HookModule
        if self.actuallyRestore: self._unregisterHooks()                         # HookModule
    def restore(self):                                                           # HookModule
        if self.actuallyRestore:                                                 # HookModule
            self._registerHooks()                                                # HookModule
            self.actuallyRestore = False                                         # HookModule
    def __getitem__(self, idx):                                                  # HookModule
        if type(idx) == int: return self.modules[idx]                            # HookModule
        answer = HookModule(self.persistent)                                     # HookModule
        answer.modules = self.modules[idx]                                       # HookModule
        return answer                                                            # HookModule
    def __len__(self): return len(self.modules)                                  # HookModule
    def __repr__(self):                                                          # HookModule
        f = '\n'.join([f'  - {fn.name or str(fn)}' for fn in self.forwardFns])   # HookModule
        f = "" if f == "" else f"Forward hooks:\n{f}\n"                          # HookModule
        b = '\n'.join([f'  - {fn.name or str(fn)}' for fn in self.backwardFns])  # HookModule
        b = "" if b == "" else f"Backward hooks:\n{b}\n"                         # HookModule
        n = '\n'.join([f'  {i}. {data.name}' for i, data in enumerate(self)])    # HookModule
        excludes = {"withForwardHook", "withBackwardHook", "withHook", "withCheckpoint"} # HookModule
        withs = '\n'.join([f"- m.{key}()" for key in dir(self) if key.startswith("with") and key not in excludes]) # HookModule
        return f"""{super()._reprHead} with {len(self)} modules:\n{n}\n{f}{b}
Use...
- m.plot("means", "stds"): to plot simple statistics
- m[i]: to get a specific module
- m[a:b]: to get a new HookModule with selected modules
- m.css("..."): to select a specific subset of modules only
- m.withHook(hookCb): to hook a specific callback function
- m.clearHooks(): to clear all hooks
{super()._reprCan}

Built-in `with-` functions:\n{withs}"""                                          # HookModule
@k1lib.patch(HookModule)                                                         # HookModule
def _start(self):                                                                # _start
    self.modules = []                                                            # _start
    for nn, sel in zip(self.l.model.modules(), self.l.selector.modules()):       # _start
        if "HookModule" in sel: self.modules.append(Module(nn))                  # _start
    self._registerHooks()                                                        # _start
@k1lib.patch(HookModule)                                                         # _start
def _end(self):                                                                  # _end
    for module in self.modules:                                                  # _end
        for cleanFn in self.cleanFns:                                            # _end
            cleanFn(module.data)                                                 # _end
    self._unregisterHooks()                                                      # _end
@k1lib.patch(HookModule)                                                         # _end
def withForwardHook(self, hook:_Fn, name:str=None):                              # withForwardHook
    """Adds a hook to the forward pass. See :func:`~k1lib.callbacks.hookModule.HookModule.withHook`""" # withForwardHook
    self.forwardFns += [Function(hook, name)]; return self                       # withForwardHook
@k1lib.patch(HookModule)                                                         # withForwardHook
def withBackwardHook(self, hook:_Fn, name:str=None):                             # withBackwardHook
    """Adds a hook to the backward pass. See :func:`~k1lib.callbacks.hookModule.HookModule.withHook`""" # withBackwardHook
    self.backwardFns += [Function(hook, name)]; return self                      # withBackwardHook
@k1lib.patch(HookModule)                                                         # withBackwardHook
def withHook(self, hook:_Fn, name:str=None):                                     # withHook
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

See also: m.withForwardHook(), m.withBackwardHook()"""                           # withHook
    return self.withForwardHook(hook, name).withBackwardHook(hook, name)         # withHook
@k1lib.patch(HookModule)                                                         # withHook
def clearHooks(self):                                                            # clearHooks
    self._unregisterHooks()                                                      # clearHooks
    self.forwardFns = []; self.backwardFns = []                                  # clearHooks
    self.cleanFns = []; return self                                              # clearHooks
def meanCb(data, m, inp, out):                                                   # meanCb
    data.means.append(squeeze(out, hard=True).data.mean().item())                # meanCb
@k1lib.patch(HookModule)                                                         # meanCb
def withMeanRecorder(self):                                                      # withMeanRecorder
    """Records mean"""                                                           # withMeanRecorder
    return self.withHook(meanCb, "mean")                                         # withMeanRecorder
def stdCb(data, m, inp, out):                                                    # stdCb
    data.stds.append(squeeze(out, hard=True).data.std().item())                  # stdCb
@k1lib.patch(HookModule)                                                         # stdCb
def withStdRecorder(self):                                                       # withStdRecorder
    """Records standard deviation"""                                             # withStdRecorder
    return self.withHook(stdCb, "std")                                           # withStdRecorder
def minCb(data, m, inp, out):                                                    # minCb
    data.mins.append(squeeze(out, hard=True).data.min().item())                  # minCb
@k1lib.patch(HookModule)                                                         # minCb
def withMinRecorder(self):                                                       # withMinRecorder
    """Records min"""                                                            # withMinRecorder
    return self.withHook(minCb, "min")                                           # withMinRecorder
def maxCb(data, m, inp, out):                                                    # maxCb
    data.maxs.append(squeeze(out, hard=True).data.max().item())                  # maxCb
@k1lib.patch(HookModule)                                                         # maxCb
def withMaxRecorder(self):                                                       # withMaxRecorder
    """Records max"""                                                            # withMaxRecorder
    return self.withHook(maxCb, "max")                                           # withMaxRecorder
@k1lib.patch(HookModule)                                                         # withMaxRecorder
def css(self, css:str):                                                          # css
    answer = HookModule()                                                        # css
    selector = k1lib.selector.select(self.l.model, css)                          # css
    d = {m.nn: m for m in self.modules}                                          # css
    for sel in selector.modules():                                               # css
        if "HookModule" in sel and sel.nn in d:                                  # css
            answer.modules.append(d[sel.nn])                                     # css
    return answer                                                                # css
def plotF(modules:HookModule, fields:List[str], f, rangeSlice:slice):            # plotF
    fig, axes = plt.subplots(len(fields), 2, figsize=(10, 3*len(fields)), dpi=100) # plotF
    axes = axes.reshape((-1, 2))                                                 # plotF
    for axs, field in zip(axes, fields):                                         # plotF
        for module in modules:                                                   # plotF
            module.data._plot(axs, field, rangeSlice, f)                         # plotF
        axs[0].set_title(f"Forward {field}")                                     # plotF
        axs[1].set_title(f"Backward {field}")                                    # plotF
    plt.figlegend([f"{i}. {module.name}" for i, module in enumerate(modules)], loc='center right') # plotF
@k1lib.patch(HookModule)                                                         # plotF
@k1lib.patch(Module)                                                             # plotF
def plot(self, *fields:List[str], f=cli.iden()):                                 # plot
    """Plots every simple (1 number saved/pass/module) fields.

:param fields: list of fields to plot. If none, then
    will automatically find all simple fields"""                                 # plot
    modules = [self] if isinstance(self, Module) else self                       # plot
    if len(modules) == 0: raise Exception("No modules to plot!")                 # plot
    if len(fields) == 0:                                                         # plot
        fields = []; forwardData = modules[0].data.forward                       # plot
        for field in forwardData.state.keys():                                   # plot
            if field.startswith("_"): continue                                   # plot
            fieldData = forwardData[field]                                       # plot
            if type(fieldData) == list and k1lib.isNumeric(fieldData[0]):        # plot
                fields.append(field)                                             # plot
    return k1lib.viz.SliceablePlot(partial(plotF, modules, fields, f))           # plot
