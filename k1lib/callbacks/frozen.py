# AUTOGENERATED FILE! PLEASE DON'T EDIT
import k1lib
from k1lib.callbacks import Callback, Callbacks
__all__ = ["Frozen"]
@k1lib.patch(Callback.cls)
class Frozen(Callback):
    """Freezes selected parts of the network"""
    def __init__(self, css:str):
        self.css = str
    def startRun(self):
        self.selector = self.learner.selector.copy()
        self.selector.clearProps()
        self.selector.parse(k1lib.selector.filter(css, "_frozen_"))
        self.params = []; self.oldParamValues = []
        for m in self.selector.modules("_frozen_"):
            self.params.extend(m.parameters())
        for p in self.params:
            self.oldParamValues.append(p.requires_grad)
            p.requires_grad = False
    def endRun(self):
        for p, v in zip(self.params, self.oldParamValues):
            p.requires_grad = v
        self.params = []
    def __repr__(self):
        return f"""{self._reprHead}, can...
- f.selector: to get internal k1lib.ModuleSelector object
{self._reprCan}"""
@k1lib.patch(Callbacks, docs=Frozen)
def withFrozen(self, css:str): return self.append(Frozen(css))