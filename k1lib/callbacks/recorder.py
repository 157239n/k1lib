# AUTOGENERATED FILE! PLEASE DON'T EDIT
import k1lib, torch; from k1lib.callbacks import Callback, Callbacks
from typing import Tuple, List
__all__ = ["Recorder"]
@k1lib.patch(Callback.cls)
class Recorder(Callback):
    """Records xb, yb and y from a short run. No training involved"""
    def __init__(self):
        super().__init__(); self.order = 20
        self.xbs = []; self.ybs = []; self.ys = []
    def startBatch(self):
        self.xbs += [self.xb.detach()]
        self.ybs += [self.yb.detach()]
    def endPass(self):
        self.ys += [self.y.detach()]
    @property
    def values(self): return self.xbs, self.ybs, self.ys
    def record(self, epochs:int=1, batches:int=None) -> Tuple[List[torch.Tensor], List[torch.Tensor], List[torch.Tensor]]:
        """Returns recorded xBatch, yBatch and answer y"""
        recorder = Recorder()
        with self.cbs.context(), self.cbs.suspendEvaluation():
            self.cbs.withDontTrain().withTimeLimit(5).append(recorder)
            self.run(epochs, batches)
        return recorder.values
    def __repr__(self):
        return f"""{self._reprHead}, can...
- r.record(epoch[, batches]): runs for a while, and records x and y batches, and the output
{self._reprCan}"""
@k1lib.patch(Callbacks, docs=Recorder)
def withRecorder(self): return self.append(Recorder())