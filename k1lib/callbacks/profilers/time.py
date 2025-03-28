# AUTOGENERATED FILE! PLEASE DON'T EDIT HERE. EDIT THE SOURCE NOTEBOOKS INSTEAD
import k1lib, time, torch; from k1lib import fmt, cli
from k1lib.callbacks import Callback, Cbs
_ltime = 15; _lt1 = 8; _lt2 = 18
class TimeData:                                                                  # TimeData
    def __init__(self, tProfiler, mS:k1lib.selector.ModuleSelector):             # TimeData
        self.tProfiler = tProfiler; self.mS = mS                                 # TimeData
        self.startTime = None; self.time = 0; self.hook()                        # TimeData
    def hook(self):                                                              # TimeData
        def fpHk(m, i):                                                          # TimeData
            if self.tProfiler.is_cuda: torch.cuda.synchronize()                  # TimeData
            self.startTime = time.time()                                         # TimeData
        def fHk(m, i, o):                                                        # TimeData
            if self.tProfiler.is_cuda: torch.cuda.synchronize()                  # TimeData
            self.time += time.time() - self.startTime                            # TimeData
        self.fpH = self.mS.nn.register_forward_pre_hook(fpHk)                    # TimeData
        self.fH = self.mS.nn.register_forward_hook(fHk)                          # TimeData
    def unhook(self):                                                            # TimeData
        self.tProfiler.totalTime = max(self.tProfiler.totalTime, self.time)      # TimeData
        self.fpH.remove(); self.fH.remove()                                      # TimeData
    def __getstate__(self):                                                      # TimeData
        answer = dict(self.__dict__)                                             # TimeData
        del answer["mS"]; del answer["tProfiler"]; return answer                 # TimeData
    def __setstate__(self, state): self.__dict__.update(dict(state))             # TimeData
    def __str__(self):                                                           # TimeData
        if self.time <= 1e-20: return ""                                         # TimeData
        a = f"{fmt.time(self.time)}".ljust(_ltime)                               # TimeData
        b = f"{round(100 * self.time / self.tProfiler.totalTime)}%".rjust(_lt1)  # TimeData
        c = f"{round(100 * self.time / self.tProfiler.selectedMaxTime)}%".rjust(_lt2) if self.tProfiler.selectedMaxTime != None and "_timeProf_" in self.mS else "" # TimeData
        return f"{a}{b}{c}"                                                      # TimeData
class TimeProfiler(Callback):                                                    # TimeProfiler
    """Profiles execution time. Only measures forward times, as
backward times can't really be measured. Example::

    l = k1lib.Learner.sample()
    l.cbs.add(Cbs.Profiler())
    # views table
    l.Profiler.time
    # views table highlighted
    l.Profiler.time.css("#lin1")"""                                              # TimeProfiler
    def startRun(self):                                                          # TimeProfiler
        if not hasattr(self, "selector"): # if no selectors found                # TimeProfiler
            self.selector = self.l.model.select("")                              # TimeProfiler
        for m in self.selector.modules(): m.data = TimeData(self, m)             # TimeProfiler
        self.selector.displayF = lambda m: (fmt.txt.red if "_timeProf_" in m else fmt.txt.identity)(m.data) # TimeProfiler
        self.totalTime = 0; self.selectedMaxTime = None                          # TimeProfiler
    def startStep(self): return True                                             # TimeProfiler
    def _run(self):                                                              # TimeProfiler
        """Runs everything"""                                                    # TimeProfiler
        with self.cbs.context(), self.cbs.suspendEval():                         # TimeProfiler
            self.is_cuda = next(self.l.model.parameters()).is_cuda               # TimeProfiler
            if self.is_cuda: self.cbs.add(Cbs.Cuda())                            # TimeProfiler
            else: self.cbs.add(Cbs.Cpu())                                        # TimeProfiler
            self.l.run(1, 1)                                                     # TimeProfiler
        for m in self.selector.modules(): m.data.unhook()                        # TimeProfiler
    def css(self, css:str):                                                      # TimeProfiler
        """Selects a small part of the network to highlight. See also: :mod:`k1lib.selector`.""" # TimeProfiler
        self.selector.parse(k1lib.selector.preprocess(css, "_timeProf_"))        # TimeProfiler
        self.selectedMaxTime = 0                                                 # TimeProfiler
        for m in self.selector.modules():                                        # TimeProfiler
            if "_timeProf_" in m:                                                # TimeProfiler
                self.selectedMaxTime = max(self.selectedMaxTime, m.data.time)    # TimeProfiler
        print(self.__repr__())                                                   # TimeProfiler
        self.selector.clearProps(); self.selectedMaxTime = None                  # TimeProfiler
    def __repr__(self):                                                          # TimeProfiler
        header = "time".ljust(_ltime) + "% total".rjust(_lt1) + ("% selected max" if self.selectedMaxTime != None else "").rjust(_lt2) # TimeProfiler
        footer = ""                                                              # TimeProfiler
        if self.selectedMaxTime != None:                                         # TimeProfiler
            b = f"{round(100 * self.selectedMaxTime / self.totalTime)}%".rjust(_lt1, " ") # TimeProfiler
            st = f"{fmt.time(self.selectedMaxTime)}".rjust(_lt2)                 # TimeProfiler
            footer = ("Selected max", " " * _ltime + b + st)                     # TimeProfiler
        c = self.selector.__repr__(intro=False, header=header, footer=footer).split("\n") | cli.tab() | cli.join("\n") # TimeProfiler
        return f"""TimeProfiler ({"GPU" if self.is_cuda else "CPU"}):\n{c}

Caveats: This one's a bit stranger than memory and computation profilers
1. There is no "total" time (adding all times in all modules). There
    is total network execution time tho, which is just the time taken
    for the top level module to execute
2. "% selected max" column displays percentage of selected max, not
    percentage of total selected time, which may matter in your analysis

Can...
- tp.css("..."): highlights a particular part of the network
- tp.selector: to get internal k1lib.ModuleSelector object"""                    # TimeProfiler
