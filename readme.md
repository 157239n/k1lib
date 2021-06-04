# K1lib

This is my attempt at building a robust suite of toolchains in ML, so that everything sort of makes sense. Let's take a detailed look at how all of these works:

## basics

`Object` class helps code organization here and there. You can do `o = Object.fromDict({"a": 3})`, and `o.a` will be 3.
You can also do `a = Object().withAutoDeclare(lambda: [])`, so that even if you have not declared `a.field` before, when you access it, it will return a `[]`.

There are also several exceptions:
- `CancelRunException`: thrown whenever you want to end the run immediately
- `CancelEpochException`: thrown whenever you want to end the current epoch but still want to run
- `CancelBatchException`: thrown whenever you want to end the current batch, but still want to run the epoch

There are also little functions here and there:
- `test(predicate)`: throws error if value is false
- `close(a, b)`: tests if 2 values are close to each other. Can be number, list, array, tensor
- `getFirst(x)`: get first element, if it's a tuple or list, else return itself
---

## callbacks

A callback is pretty simple. While training, you may want to sort of insert functionality here and there. Let's say you want the program to print out a progress bar after each epoch. You can edit the learning loop directly, with some internal variables to keep track of the current epoch and batch, like this:

```python
startTime = time.time()
for epoch in epochs:
    for batch in batches:
        # do training
        data = getData()
        train(data)
        
        # calculate progress
        elapsedTime = time.time() - startTime
        progress = round((batch / batches + epoch) / epochs * 100)
        print(f"\rProgress: {progress}%, elapsed: {np.round(elapsedTime, 2)}s         ", end="")
```

But this means when you don't want that functionality anymore, you have to know what internal variable belongs to the progress bar, and you have to delete it. With callbacks, things work a little bit differently

```python
cbs = Callbacks()

def _progressFunction():
    progress = round((batch / batches + epoch) / epochs * 100)
    print(f"Progress: {progress}%, epoch: {epoch}/{epochs}, batch: {batch}/{batches}")
progressCallback = Callback.withCheckpoint("endBatch", _progressFunction)
cbs.append(progressCallback)

cbs("startRun")
for epoch in epochs:
    cbs("startEpoch")
    for batch in batches:
        cbs("startBatch")
        
        # do training
        data = getData()
        cbs("startTrain")
        output = model(data)
        cbs("startLoss")
        loss = lossF(output)
        cbs("startBackprop")
        backprop(model, loss)
        
        cbs("endBatch")
    cbs("endEpoch")
cbs("endRun")
```

You have your main training loop, which has a lot of 'checkpoints'. The checkpoints are controlled by a `Callbacks` object. Then before the training loop, you inject any functionality that you want, then that will be executed for you. You can also define it like this:

```python
class ProgressBar(Callback):
    def startRun(self):
        self.startTime = time.time()
    def startBatch(self):
        self.elapsedTime = time.time() - self.startTime
        progress = round((batch / batches + epoch) / epochs * 100)
        print(f"\rProgress: {progress}%, elapsed: {np.round(self.elapsedTime, 2)}s         ", end="")
```

As you can see, if you want to get rid of the progress bar, you have to delete the `startTime` line and the actual progress line. This requires you to remember what lines belongs to what functionality. If you use the callbacks mechanism instead, then you can just uncomment `cbs.append(ProgressBar())`, or `cbs.append(progressCallback)`, and that's it. This makes swapping out components extremely easy and repeatable.

Other use cases include intercepting at `startTrain`, and push all the training data to the GPU. You can also reshape the data however you want. You can insert different loss mechanisms (`startLoss`), or quickly inspect the model output. You can also change learning rates while training (`startEpoch`) according to some schedules. The possibility are literally endless.

### Dependency graph

How things depends on each other is interesting, and crucially important. In simple terms:

```
Learner -> Callbacks -> Callback
   |                      ^
   └----------------------┘
```

We will talk about `Learner` in detail later on, but in short, it's just a class that contains the main training loop. Let's look at an example:

```python
learner = Learner(...)
cbs = Callbacks()

class ProgressBar(Callback):
    # some functionality
progressBarCb = ProgressBar()
cbs.append(progressBarCb)
learner.withCbs(cbs)
```

When you add a `Callback` into a `Callbacks`, then `Callbacks` automatically injects itself into the `Callback`. This means when `cbs.append()` is called, `progressBarCb._cbs` will be set to `cbs`.

When you add a `Callbacks` into a `Learner`, then `Learner` automatically injects itself into `Callbacks` and all `Callback`s below that. This means `cbs.learner` and `progressBarCb.learner` will point to `learner`. This also means that you can change any variables within `learner` from within your `Callback`, for maximum flexibility.

### Actual docs

