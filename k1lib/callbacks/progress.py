# AUTOGENERATED FILE! PLEASE DON'T EDIT HERE. EDIT THE SOURCE NOTEBOOKS INSTEAD
import k1lib, time; from k1lib import fmt
from .callbacks import Callback, Callbacks, Cbs
import k1lib.cli as cli; plt = k1lib.dep.plt
__all__ = ["ProgressBar"]
@k1lib.patch(Cbs)
class ProgressBar(Callback):                                                     # ProgressBar
    """Displays the current progress, epoch and batch while running.
Deposits variables into :class:`~k1lib.Learner` at checkpoint ``startBatch``:

- progress: single float from 0 to 1, guaranteed to increase monotonically
- epochThroughput
- remaining: estimated remaining time. Does not take into account callbacks that can potentially cancel the run prematurely""" # ProgressBar
    def startRun(self):                                                          # ProgressBar
        self.startTime = time.time(); self.step = 0; self.l.progress = 0         # ProgressBar
        self.l.loss = float("inf") # to make sure this variable exist            # ProgressBar
        self.aL = self.bL = self.cL = self.dL = self.eL = 0; self.data = []      # ProgressBar
    def startBatch(self):                                                        # ProgressBar
        batch = self.l.batch; batches = self.l.batches; epoch = self.l.epoch; epochs = self.l.epochs # ProgressBar
        elapsedTime = self.elapsedTime = time.time() - self.startTime            # ProgressBar
        if batches is None: progress = self.l.progress = epoch / epochs; batchTh = None # ProgressBar
        else:                                                                    # ProgressBar
            progress = self.l.progress = (batch / batches + epoch) / epochs      # ProgressBar
            batchTh = batches * epochs * progress / elapsedTime                  # ProgressBar
        epochTh = self.l.epochThroughput = epochs * progress / elapsedTime; self.l.batchThroughput = batchTh # ProgressBar
        remaining = self.l.remaining = round(elapsedTime / (progress+1e-7) * (1-progress), 2) if progress > 0 else float('inf') # ProgressBar
                                                                                 # ProgressBar
        a = str(round(100 * progress)); self.aL = max(self.aL, len(a)); a = a.rjust(self.aL) # ProgressBar
        b = f"{epoch}/{epochs} ({fmt.throughput(epochTh, ' epochs')})"; self.bL = max(self.bL, len(b)); b = b.rjust(self.bL) # ProgressBar
        if batches is not None:                                                  # ProgressBar
            c = f"{batch}/{batches} ({fmt.throughput(batchTh, ' batches')})"; self.cL = max(self.cL, len(c)); c = c.rjust(self.cL) # ProgressBar
        else: c = f"{batch}/{batches}"; self.cL = max(self.cL, len(c)); c = c.rjust(self.cL) # ProgressBar
        d = f"{round(elapsedTime, 2)}".rjust(6); self.dL = max(self.dL, len(d)); d = d.rjust(self.dL) # ProgressBar
        e = f"{remaining}"; self.eL = max(self.eL, len(e)); e = e.rjust(self.eL) # ProgressBar
        self.data.append([epoch, batch, elapsedTime, progress, epochTh, batchTh, remaining]) # ProgressBar
        print(f"\rProgress: {a}%, epoch: {b}, batch: {c}, elapsed: {d}s, remaining: {e}s, loss: {self.l.loss}             ", end="") # ProgressBar
    def plot(self, f=cli.iden(), perEpoch=False, _window=2):                     # ProgressBar
        """Plots detailed partial execution time profile.

:param f: optional post processing step
:param perEpoch: if True, normalize time per epoch, else keep it at time per run
:param _window: number of batches to calculate the processing rate over. Put low
    values (min 2) to make it crisp (and inaccurate), put high values to make it
    smooth (and accurate)"""                                                     # ProgressBar
        if perEpoch: f = cli.apply(cli.op()/self.l.epochs) | f                   # ProgressBar
        self.data | cli.cut(2, 3) | cli.deref() | cli.window(_window)\
        | cli.apply(cli.rows(0, -1) | cli.transpose() | ~cli.apply(lambda x, y: y-x) | ~cli.aS(lambda x, y: x/y))\
        | f | cli.deref() | cli.aS(plt.plot)                                     # ProgressBar
        plt.ylabel("Time/epoch (seconds)" if perEpoch else "Time/run (seconds)"); # ProgressBar
