# AUTOGENERATED FILE! PLEASE DON'T EDIT
from k1lib.callbacks import Callback, Callbacks
import k1lib, os, torch
__all__ = ["Autosave", "DontTrainValid", "InspectLoss", "ModifyLoss", "Cpu", "Cuda",
           "DType", "InspectBatch", "ModifyBatch", "InspectOutput", "ModifyOutput", 
           "Beep"]
@k1lib.patch(Callback.cls)
class Autosave(Callback):
    """Autosaves 3 versions of the network to disk"""
    def __init__(self): super().__init__(); self.order = 23
    def endRun(self):
        os.system("mv autosave-1.pth autosave-0.pth")
        os.system("mv autosave-2.pth autosave-1.pth")
        self.learner.save("autosave-2.pth")
@k1lib.patch(Callbacks, docs=Autosave)
def withAutosave(self): return self.append(Autosave())
@k1lib.patch(Callback.cls)
class DontTrainValid(Callback):
    """If is not training, then don't run m.backward() and opt.step().
The core training loop in k1lib.Learner don't specifically do this,
cause there may be some weird cases where you want to also train valid."""
    def _common(self):
        if not self.model.training: return True
    def startBackward(self): return self._common()
    def startStep(self): return self._common()
@k1lib.patch(Callbacks, docs=DontTrainValid)
def withDontTrainValid(self): return self.append(DontTrainValid())
@k1lib.patch(Callback.cls)
class InspectLoss(Callback):
    """Expected `f` to take in 1 float."""
    def __init__(self, f): super().__init__(); self.f = f; self.order = 15
    def endLoss(self): self.f(self.loss.detach())
@k1lib.patch(Callbacks, docs=InspectLoss)
def withInspectLoss(self, f): return self.append(InspectLoss(f))
@k1lib.patch(Callback.cls)
class ModifyLoss(Callback):
    """Expected `f` to take in 1 float and return 1 float."""
    def __init__(self, f): super().__init__(); self.f = f; self.order = 13
    def endLoss(self): self.learner.loss = self.f(self.loss)
@k1lib.patch(Callbacks, docs=ModifyLoss)
def withModifyLoss(self, f): return self.append(ModifyLoss(f))
@k1lib.patch(Callback.cls)
class Cuda(Callback):
    """Moves batch and model to the default GPU"""
    def startRun(self): self.model.cuda()
    def startBatch(self):
        self.learner.xb = self.learner.xb.cuda()
        self.learner.yb = self.learner.yb.cuda()
@k1lib.patch(Callbacks, docs=Cuda)
def withCuda(self, name:str=None): return self.append(Cuda(), name)
@k1lib.patch(Callback.cls)
class Cpu(Callback):
    """Moves batch and model to CPU"""
    def startRun(self): self.model.cpu()
    def startBatch(self):
        self.learner.xb = self.learner.xb.cpu()
        self.learner.yb = self.learner.yb.cpu()
@k1lib.patch(Callbacks, docs=Cpu)
def withCpu(self, name:str=None): return self.append(Cpu(), name)
@k1lib.patch(Callback.cls)
class DType(Callback):
    """Moves batch and model to a specified data type"""
    def __init__(self, dtype): super().__init__(); self.dtype = dtype
    def startRun(self): self.model = self.model.to(self.dtype)
    def startBatch(self):
        self.learner.xb = self.learner.xb.to(self.dtype)
        self.learner.yb = self.learner.yb.to(self.dtype)
@k1lib.patch(Callbacks, docs=DType)
def withDType(self, dtype:torch.dtype): return self.append(DType(dtype))
@k1lib.patch(Callback.cls)
class InspectBatch(Callback):
    """Expected `f` to take in 2 tensors."""
    def __init__(self, f:callable): super().__init__(); self.f = f; self.order = 15
    def startBatch(self): self.f(self.xb, self.yb)
@k1lib.patch(Callbacks, docs=InspectBatch)
def withInspectBatch(self, f): return self.append(InspectBatch(f))
@k1lib.patch(Callback.cls)
class ModifyBatch(Callback):
    """Modifies xb and yb on the fly. Expected `f`
    to take in 2 tensors and return 2 tensors."""
    def __init__(self, f): super().__init__(); self.f = f; self.order = 13
    def startBatch(self): self.learner.xb, self.learner.yb = self.f(self.xb, self.yb)
@k1lib.patch(Callbacks, docs=ModifyBatch)
def withModifyBatch(self, f): return self.append(ModifyBatch(f))
@k1lib.patch(Callback.cls)
class InspectOutput(Callback):
    """Expected `f` to take in 1 tensor."""
    def __init__(self, f): super().__init__(); self.f = f; self.order = 15
    def endPass(self): self.f(self.y)
@k1lib.patch(Callbacks, docs=InspectOutput)
def withInspectOutput(self, f): return self.append(InspectOutput(f))
@k1lib.patch(Callback.cls)
class ModifyOutput(Callback):
    """Modifies output on the fly. Expected `f` to take
in 1 tensor and return 1 tensor"""
    def __init__(self, f): super().__init__(); self.f = f; self.order = 13
    def endPass(self): self.learner.y = self.f(self.y)
@k1lib.patch(Callbacks, docs=ModifyOutput)
def withModifyOutput(self, f): return self.append(ModifyOutput(f))
@k1lib.patch(Callback.cls)
class Beep(Callback):
    """Plays a beep sound when the run is over"""
    def endRun(self): k1lib.beep()
@k1lib.patch(Callbacks, docs=Beep)
def withBeep(self, name:str=None): return self.append(Beep(), name)