# AUTOGENERATED FILE! PLEASE DON'T EDIT
import k1lib
class Callback:
    """Represents a callback. Define specific functions
    inside to intercept certain parts of the training
    loop. Can reference Learner's attrs directly
    using `self` like this:
    >>> self.opt # actually accessing Learner.opt, if `opt` is not defined
    
    You can also set Learner's attributes like this:
    >>> self.learner.xb = self.xb[None]
    This takes x batch of learner, unsqueeze it at
    the 0 position, then sets the x batch again.
    
    Normally, you will define a subclass of this and
    define specific intercept functions, but if you
    want to create a throwaway callback, then do this:
    >>> Callback().withCheckpoint("startRun", lambda: print("start running"))
    
    You can use `.cls` for a list of default Callback
    classes, for any particular needs"""
    def __init__(self, name=None):
        super(Callback, self).__init__()
        self.learner = None; self.cbs = None
        self.name = name or self.__class__.__name__
        self.order = 10 # can be modified by subclasses. A smaller order will be executed first
    def _injectCbs(self, cbs): self.cbs = cbs; return self
    def _injectLearner(self, learner): self.learner = learner; return self
    def __getattr__(self, attr):
        if attr == "learner": raise AttributeError(attr)
        if hasattr(self.learner, attr):
            return getattr(self.learner, attr)
        raise AttributeError(attr)
    def __getstate__(self):
        state = dict(self.__dict__)
        del state["learner"]; del state["cbs"]; return state
    def __setstate__(self, state): self.__dict__.update(state)
    def __repr__(self): return f"{self._reprHead}, can...\n{self._reprCan}"
    @property
    def _reprHead(self): return f"Callback `{self.name}`"
    @property
    def _reprCan(self): return """- cb.something: to get specific attribute "something" from learner if not available
- cb.withCheckpoint(checkpoint, f): to quickly insert an event handler
- cb.detach(): to remove itself from its parent Callbacks"""
    def withCheckpoint(self, checkpoint:str, f:callable): setattr(self, checkpoint, lambda: f(self)); return self
    def detach(self): self.cbs.remove(self.name); return self
Callback.cls = k1lib.Object()
class Callbacks:
    def __init__(self):
        self.learner = None; self.dict = {} # dict is the actual child storage
        self.suspendStack = []
    def injectLearner(self, learner):
        """Intended to be used by Learner only. Injects
        into all callbacks and update learner's dict."""
        self.learner = learner
        [cb._injectLearner(learner) for cb in self.cbs]; return self
    @property
    def cbs(self): return [*self.dict.values()] # convenience method for looping over stuff
    def _sort(self):
        self.dict = dict(sorted(self.dict.items(), key=lambda x: x[1].order))
        return self
    def append(self, cb, name=None):
        """Adds a callback to the collection."""
        cb._injectLearner(self.learner)._injectCbs(self)
        name = name or cb.name
        if name in self.dict:
            i = 0
            while (name := f"{name}{i}") in self.dict: i += 1
        cb.name = name; self.dict[name] = cb; self._sort(); return self
    def remove(self, name):
        """Removes a callback from the collection."""
        if name not in self.dict: return print(f"Callback `{name}` not found")
        del self.dict[name]; self._sort(); return self
    def _handleCbCall(self, cb, checkpoint, *args, **kwargs):
        if hasattr(cb, checkpoint): return getattr(cb, checkpoint)() != None
    def __call__(self, checkpoint):
        return any([self._handleCbCall(cb, checkpoint) for cb in self.cbs])
    def __getattr__(self, attr):
        if attr == "dict": raise AttributeError()
        if attr in self.dict: return self.dict[attr]
        else: raise AttributeError
    def __getstate__(self):
        state = dict(self.__dict__); del state["learner"]; return state
    def __setstate__(self, state):
        self.__dict__.update(state)
        for cb in self.cbs: cb._injectCbs(self)
    def __repr__(self):
        return "Callbacks:\n" + '\n'.join([f"- {cbName}" for cbName in self.dict]) + """\n
Use...
- cbs.append(cb[, name]): to add a callback with a name
- cbs("startRun"): to trigger a specific event
- cbs.Loss: to get a specific callback
- cbs.suspend(["Loss", "Cuda"]): to temporarily prevent triggering events in
    specific callbacks. Can be used multiple times before restoring
- cbs.restore(): to restore latest temporary suspension
"""
    @staticmethod
    def standard(advanced=True):
        """Standard callbacks. Include advanced callbacks
        if `advanced` is True. They can impact performance,
        so it's possible to switch them off."""
        cbs = Callbacks().withProgressBar().withLoss().withLossLandscape()
        if advanced: cbs.withHookModule().withHookParam()
        return cbs
@k1lib.patch(Callbacks)
def suspend(self, cbsClasses:list):
    stackFrame = []
    for cb in self.cbs:
        for cbsClass in cbsClasses:
            if cb.__class__.__name__ == cbsClass:
                stackFrame.append(cb); break
    for cb in stackFrame: # do this cause if not, self.cbs will be modified while looping over it
        self._handleCbCall(cb, "suspend")
        cb.detach()
    self.suspendStack.append(stackFrame)
@k1lib.patch(Callbacks)
def restore(self):
    stackFrame = self.suspendStack.pop()
    for cb in stackFrame:
        self.append(cb)
        self._handleCbCall(cb, "restore")
from k1lib._callbacks import shorts as _shorts
from k1lib._callbacks import loss_progress as _loss_progress
from k1lib._callbacks import hookParam as _hookParam
from k1lib._callbacks import hookModule as _hookModule
from k1lib._callbacks import paramFinder as _paramFinder
from k1lib._callbacks import lossLandscape as _lossLandscape