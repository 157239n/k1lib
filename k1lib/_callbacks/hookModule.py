# AUTOGENERATED FILE! PLEASE DON'T EDIT
from k1lib.callbacks import Callback, Callbacks
import k1lib
from functools import partial
from k1lib import getFirst as _getFirst
import matplotlib.pyplot as plt
@k1lib.patch(Callback.cls)
class HookModule(Callback, k1lib.ListContainer):
    """Records means and std of output of individual
    modules on both forward and backward pass. Erases
    info before each run.

    Args:
        persistent: whether to save results across runs.
            This comes in handy if your network is pretty
            heavy. If false, then can execute `.reset()` to
            reset everything

    Can pass through additional forward and backward
    callbacks. There are several methods for that:
        .withForwardHook(). This literally just appends the
            hook to the variable `.forwardFns`
        .withBackwardHook(). This literally just appends the
            hook to the variable `.backwardFns`
        .withHook(). Just calls the 2 functions above

    You can manipulate `.forwardFns` and `.backwardFns`
    directly. But if you need quality of life stuff, here
    are more methods:
        .clearHooks()

    After a learner is created and bound with a Callbacks,
    you can add a hook like this:
    >>> learner.HookModule.withMeanRecorder()

    There are a few built in hooks that you can check out:
        .withMeanRecorder()
        .withStdRecorder()
        .withMinRecorder()
        .withMaxRecorder()
        .withHistRecorder()

    By default, this will analyze `learner.model`, but
    you can change that like this:
    >>> learner.HookModule.module = <intended nn.Module object>

    After a run, you can access a module's data by exploring these:
    >>> learner.HookModule[i].forward.<field>
    >>> learner.HookModule[i].backward.<field>
    `<field>` is any field you pass to `data` in the hook
    you passed to `.withHook`

    If your field is just a simple list of numbers, you
    can plot all values in all modules using `.plot()`:
    >>> learner.HookModule.plot()"""
    def __init__(self, persistent:bool):
        super(HookModule, self).__init__()
        # ListContainer structure: [{name: ..., forward: {}, backward: {}}]. forward and backward are reference objects to store data
        self._handles = [] # the hook handles returned by pytorch at startRun, so that we can remove them later on
        self.forwardFns = []; self.backwardFns = [] # lsit of forward and backward hooks
        self.cleanFns = []; self._module = None
        self.running = False # state variable, to make sure we exit (free hooks) once and only once
        self.simpleFields = [] # list of fields:str that are pretty simple, and only saves a single number/pass/module, like "means". This is just to aid usability in the .plot() function
        self.persistent = persistent
    @property
    def module(self): return self._module or self.model.modules()
    @module.setter
    def module(self, module): self._module = module
    def reset(self):
        """Intended to be called by end user only, to reset
        everything if choose to persist results across runs."""
        self._end(); self._start()
    def startRun(self):
        if (not self.persistent) or (len(self._handles) == 0):
            self._start()
    def _wrappingUp(self):
        if not self.persistent: self._end()
    def endRun(self): self._wrappingUp()
    def cancelBatch(self): self._wrappingUp()
    def cancelEpoch(self): self._wrappingUp()
    def cancelRun(self): self._wrappingUp()
    def suspend(self): self._unregisterHooks()
    def restore(self): self._registerHooks()
    def __getstate__(self):
        state = super().__getstate__()
        del state["_handles"]
        return state
    def __repr__(self):
        f = '\n'.join([f'  - {fn.name or str(fn)}' for fn in self.forwardFns])
        b = '\n'.join([f'  - {fn.name or str(fn)}' for fn in self.backwardFns])
        n = '\n'.join([f'  {i}. {data.name}' for i, data in enumerate(self)])
        return f"""{super()._reprHead} with {len(self)} modules:\n{n}\n
Forward hooks:\n{f}
Backward hooks:\n{b}

Use...
- m.plot("means", "stds"): to plot simple statistics
- m[i]: to get a specific module
- m.withHook(hookCb): to hook a specific callback
{super()._reprCan}"""
def hook(fns, *args): [fn(*args) for fn in fns]
@k1lib.patch(HookModule)
def _registerHooks(self): # helper method only
    for module, data in zip(self.module, self):
        self._handles.append(module.register_forward_hook(partial(hook, self.forwardFns, data.forward)))
        self._handles.append(module.register_backward_hook(partial(hook, self.backwardFns, data.backward)))
@k1lib.patch(HookModule)
def _unregisterHooks(self): # helper method only
    for handle in self._handles:
        handle.remove()