`Callback` class:
- `callback.withCheckpoint(checkpoint, function)`: For throwaway/quick callbacks that is extremely simple. `function` will be supplied with `self` argument
- `callback.detach()`: Detaches from its parent `Callbacks`

`Callbacks` class:
- `cbs.injectLearner(learner)`: Custom dependency injection
- `cbs.append(cb)`: Adds a callback
- `cbs.remove(name)`: Removes a callback with the specific name (if not specified, then usually class name)
- `cbs(checkpoint)`: Executed a checkpoint

Prebuilt callbacks:
- `cbs.withInspectLoss(function)`: When loss is calculated, calls `function(loss)`
- `cbs.withInspectBatch(function)`: When batch is loaded, calls `function(xb, yb)`
- `cbs.withModifyBatch(function)`: When batch is loaded, modify it using `xb, yb = function(xb, yb)`
- `cbs.withCuda()`: When batch is loaded, push them to the GPU
- `cbs.withInspectOutput(function)`: When output is calculated, calls `function(y)`
- `cbs.withModifyOutput(function)`: When output is calculated, modify it using `y = function(y)`
- `cbs.withProgressBar()`: Updates a progress bar at the start of each batch

Complex prebuilt callbacks:

#### Loss

Records losses. To activate: `cbs.withLoss()`
Uses:
- `learner.Loss.train`: list of all training losses over all epochs and batches (length = #epochs * #batches)
- `learner.Loss.valid`: list of all validation losses over all epochs and batches (length = #epochs * #batches)
- `learner.Loss.plot()`: plots the 2 above
- `Learner.Loss.epoch.train`: list of average training epoch losses (length = #epochs)
- `Learner.Loss.epoch.valid`: list of average validation epoch losses (length = #epochs)
- `Learner.Loss.epoch.plot`: plots the 2 above

#### HookModule

Record inputs and outputs of the modules. To activate: `cbs.withHookModule()`

This is a bit complicated, so let's see a few examples first. `learner.HookModule.withMeanRecorder()` will record the mean forward in/out and backward in/out of each module. This means that you can access it later, like:
- `learner.HookModule[0].forward.means`: returns a list of output means of the first module/layer
- `learner.HookModule[0].backward.means`: returns a list of output gradient means of the first module/layer

Actually implementing it by yourself is a bit complicated, so you should read over the source code to get a better feeling. For normal usage, feel free to display elements (like `learner.HookModule`, `learner.HookModule[0]`, ...) right on your cell, as they provide detailed guidance.

#### HookParam

Records parameters mean and std. To activate: `cbs.withHookModule()`

If your network has `Linear` and `Conv2d`, both of which has parameters, then this callback will record the average and std of each of those parameters at `startBatch`.

Uses:
- `learner.HookParam.plot()`: plots everything

#### ParamFinder

Finds the best parameter value for training. To activate: `cbs.withParamFinder("lr")`

Replace "lr" with any parameters you want figure out. When everything is setup properly, you can train it normally for a little bit (optional, but just to give the network some familiarity with the problem), then do `learner.ParamFinder.run()`.

This searches in the range of $10^{-6}$ to $10^2$

---

## learner

Actually this one is pretty simple. Think of it as just a container for the model, data, optimizer, and loss function. It handles basic stuff like the main training loop, and it also manages the callback mechanism:
- `learner.configure(model, data, opt, lossFunction)`: Configures the learner. All of these has to be configured before running. You can configure them at initialization (`Learner(...)`), or at run time (`learner.run(3, ...)`)
- `learner.run(epochs, ...)`: Runs for a number of epochs

All checkpoints available:
- `startRun`, `endRun`, `cancelRun`: Before, after run, and when run is cancelled
- `startEpoch`, `endEpoch`, `cancelEpoch`: Before, after epoch, and when epoch is cancelled
- `startValidBatches`: Each epoch has 2 phases, 1 train and 1 validation. This sits between them
- `startBatch`, `endBatch`, `cancelBatch`: before, after batch, and when batch is cancelled
- `endPass`: After passed data to the model
- `endLoss`: After loss is calculated
- `startBackward`: Before backprop. Return anything (not `None`) to not execute this
- `startStep`: Before step. Return anything (not `None`) to not execute this
- `startZeroGrad`: Before zero gradients. Return anything (not `None`) to not execute this
- `suspend`: Before detaching callback for temporary suspension
- `restore`: After being reattached to `Callbacks` after temporary suspension

There's also a quick and dirty `nn.Module` called `Lambda`. This basically transforms a regular function into a module.

---

## schedule

A schedule is just a function mapping from $[0, 1]$ to a real value. When used together with the `ParamScheduler` callback, it will change the network parameter to that specific real value. Using `ParamScheduler` is quite easy though:
- `ParamScheduler("lr", <schedule>)`: just a typical constructor. Then you can add this `Callback` to the learner

Everything else are tools to create schedules easily.
