# AUTOGENERATED FILE! PLEASE DON'T EDIT
from k1lib.callbacks import Callback, Callbacks
import k1lib, torch, numpy as np
import matplotlib.pyplot as plt
__all__ = ["LossLandscape"]
@k1lib.patch(Callback.cls)
class LossLandscape(Callback):
    """Plots the loss landscape of the network. Display
    this in your cell for more."""
    def __init__(self): super().__init__()
    def _calc(self, i, ax, _range, vector1, vector2):
        res = 50; _range = k1lib.Range(_range); model = self.learner.model
        x, y = torch.meshgrid(torch.linspace(*_range, res), torch.linspace(*_range, res))
        z = np.empty((res, res))
        with torch.no_grad():
            originalParams = model.exportParams()
            for ix, _ in enumerate(x):
                for iy, _ in enumerate(y):
                    for param, og, v1, v2 in zip(model.parameters(), originalParams, vector1, vector2):
                        param.data = og + x[ix, iy] * v1 + y[ix, iy] * v2
                    self.cbs("startPass")
                    self.learner.y = self.learner.model(self.xb)
                    self.cbs("endPass")
                    self.cbs("startLoss"); self.learner.loss = self.lossF(self.y, self.yb).detach().item(); self.cbs("endLoss")
                    z[ix, iy] = self.loss if self.loss == self.loss else 0 # check for nan
                    print(f"\rProgress: {round(100*(ix+iy/res)/res)}%     ", end="")
            model.importParams(originalParams)
        ax.plot_surface(x, y, z, cmap=plt.cm.coolwarm)
        print(f"     {i+1}/8 Finished {_range} range       ", end="")
    def plot(self):
        print() # nice new line
        with self.cbs.suspend(cbsClasses=["HookModule", "HookParam", "ProgressBar", "ParamScheduler", "Loss", "Autosave"]):
            self.cbs("startRun"); self.cbs("startEpoch")
            self.learner.xb, self.learner.yb = next(iter(self.learner.data.valid))
            self.cbs("startBatch"); k1lib.clearLine()
            model = self.learner.model
            def getVectors(): return model.getParamsVector(), model.getParamsVector()
            fig, axes = plt.subplots(2, 4, subplot_kw={"projection": "3d"}, figsize=(16, 8), dpi=120)
            ranges = [.0562, .1, .177, .316, .562, 1, 1.77, 3.16]
            vectors = getVectors()
            for i, (ax, _range) in enumerate(zip(axes.flatten(), ranges)):
                self._calc(i, ax, [-_range, _range], *vectors)
            self.cbs("endBatch"); self.cbs("endEpoch"); self.cbs("endRun")
            plt.show()
    def __repr__(self):
        return f"""{self._reprHead}, use...
- ll.plot(): to plot everything
{self._reprCan}"""
@k1lib.patch(Callbacks, docs=LossLandscape)
def withLossLandscape(self): return self.append(LossLandscape())