@k1lib.patch(HookModule)
def _start(self):
    self.clear()
    self._handles = []
    for module in self.module:
        data = k1lib.Object.fromDict({"forward": k1lib.Object().withAutoDeclare(k1lib.Object.listGenerator)\
                                          .withRepr("Use .means, .stds, or other custom fields you defined in your hook"),
                                      "backward": k1lib.Object().withAutoDeclare(k1lib.Object.listGenerator)\
                                          .withRepr("Use .means, .stds, or other custom fields you defined in your hook"),
                                      "name": module.__class__.__name__})
        data.repr = f"Module `{data.name}`. Use...\n- m.forward for data stored during forward pass\n- m.backward for data stored during backward pass"
        self.append(data)
    self._registerHooks()
@k1lib.patch(HookModule)
def _end(self):
    if self.running: # make sure to only execute once when training ends
        for moduleData in self:
            for cleanFn in self.cleanFns:
                cleanFn(moduleData.forward, moduleData.backward)
        self._unregisterHooks()
        self.running = False
def plotF(self, _slice, fields, attrs=[]):
    """Plots every simple (1 number saved/pass/module) fields.

    Args:
        fields: list of fields, like `["means", "stds"]`. Defaults to every simple fields
        _slice: custom slice across all graphs
    """
    if type(fields) == str: fields = [fields]
    logScale = "log" if "log" in attrs else "linear"
    def _plot(i, objF, title): # plots forward OR backward data of all modules of a particular field, assuming it's an array
        plt.subplot(len(fields), 2, i)
        for data in self: # display all modules
            obj = objF(data)
            plt.plot(range(len(obj))[_slice], obj[_slice], alpha=0.5)
        plt.title(title); plt.yscale(logScale)
    plt.figure(figsize=(10, 3*len(fields)), dpi=100)
    for i, field in enumerate(fields):
        _plot(i*2+1, lambda m: getattr(m.forward, field), f"Forward {field}")
        _plot(i*2+2, lambda m: getattr(m.backward, field), f"Backward {field}")
    plt.figlegend([data.name for data in self], loc='center right'); plt.show()
@k1lib.patch(HookModule)
def plot(self, *fields):
    if len(fields) == 0: fields = self.simpleFields
    return k1lib.viz.SliceablePlot(partial(plotF, self), alphaSlice=fields, docs="""
- p["means", "stds"]: to display plots of 2 variables
- p["means"].log: to display plot using log scale""")
@k1lib.patch(HookModule)
def withForwardHook(self, hook:callable, name=None):
    """Adds a hook to the forward pass. See `.withHook()` for more information"""
    hook.name = name; self.forwardFns += [hook]; return self
@k1lib.patch(HookModule)
def withBackwardHook(self, hook:callable, name=None):
    """Adds a hook to the backward pass. See `.withHook()` for more information"""
    hook.name = name; self.backwardFns += [hook]; return self
@k1lib.patch(HookModule)
def withHook(self, hook:callable, name=None):
    """Adds a hook to both the forward and backward pass.
    Params:
        `hook` function is expected to take in these parameters: (data, module, inp, out)
            data: the injected dependency for you to store stuff.
                Initially, `data` is an empty object, so you have to
                check whether it has your field like so:
                >>> if not hasattr(data, "min"): data.min = float("inf")
                >>> data.min = torch.min(data.min, out)

                If you do not do this, then undefined variables will
                automatically be an empty list, so that this is fine:
                >>> data.max.append() # okay

                Later on, you can do things like:
                >>> HookModule[i].forward.min
                and get the data you saved from the hook.
            module: the module this function hooks into. Please
                refer to `torch.nn.Module.register_forward_hook()` to
                know more.
            inp: input (or grad of input) to the module
            out: output (or grad of output) to the module
        `name`: custom name for the function for nice displaying
    """
    return self.withForwardHook(hook, name).withBackwardHook(hook, name)
@k1lib.patch(HookModule)
def clearHooks(self):
    self.forwardFns = []; self.backwardFns = []
    self.cleanFns = []; return self
def meanCb(data, m, inp, out): data.means.append(_getFirst(out).data.mean().item())
@k1lib.patch(HookModule)
def withMeanRecorder(self):
    self.simpleFields.append("means");
    return self.withHook(meanCb, "mean")
def stdCb(data, m, inp, out): data.stds.append(_getFirst(out).data.std().item())
@k1lib.patch(HookModule)
def withStdRecorder(self):
    self.simpleFields.append("stds");
    return self.withHook(stdCb, "std")
def minCb(data, m, inp, out): data.mins.append(_getFirst(out).data.min().item())
@k1lib.patch(HookModule)
def withMinRecorder(self):
    self.simpleFields.append("mins");
    return self.withHook(minCb, "min")
def maxCb(data, m, inp, out): data.maxs.append(_getFirst(out).data.max().item())
@k1lib.patch(HookModule)
def withMaxRecorder(self):
    self.simpleFields.append("maxs");
    return self.withHook(maxCb, "max")
@k1lib.patch(Callbacks, docs=HookModule)
def withHookModule(self, persistent=True):
    return self.append(HookModule(persistent).withMeanRecorder().withStdRecorder())