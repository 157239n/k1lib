# AUTOGENERATED FILE! PLEASE DON'T EDIT
from k1lib.callbacks import Callback, Callbacks
import k1lib, torch
from typing import List
__all__ = ["ConfusionMatrix"]
@k1lib.patch(Callback.cls)
class ConfusionMatrix(Callback):
    " "
    def __init__(self, categories:List[str]=None):
        """Records what categories the network is confused the most. Expected
variable ``preds`` to be set in :class:`k1lib.Learner` before checkpoint ``endLoss``.
This is implemented in :class:`~k1lib.callbacks.lossFunctions.shorts.LossNLLCross`.

:param categories: list of category names"""
        super().__init__(); self.categories = categories
        self.n = len(categories or []) or 2
        self.matrix = torch.zeros(self.n, self.n)
    def _adapt(self, idxs):
        """Adapts the internal matrix so that it supports new categories"""
        m = idxs.max().item() + 1
        if m > self.n: # +1 because max index = len() - 1
            matrix = torch.zeros(m, m)
            matrix[:self.n, :self.n] = self.matrix
            self.matrix = matrix; self.n = len(self.matrix)
        return idxs
    def startEpoch(self): self.matrix = torch.zeros(self.n, self.n)
    def endLoss(self):
        yb = self._adapt(self.l.yb); preds = self._adapt(self.l.preds)
        self.matrix[yb, preds] += 1
    def endEpoch(self): self.matrix /= self.matrix.max(dim=1).values
    def plot(self):
        """Plots everything"""
        k1lib.viz.confusionMatrix(self.matrix, self.categories or range(self.n))
    def __repr__(self):
        return f"""{super()._reprHead}, use...
- l.plot(): to plot everything
{super()._reprCan}"""
@k1lib.patch(Callbacks, docs=ConfusionMatrix.__init__)
def withConfusionMatrix(self, categories:List[str]=None, name:str=None):
    return self.append(ConfusionMatrix(categories), name)