
Changelogs
==========

`1.8 </1.8>`_ - Jan 27th, 2025
-------------------------------

.. currentmodule:: k1lib.cli

Cli:

- Added :class:`~kjs.toPyFunc`, for compiling clis to really optimized python

Generic:

- Added :class:`~k1lib.Struct`, to define structs, serialize and deserialize
  them to bytes, on both Python and JS side

`1.7 </1.7>`_ - Jan 25th, 2025
-------------------------------

.. currentmodule:: k1lib.cli

Cli:

- Added :class:`~conv.toFileType`, :class:`~conv.toQr`, :class:`~conv.toExcel`, :class:`~conv.toMdTable`

:class:`~lsext.sql` modifications:

- Added lots of caching mechanisms: s["db"], db["table"] and table["id"]
- Allowed setting json columns using dict
- Added option to automatically html escape for text fields, to avoid cross site scripting

Generic:

- Added :meth:`~k1lib.aes_encrypt`, :meth:`~k1lib.aes_decrypt`, :meth:`~k1lib.cache`, :meth:`~k1lib.modbusCrc` and :meth:`~k1lib.parseTimeStr`
- Added :meth:`k1lib.viz.Clipboard`, :meth:`k1lib.viz.Download`, :meth:`k1lib.viz.Popup`, :meth:`k1lib.viz.qrScanner`, :meth:`k1lib.viz.daisyUI`
- Added :class:`~k1lib.AutoUpdateValue`, :class:`~k1lib.Aggregate`, :meth:`~k1lib.tempObj`, :class:`~k1lib.ConfinedAutoIncrement`, :class:`~k1lib.Perlin`
- Added delay mode to :meth:`~k1lib.cron`
- Added :meth:`~k1lib.preload` as an advanced version of :meth:`~k1lib.cache`
- Added :class:`~k1lib.TimeSeries`, :class:`~k1lib.speed` for random speed/throughput benchmarks
- Added :meth:`~k1lib.compileCExt`, to quickly build pybind11 Python C extensions and load it to the current process seemlessly

`1.6 </1.6>`_ - Mar 8th, 2024
-------------------------------

.. currentmodule:: k1lib.cli

Cli:

- Added :class:`~utils.toPdf`, :class:`~utils.lookupRange`, :class:`~utils.branch`
- Added optional delay to :class:`~output.intercept`
- Added :class:`~modifier.iterDelay`
- Added :class:`~conv.toDist`, :class:`~conv.toAngle`, :class:`~conv.idxsToNdArray`, :class:`~conv.toYaml`, :class:`~conv.toMedian`
- Added daemon mode to :class:`~inp.cmd`
- Added module :mod:`~k1lib.cli.kcv`, focusing on opencv aruco markers detection
- Added proper pandas support to most cli
- Added support for raw row ingestion to :class:`~conv.toCsv`
- Added powerful ``nparray | (~aS(lambda x,y: x+y)).all(3)`` array optimization strategy
- Added :meth:`lsext.sql.queryMany` and :meth:`lsext.sqltable.insertBulk`
- Added convenience methods to :class:`~lsext.s3` and friends. Also added :class:`lsext.Redis`
- Added JS transpiler functions to matplotlib colormaps

Generic:

- Added monkey patched methods :meth:`os.netstat` and :meth:`os.killPort`
- Added :meth:`~k1lib.fmt.dollar`
- Added several language formatters like :class:`~k1lib.fmt.js`, :class:`~k1lib.fmt.py`, :class:`~k1lib.fmt.html`, :class:`~k1lib.fmt.sql`
- Added :mod:`~k1lib.kcom` for external hardware communications, with :class:`~k1lib.kcom.Gsm` and
  :class:`~k1lib.kcom.Host`
- Added monkey-patched method :meth:`torch.transpose_axes` to match numpy's signature
- Added monkey-patched method :meth:`plt.worldmap` to quickly plot out a world map
- Added monkey-patched method :meth:`html.b64escape` to provide a more robust html escaping where JS is available
- Added monkey-patched method :meth:`pandas.DataFrame.newColName`
- Added module :mod:`~k1lib.kop` for optics simulation
- Added module :mod:`~k1lib.zircon` for browser automation

`1.5 </1.5>`_ - Jan 6th, 2024
-------------------------------

.. currentmodule:: k1lib.cli

Cli:

- Added s3 compatibility with ``ls()`` and ``cat()`` at :mod:`k1lib.cli.lsext`
- Added :class:`~conv.toUnix`, :class:`~conv.toLinks`, :class:`~conv.toArgmin`,
  :class:`~conv.toArgmax`, :class:`~conv.toMovingAvg`, :class:`~conv.toCm`
- Added :class:`~structural.batchedTrigger`, :class:`~structural.latch`, alias :class:`~structural.insId`
- Added :class:`~utils.zeroes`, :class:`~utils.normalize`
- Added :class:`~filt.trigger`, :class:`~filt.filtStd`
- Added :class:`~modifier.clamp`
- Added :class:`~output.unpretty`
- Added :class:`~kapi.post`
- Added :meth:`utils.deref.js` to transpile any data (not functions) into JS
- Removed :class:`structural.expandE`, because it's so niche
- Added JS transpiler functionality to generate JS code automatically from clis
- Added module :mod:`~k1lib.cli.kjs` in support for the JS transpiler
- Added module :mod:`~k1lib.cli.kgv` to quickly plot graphviz plots
- Added tail() optimization for :class:`~inp.catPickle`

Generic:

- Added websocket client and server support at :mod:`~k1lib.kws`
- Added logging integration with https://logs.mlexps.com using :meth`~k1lib.log`
- Added module :mod:`~k1lib.kast` for advanced abstract syntax tree manipulation
  in support for the JS transpiler
- Added :meth:`~k1lib.resolve` to resolve coroutines everywhere
- Added :meth:`serve.json`, :meth:`serve.date`, :meth:`serve.serialized`, :meth:`serve.apiKey` and souped up :mod:`~k1lib.serve` a little
- Added :mod:`~k1lib.serpent`, a lua serialization module
- Added formatting function :meth:`~k1lib.fmt.rmAnsi`

`1.4 </1.4>`_ - June 30th, 2023
-------------------------------

.. currentmodule:: k1lib.cli

Cli:

- Added ability for an existing cli to join with a function that's not a cli
  transparently. Meaning this is now possible: ``3 | (iden() | (lambda x: x**4))``
- Added :class:`~conv.toHash`, :class:`~conv.toStd`
- Accelerated :meth:`~modifier.applyCl.balanceFolder`
- Accelerated :class:`~structural.repeat`, :class:`~structural.repeatFrom`, :class:`~structural.joinStreams`
  and :class:`~structural.unique` for array types
- Added library-wide optimization that allows ``np.random.randn(3, 4, 5, 6) | item().all() | shape() == (3, 5, 6)``
  to operate on the array directly and not be broken up by ``.all()``
- Removed :class:`structural.accumulate` and :class:`structural.indexTable`, as it can be done using :class:`~structural.groupBy` and it's not used enough
- Added :class:`~utils.sketch`, :class:`~utils.syncStepper`
- Added alias :class:`~structural.T`
- Added Cython support and cpu limit settings option for :class:`~modifier.applyCl`
- Added full distribution mode to :class:`~filt.intersection`
- Added builtin ML models support: :class:`~models.embed`, :class:`~models.complete`,
  :class:`~models.kmeans`, :class:`~models.tsne` and :class:`~models.bloom`
  Model operations are also optimized to batch things together automatically
- Added new way to deal with infinite iterators generated by :class:`~structural.repeat` and friends
- Added multiple table pretty-format mode to :class:`~output.pretty`
- Removed :mod:`~k1lib.cli.kcsv`, because it's ridiculous to have a single short method in a big module
  and it's not intuitive. Replaced that with :class:`~conv.toCsv`
- Added :mod:`~k1lib.cli.ktree` for dealing with tree structures
- Added support for .zip files for :class:`~inp.kunzip`, :meth:`~inp.ls` and :meth:`~inp.cat`
- Added support for custom datatypes for :meth:`~inp.ls` and :meth:`~inp.cat`
- Added :mod:`k1lib.cli.lsext`, for ls's custom datatypes ("ls extensions"), particularly MySQL, PostgreSQL and SQLite
- Added robust Actor model for :class:`~modifier.applyCl`.
- Accelerated :class:`~filt.rows` and :class:`~filt.cut` for array types
- Added unsort mode to :class:`~modifier.sort`
- Added :class:`~modifier.roll`, :meth:`~k1lib.batchify`
- Added :mod:`k1lib.cli.kapi` to use ML apis published on mlexps.com
- Added :mod:`k1lib.selen` to extract main content of a webpage using Selenium

Generic:

- Added :meth:`~k1lib.cron`, :class:`k1lib.viz.PDF`

`1.3 </1.3>`_ - May 26th, 2023
------------------------------

.. currentmodule:: k1lib.cli

Cli:

- Revamped docs a lot
- Added :class:`~modifier.applyCl` to execute functions across an entire cluster
- Auto get representation if not string in :class:`~grep.grep`.
- Added aliases :class:`~modifier.map_`, :class:`~filt.filter_` and :class:`~structural.flatten`
- Added string execution ``3 | aS("x+2")`` capability to all clis
- Added :class:`~conv.toHtml` to quickly convert PIL image to html tag
- Accelerated :class:`~filt.filt` for array types even more
- Added :class:`~structural.ungroup`, and added more modes to :class:`~structural.groupBy`
- Fixed ``cut()[2:-2]`` edge case
- Added :class:`~utils.rItem` and :class:`~inp.urlPath` for quality of life
- Added demiliter-splitting mode to :class:`~conv.toDict`
- Added :meth:`nb.execute.rightAway`, :meth:`~conv.toAscii`, :class:`~utils.backup`,
  :class:`~inp.kzip` and :class:`~inp.kunzip`, :meth:`~filt.resume`
- Added :meth:`modifier.applyMp.shared` to easily share memory between processes
- Accelerated :meth:`~inp.cat` using :mod:`k1a` if sB and eB are specified
- Added multi-column mode to :class:`~modifier.apply`
- Removed :meth:`inp.curl` because you can do ``cat("http://example.com")`` directly
- Added array mode and ``retries`` parameter to :class:`~filt.tryout`
- Allowed building pipelines with normal classes that only define ``__ror__`` but not
  subclass :class:`~init.BaseCli`

Generic:

- Revamped :mod:`~k1lib.serve` a little, adding a more robust type system
- Added more default imports like ray and pyarrow
- Added :class:`~k1lib.viz.Scroll` and :class:`~k1lib.viz.Toggle`
- Added :meth:`~k1lib.viz.row`, :meth:`~k1lib.viz.col`, :meth:`~k1lib.viz.pre` and
  :meth:`~k1lib.viz.h` to quickly build html strings
- Added :meth:`~k1lib.capturePlt` to capture matplotlib plots
- Added formatting functions :meth:`~k1lib.fmt.fromSize` and :meth:`~k1lib.fmt.colors`
- Added pipe mode to :class:`~k1lib.viz.Carousel` and :class:`~k1lib.Wrapper`

`1.2 </1.2>`_ - Feb 7th, 2023
-----------------------------

.. currentmodule:: k1lib.cli

Cli:

- Added newPoolEvery mode to :class:`~modifier.applyMp`
- Added :class:`~inp.walk`, :class:`~filt.tryout`, :class:`~inp.splitSeek`,
  :meth:`inp.cat.pickle`.
- Added PIL image mode to :class:`~utils.size`
- Added chemical structure mode to :class:`~conv.toPIL`
- Added read speed profiler to :meth:`~inp.cat`
- Added table mode to :class:`~output.plotImgs`
- Added :meth:`filt.filt.split`, :meth:`filt.head.split`
- Removed :class:`output.split`, because it's horribly inefficient. Use
  :class:`~inp.splitSeek` instead.
- Added argument expand mode to :class:`~modifier.applyMp`.
- Added column mode to :class:`~filt.intersection` and added None column mode to :class:`~filt.union`
- Simplified :class:`~structural.insert`
- Accelerated :class:`~filt.filt`, :class:`~filt.cut`, :class:`~structural.joinStreams`
  and :class:`~modifier.randomize` for array types
- Added complex yielding functionality to :class:`~structural.repeatF`.
- Added automatic error checking for :class:`~filt.filt`.
- Added padding option to :class:`~structural.window`
- Added probability weighting mode to :class:`~structural.joinStreamsRandom`
- Fixed :mod:`forbiddenfruit` or-patching of :class:`~numpy.ndarray`, :class:`dict`,
  :class:`pandas.core.series.Series` and :class:`pandas.core.frame.DataFrame`

Generic:

- Added :class:`~k1lib.ConstantPad`, :class:`~k1lib.viz.ToggleImage`, :meth:`~k1lib.dep`
  and :meth:`~k1lib.ticks`.
- Added more features to :class:`~k1lib.viz.Carousel`
- Changed :meth:`~k1lib.captureStdout` so that it can capture C library's output and
  can capture stderr
- Added :mod:`~k1lib.p5` module for quick Processing-like image manipulation
- Developed :mod:`~k1lib.k1ui` module a lot further

`1.1 </1.1>`_ - Oct 3rd, 2022
-----------------------------

.. currentmodule:: k1lib.cli

Cli:

- Added dictionary mode, with table name to :meth:`~cif.tables`
- Added :meth:`~cif.records`, :class:`~conv.toGray`, :class:`~output.plotImgs`,
  :class:`~conv.toBytes`, :class:`~structural.indexTable`, :class:`~structural.splitC`
- k1a speedups: :class:`~inp.cat`
- Fixed strange bug in :class:`~modifier.applyMp` that happens between PyTorch and multiprocessing
- Added tensor/bytes/figure to image feature to :meth:`~conv.toPIL`
- Added image saving mode to :meth:`~output.file`
- Added separator mode to :class:`~structural.oneHot`
- Removed :class:`conv.toStr`, :class:`conv.toSet`, :class:`conv.toIter`,
  :class:`conv.toBin`, :class:`conv.toIdx`, :class:`conv.toDictF`, :class:`modifier.applySerial`
  because they're kinda meaningless and redundant.
- Added bytes mode chunking to :class:`~inp.cat`
- Removed module :mod:`k1lib.cli.others` as it's pretty useless

Generic:

- Added :meth:`~k1lib.pushNotification`, :meth:`fmt.throughput`
- Removed :meth:`~k1lib.clearLine`, :meth:`~k1lib.close`, :meth:`~k1lib.textToHtml`
  as they are quite niche
- Moved :meth:`k1lib.sameStorage` to :meth:`torch.sameStorage`
- Monkey patched :meth:`pandas.core.frame.DataFrame.table`, :class:`builtins.str.splitCamel`
- Added intersection operation to :class:`~k1lib.Domain`
- Removed library's PyTorch dependency, so that it can be lightweight enough to be used
  inside containers

.. currentmodule:: k1lib.selector

Deep learning:

- Added :meth:`ModuleSelector.intercept`
- Added estimated time remaining and throughput estimations to :class:`~k1lib.callbacks.progress.ProgressBar`
- Removed module :mod:`k1lib.kdata`, as that provides no value

`1.0 </1.0>`_ - Aug 9th, 2022
-----------------------------

.. currentmodule:: k1lib.cli

Cli:

- Removed :class:`conv.toNumpy`, as ``toList() | aS(np.array)`` does the same thing
- Added fill mode to :class:`~utils.lookup`
- Changed :class:`~output.tee` style to be more natural
- Removed :class:`utils.headerIdx`, as :meth:`~structural.insertIdColumn` roughly does the same thing
- Removed :class:`init.manyToMany`, replaced with :class:`~modifier.apply` to simplify things
- Removed unstable :class:`~modifier.op` ``in`` feature and added combined compare ops to it
- Added bounds comparison to :class:`~modifier.op`, thus removed :class:`filt.inRange`
- Added ``every`` mode to :class:`~output.tee`.
- Simplified :class:`~structural.insertColumn`
- Added :class:`~structural.oneHot`.
- Restructured expand argument feature in :class:`~modifier.applySerial`
- Added :mod:`~k1lib.cli.cif` module
- Removed :mod:`~k1lib.cli.entrez` module, as it doesn't add much value
- Simplified :class:`~output.file` by removing explicit text/byte mode param

LLVM:

- Added LLVM compiler/optimizer system to cli.
- Added :mod:`~k1lib.cli.typehint` and :mod:`~k1lib.cli.optimizations` modules
- Optimizations: :class:`~structural.unsqueeze`, :class:`~kxml.node`, :meth:`~inp.cat`, :class:`~filt.head`

Generic:

- Added library `k1a <https://github.com/157239n/k1a>`_ to speed up certain
  parts of the main library by compiling things down to C.
- Added `k1ui <https://github.com/157239n/k1ui>`_ support within k1lib. It's
  a Java program that can communicate over the network and provides apis to
  manipulate mouse/keyboard and screens.

.. currentmodule:: k1lib.callbacks

DL:

- Added callback :class:`limits.CancelOnOverfit`

`0.17 </0.17>`_ - Jul 15th, 2022
--------------------------------

.. currentmodule:: k1lib.cli

Cli:

- Accelerated :class:`~filt.head` for all sliceable types
- Add fractional mode to :class:`~filt.head`
- Added expanded arguments mode to :class:`~modifier.apply`
- Added column mode to :class:`~modifier.sortF`
- Added :meth:`gb.feats.root`, :meth:`gb.feats.tags`
- Removed :meth:`gb.feats.tag`, use :meth:`gb.feats.tags` instead
- Added predicate mode to :class:`~grep.grep`
- Added :class:`~utils.dictFields`
- Accelerated :class:`~structural.groupBy` significantly
- Removed :meth:`~structural.collate`, as there's no use for it
- Accelerated :class:`~utils.shape`, thus removing :class:`conv.lengths` and
  :class:`conv.toLens` as ``shape(0).all()`` is just as good

`0.16 </0.16>`_ - Jun 28th, 2022
--------------------------------

.. currentmodule:: k1lib.cli

Cli:

- Accelerated :class:`~filt.head` if input's a :class:`torch.Tensor` or :class:`np.ndarray`.
- Added :meth:`~utils.tree`, :class:`~utils.timeLimit`, :class:`~output.split`,
  :class:`~utils.lookup`.
- Renamed :class:`~structural.joinList` to :class:`~structural.insert`, cause that's more intuitive
- Removed :class:`structural.insertRow`, as ``insertRow(1, 2)`` can be achieved using ``~insert(1, 2)``
- Souped up :class:`~structural.insertColumn`
- Added column mode in :class:`~grep.grep`.
- Added JIT compilation for :class:`~modifier.op`
- Added alias :class:`~modifier.parallel` and :class:`~conv.toLens`
- Accelerated :class:`~structural.batched` if input's a :class:`range`
- Added accelerated mode to :meth:`~inp.cat`
- Grouped ``to__`` clis into the module :mod:`~k1lib.cli.conv`.
- Removed redundant :class:`~utils.toType` and :class:`~utils.identity`

`0.15 </0.15>`_ - Mar 22nd, 2022
--------------------------------

Generic:

- Added :class:`~k1lib.UValue`, :meth:`~k1lib.now`
- Patched :class:`numpy.ndarray`'s ``__or__`` method to work better with cli tools
- Added a few mathematical and physics constants in :mod:`k1lib.imports`
- Added :meth:`selector.ModuleSelector.cutOff`
- Renamed :meth:`k1lib.integrate` to :meth:`k1lib.integral`, to avoid conflict with existing cli
- Added :meth:`~k1lib.sameStorage`

.. currentmodule:: k1lib.cli

Cli:

- Moved :meth:`k1lib.tab` to :meth:`utils.tab`.
- Added keyword arguments to :class:`~modifier.applyS` and :meth:`~structural.repeatF`
- Added :class:`~structural.groupBy`, :class:`~utils.disassemble`, :class:`~utils.toProd`
- Added ``mode`` option to :class:`~modifier.toFloat` and :class:`~modifier.toInt`
- Accelerated :class:`~modifier.toFloat`, :class:`~modifier.toInt`,
  :class:`~structural.batched` and :class:`~utils.smooth` if it's a
  :class:`torch.Tensor` or :class:`np.ndarray`

`0.14 </0.14>`_ - May 1st, 2022
-------------------------------

.. currentmodule:: k1lib.callbacks

Generic:

- Added :class:`~shorts.OnProgress` callback

.. currentmodule:: k1lib.cli

Cli:

- Changed implementation of :class:`~filt.rows`. Should be much more stable and
  perdictable than the last version
- Fixed :class:`~structural.transpose` so that it works efficiently with numpy arrays
- Fixed :class:`~structural.splitW` so that it includes dangling elements at the end
- Revamped :mod:`k1lib.cli.kxml` heavily
- Added :meth:`structural.count.join`, to join multiple count results together
- Added aliases :class:`~utils.toImg`, :class:`~modifier.aS`
- Added :class:`~utils.toRgb` and :class:`~utils.toRgba`.
- Added :class:`~utils.clipboard` and its dependency requirement.
- Fixed bug in :class:`~structural.accumulate`.
- Removed :meth:`modifier.replace` and :meth:`modifier.remove`, as those can be done by
  :class:`~modifier.op` just fine.
- Added seed option in :class:`~modifier.randomize`
- Added :class:`~structural.window`.

`0.13 </0.13>`_ - Mar 23rd, 2022
--------------------------------

.. currentmodule:: k1lib.callbacks.callbacks

Generic:

- Added :meth:`~k1lib.pValue`.
- :meth:`~k1lib.captureStdout` now returns a :class:`~k1lib.Wrapper`
- Added :meth:`~k1lib.attrContext`, :class:`~k1lib.MovingAvg`
- Monkey patched :meth:`~matplotlib.pyplot.animate`
- Added mechanism to quickly insert a :class:`Callback` in :meth:`Callbacks.add`

.. currentmodule:: k1lib.cli

Cli:

- Added support for ``filt(4 in op())`` as extension for :meth:`filt.contains`.
- Added support for ``filt(op() in [1, 2, 3])`` as extension for :meth:`filt.inSet`
- Removed :meth:`filt.isFile`, as ``filt(os.path.isfile)`` does the same thing.
- Added JIT basics. Just a stub feature for now.
- Added :class:`~utils.toSorted`, :class:`~structural.reshape`, :class:`~modifier.integrate`,
  :class:`~output.tee`, :class:`~utils.rateLimit`.
- Added multidimensional option to :class:`~structural.joinStreams`.
- Added pipe input mode to :meth:`sam.cat`.
- Added control flow blocking option to :class:`inp.cmd`.
- Added ``unpack`` param to :class:`~modifier.applySerial`.
- Renamed :meth:`structural.splitList` to :meth:`~structural.splitW`
- Added :meth:`modifier.stagger.tv`
- Replaced :meth:`k1lib.smooth` with :meth:`utils.smooth` with a simpler impl

`0.12 </0.12>`_ - Dec 1st, 2021
-------------------------------

.. currentmodule:: k1lib.cli

Generic:

- Disallow adding new settings accidentally when using :meth:`~k1lib.Settings.context`.

Cli:

- Fixed :class:`~inp.cmd` piping mechanism into each other.
- Added ``quiet`` setting, used by :class:`~inp.cmd`.
- Made :class:`~filt.columns` more robust so that it can deal with missing elements
  and longer rows below.
- Added operator ``-`` to :class:`~filt.filt` for extra intuitiveness.6
- Added :class:`~utils.bindec`, :class:`~utils.toBin`, :class:`~utils.toIdx`,
  :class:`sam.flag`, :meth:`~bio.longFa` and :class:`~bio.idx`.
- Moved :class:`sam.quality` to :meth:`bio.quality`, and added ``cli.bio.phred``,
  ``cli.sam.header`` settings.
- Moved setting ``cli.oboFile`` to ``cli.bio.go``, and ``cli.lookupImgs`` to
  ``cli.bio.lookupImgs``.
- Added ``fill`` param to :class:`~utils.item`.
- Optimizes higher order operations quite a bit, and added setting ``cli.atomic``.
- Renamed :class:`init.manyToManySpecific` to :class:`init.mtmS`, and added method
  :meth:`~init.mtmS.f`.
- Added :meth:`~structural.transpose.fill` and :meth:`~structural.transpose.wrap` to
  :meth:`~structural.transpose`.
- Revamped how :class:`~inp.cmd` works, allowed real time output yielding, added
  bytes mode and option on how to return stdout and stderr.

`0.11 </0.11>`_ - Nov 24th, 2021
--------------------------------

.. currentmodule:: k1lib.callbacks

DL:

- Added :class:`~k1lib.Settings`, and the centralized :attr:`~k1lib.settings` for the
  entire library. As a consequence, moved :attr:`k1lib.cli.cliSettings` to
  :attr:`~k1lib.settings` under name "cli".
- Added :class:`~limits.TrainOnly`, :class:`~limits.ValidOnly`.
- Removed "pause" concept from :class:`~callbacks.Callback`.
- Patched :meth:`torch.Tensor.positionalEncode`, and removed procedural version
  (:meth:`k1lib.positionalEncode`).
- Added :class:`~k1lib.knn.MultiheadAttention`.

.. currentmodule:: k1lib.cli

Cli:

- Added multidimensional mode to :class:`~structural.transpose`.
- Changed param position of :class:`~utils.deref` so that it's more convenient.
- Moved :class:`inp.toPIL` to :class:`utils.toPIL`, to be more consistent.
- Added :mod:`~k1lib.cli.nb`. As a consequence, removed :meth:`~k1lib.nbCells` and
  :meth:`~k1lib.executeNb`.
- Added temporary file and append features to :meth:`~output.file`.
- Added immediate resolve option to :class:`~inp.cmd`.
- Added ``N`` option (max sections) and changed :meth:`~grep.grep.till` mechanics
  in :class:`~grep.grep`. Also added ``sep`` option and as a consequence, removed
  :class:`~grep.grepToTable`.
- Added home directory support for :class:`~output.file`, :meth:`~inp.cat` and
  :meth:`~inp.ls`.

`0.10 </0.10>`_ - Nov 17th, 2021
--------------------------------

.. currentmodule:: k1lib.callbacks

DL:

- Added :meth:`~k1lib.nbCells`, :meth:`~k1lib.timer`
- Changed :class:`~k1lib.Absorber` methods so that it won't use special words like
  ``int``, ``float``, ``len``, ``str`` and added :meth:`~k1lib.Absorber.ab_contains`
  and :meth:`~k1lib.Absorber.ab_fastF`.
- Revamped lots of Callbacks docs
- Renamed :class:`~k1lib.CaptureStdout` to :class:`~k1lib.captureStdout`, to match
  context manager's styles.

.. currentmodule:: k1lib.cli

Cli:

- Added ``utilization`` parameter to :class:`~modifier.applyMp`.
- Added :meth:`~init.fastF`
- Added tensor mode to :class:`~filt.mask`.
- Added ``filt`` and ``apply`` modes with columns to :class:`~trace.trace`.
- Made :class:`~utils.deref` so that it ignores dictionaries.
- Added some compatibility with numpy arrays across clis.
- Added ``cacheLimit`` parameter to :class:`~modifier.apply` and as a consequence,
  removed :class:`~modifier.applyCached`.
- Added :class:`~utils.toType` and :class:`~modifier.applyTh`.
- Added ``bs`` parameter to :class:`~modifier.applyMp` and as a consequence, removed
  :meth:`~modifier.applyMpBatched`.

`0.9 </0.9>`_ - Mov 14th, 2021
------------------------------

.. currentmodule:: k1lib.callbacks

DL:

- Added :meth:`~k1lib.scaleSvg`.
- Added ``prefix`` option to :class:`~k1lib.AutoIncrement`.

.. currentmodule:: k1lib.cli

Cli:

- Added ``kwargs`` argument to :meth:`modifier.applyMpBatched`.
- Added :class:`~k1lib.RunOnce`, :class:`~k1lib.MaxDepth`.
- Added alias :class:`~utils.iden`.
- Added :meth:`~trace.trace` mechanism, with accompanying tutorial.
- Remove :class:`~utils.shape`'s tensor special case
- Added :class:`~modifier.applySerial`.
- Added ``inf`` and ``context`` to :attr:`cliSettings`.
- Fixed bug where ``"abc" | deref()`` will actually split the string into characters.
- Terminates pool in :class:`~modifier.applyMp` if is keyboard interrupted, and in
  general made it much more robust.
- Stops :class:`~utils.deref` early if encountered :attr:`~structural.yieldSentinel`
- Optimizes :class:`~modifier.op` even further, thus removing :meth:`~filt.isValue`,
  as ``filt(op() == value)`` does the same thing.

`0.8 </0.8>`_ - Nov 7th, 2021
-----------------------------

.. currentmodule:: k1lib.callbacks

DL:

- Exposed :mod:`k1lib.viz` automatically, and improve :meth:`~k1lib.viz.mask` so
  that it smoothes out highlighted regions.
- Added :meth:`~k1lib.perlin3d`.
- Monkey patched :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.march`,
  :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.surface`, :meth:`~matplotlib.pyplot.k3d`,
  :meth:`~torch.loglinspace`, :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.point`,
  :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.line`, :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.plane`,
  :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.aspect`.
- Renamed :meth:`~callbacks.Callbacks.append` to :meth:`~callbacks.Callbacks.add`.
- Removed ``with-`` semantics for :meth:`~callbacks.Callback`. Use :attr:`~callbacks.Cbs` instead.
- Changed :meth:`~k1lib.selector.ModuleSelector.__contains__` so that it handles ``*``
  differently.

.. currentmodule:: k1lib.cli

Cli:

- Modified :class:`~utils.shape` so that it can detect multiple dimensions now, not
  just 2.
- Added :meth:`~structural.activeSamples.extend`, :meth:`~structural.activeSamples.fullness`.
- Added :class:`~modifier.applyCached`.
- Brought back :meth:`~structural.table`.
- Removed :meth:`~filt.startswith` and :meth:`~filt.endswith`, as ``filt(op().startswith())``
  does the same thing.

`0.7 </0.7>`_ - Nov 3rd, 2021
-----------------------------

.. currentmodule:: k1lib.callbacks

DL:

- Added ``metab`` as extra metadata from dataloaders to :class:`~k1lib.Learner` in
  the core training loop and modified :class:`~recorder.Recorder` to
  return it if available.
- Added ``n`` option to :class:`~k1lib.AutoIncrement`.
- Added :meth:`~k1lib.viz.mask`.
- Removed :meth:`k1lib.stats`, replaced it with :meth:`torch.Tensor.stats` directly
- Added :class:`~k1lib.cli.modifier.op` option to :class:`~k1lib.schedule.Fn`.
- Added :meth:`torch.Tensor.hasInfs`
- Made :class:`~lossFunctions.shorts.LossNLLCross` integrates with
  :class:`~lossFunctions.accuracy.AccF` instead.
- Made :class:`~lossFunctions.accuracy.AccF` integrates with :class:`~confusionMatrix.ConfusionMatrix`.
- Made :class:`~confusionMatrix.ConfusionMatrix` resilient against nans and infs,
  and fixed norm strategy (tensor rows divide by max rows, instead of tensor columns
  divide by max rows, like before).

.. currentmodule:: k1lib.cli

Cli:

- Added :class:`~filt.mask`, :meth:`~structural.unsqueeze`.
- Made :class:`~modifier.op` compatible with lots of other cli tools, so you can do
  stuff like ``filt(op() > 3, 1)``.
- Removed :class:`~structural.split`, as ``op().split().all() | joinStreams()`` does
  the same thing. This is longer, so I kinda want to put it back in, but the name
  is incredibly oxymoronic.
- Removed :meth:`~structural.listToTable` and its alias :meth:`~structural.tableFromList`,
  as they are too simple, and the new ``unsqueeze(1)`` does the same thing.
- Removed ``args`` option in :class:`~modifier.applyMp`, as it feels clunky.
- Removed :class:`~inp.cats` as ``cat().all()`` does the same job.
- Sped up :class:`~modifier.op` to have roughly same performance as
  :class:`~modifier.apply`. As a consequence, removed [:class:`~modifier.lstrip`,
  :class:`~modifier.rstrip`, :class:`~modifier.strip`, :class:`~modifier.upper`,
  :class:`~modifier.lower`] clis as stuff like ``op().upper().all()`` does the same
  and I want to simplify the collection of cli tools.
- Completely removed :mod:`k1lib.cli.ctx` module, as the performance sacrifices are
  too much, and it doesn't add a lot of useful features.
- Renamed :class:`utils.to1Str` to :class:`~utils.join` as that is more intuitive.
- Removed :class:`structural.table`, as ``op().split().all()`` does the same thing

`0.6 </0.6>`_ - Oct 30th, 2021
------------------------------

DL:

- Added :class:`~k1lib.knn.LinBlock`, :class:`~k1lib.Absorber`.
- Added __module__ impersonation for :class:`~k1lib.wrapMod`.
- Renamed :class:`~k1lib.callbacks.lossFunctions.shorts.LossLambda` to :class:`~k1lib.callbacks.lossFunctions.shorts.LossF`
- Renamed :meth:`torch.nn.Module.preserveDevice` to :meth:`torch.nn.Module.deviceContext`
  and add preserve buffers capability.
- Added :meth:`torch.nn.Module.gradContext`.

.. currentmodule:: k1lib.selector

:class:`k1lib.selector.ModuleSelector`:

- Renamed :meth:`filter` to :meth:`preprocess`.
- Added :meth:`~ModuleSelector.hookFp`, :meth:`~ModuleSelector.hookF`, and
  :meth:`~ModuleSelector.hookB`.
- Removed :meth:`~ModuleSelector.selected`, as :meth:`~ModuleSelector.__call__`
  does the same thing and is more intuitive
- Added ``prop`` option to :meth:`~ModuleSelector.named_children`
  and :meth:`~ModuleSelector.children`.
- Removed callback :class:`~k1lib.callbacks.frozen.Frozen` as
  :meth:`~ModuleSelector.freeze` and :meth:`~ModuleSelector.unfreeze` does the job
  and is much more robust.
- Added :meth:`~ModuleSelector.freeze` and :meth:`~ModuleSelector.unfreeze`
- Removed :meth:`~ModuleSelector.copy`, as you can just grab another selector
  straight from the model real quick.
- Removed :meth:`~ModuleSelector.parameters`, as you can always access the
  associated :class:`torch.nn.Module` inside and get params from there.

.. currentmodule:: k1lib.cli

Cli:

- Added ``raiseError`` option in :class:`~output.intercept`.
- Added multi argument capabilities to :meth:`~init.BaseCli.__call__`.
- Added :class:`~modifier.op`.
- Changed default param ``ignoreTensors`` of :class:`~utils.deref` to True.
- Ignores :class:`~torch.nn.Module` by default in :class:`~utils.deref`.

`0.5 </0.5>`_ - Oct 27th, 2021
------------------------------

.. currentmodule:: k1lib.callbacks

DL:

- Renamed :mod:`k1lib.format` to :mod:`k1lib.fmt`, and exposed it automatically.
- Renamed :mod:`~k1lib.fmt.computation` to :mod:`~k1lib.fmt.comp`,
  :mod:`~k1lib.fmt.computationRate` to :mod:`~k1lib.fmt.compRate`.
- Added :meth:`~k1lib.fmt.sizeOf`
- Exposed :mod:`~k1lib.selector` automatically.
- Deleted :mod:`k1lib.website`
- Fixed infinity elements in :class:`landscape.Landscape`'s plots.
- Split :class:`~loss_accuracy.Accuracy`'s accuracy calculating part into
  :class:`~lossFunctions.accuracy.AccF`.

.. currentmodule:: k1lib.cli

Cli:

- Added chained mode to :class:`~utils.item`
- Fixed ignoreTensor mechanic in :class:`~utils.deref`
- Added prefetch mode in :class:`~modifier.applyMp`
- Added :class:`~modifier.applyMpBatched` that executes lots of transformations in
  a single job.
- Added :meth:`~modifier.applyMp.clearPools` and :meth:`~modifier.applyMp.pools`.
- Added bytes reading and writing to :class:`~inp.cat` :class:`~output.file`.
- Added :class:`~structural.activeSamples`.
- Removed aliases :class:`~structural.splitColumns` and :class:`~structural.joinColumns`.
- Removed :class:`~structural.stitch`, as ``to1Str().all()`` does the same thing.

`0.4 </0.4>`_ - Oct 23rd, 2021
------------------------------

This update moves things around a lot. The actual coding experience stays the same,
but a lot of links \< 0.4 will be broken in 0.4 docs. Go to 0.3 docs if you wish to
follow links.

.. currentmodule:: k1lib.callbacks

Molecule (:mod:`k1lib.mo`):

- Added close coulomb force calculations to simulator to make it
  more realistic (cyclohexane chair config possible now!)
- Added optional Hydrogen viewing to various functions in :mod:`~k1lib.mo`
- Fixed parsing bug where it doesn't recognize "3-methyl" group in
  "3-methylpentane".

DL:

- Don't let :class:`~k1lib.AutoIncrement`'s ``value`` property to auto increment
  internal value.
- Removed :class:`~k1lib.kdata.CyclicRandomSampler`, as ``range(n) | repeatFrom() | randomize(n)```
  does the same thing.
- Removed :class:`~k1lib.kdata.FunctionDataset`, added simpler
  :class:`~k1lib.kdata.FunctionData` as replacement.
- Removed :class:`~k1lib.kdata.DataLoader`, :class:`~k1lib.kdata.Data` and
  :class:`~k1lib.kdata.DatasetWithSampler`, as they're complex and obsolete.
- Added :meth:`~k1lib.kdata.tfImg`, :meth:`~k1lib.kdata.tfFloat`,
  :meth:`~k1lib.kdata.analyzeFloat`
- Monkey-patched :class:`torch.nn.Module` to have piping capabilities.
- Renamed :mod:`k1lib.data` to :mod:`k1lib.kdata`, and exposed it automatically in
  :mod:`~k1lib.imports`.
- Renamed :mod:`k1lib.nn` to :mod:`k1lib.knn`, and exposed it automatically.

.. currentmodule:: k1lib.cli

Bioinfo cli:

- Renamed :mod:`k1lib.bioinfo.cli` to :mod:`k1lib.cli`
- Added :meth:`~modifier.stagger` as the new interface for dataloaders.
- Added :class:`~output.intercept`, :class:`~inp.toPIL`.
- Added PIL conversion mode to :class:`utils.toTensor`
- Added Tensor shape mode in :class:`utils.shape`.
- Added :mod:`~k1lib.cli.others` module, with :meth:`~others.crissCross`
- Added Tensor mode to :class:`~utils.toSum`, :class:`~utils.toAvg`,
  :class:`~utils.toMin`, :class:`~utils.toMax` and :class:`~init.oneToMany`.
- Added alias :class:`~utils.toMean`.
- Added dtype choice to :class:`~utils.toTensor`.

`0.3 </0.3>`_ - Oct 18th, 2021
------------------------------

Background stuff:

- Added mo tutorial

.. currentmodule:: k1lib.callbacks

DL:

- Added :meth:`~k1lib.viz.FAnim`
- Added :mod:`~k1lib.mo` for stuff related to molecular dynamics
- Added :meth:`~k1lib.graph`, :meth:`~k1lib.digraph`, :meth:`~k1lib.AutoIncrement.__call__`
- Huge revamp of :mod:`~k1lib.schedule` to make it more intuitive. There's only 1
  main schedule object now: :class:`~k1lib.schedule.Fn`.
- Added :meth:`k1lib.wraps`, :meth:`k1lib.Object.__delitem__`, :meth:`k1lib.Range.fromRange`
- Added :class:`k1lib.Every`

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Removed :class:`~filt.notIn`, as :class:`~filt.inSet` does the job just as well
- Included cli import command in :mod:`~k1lib.imports` by default
- Modified :meth:`~modifier.toFloat` and :meth:`modifier.toInt` so they can force
  weird values to 0.
- Moved existing :class:`~structural.toDict` to :class:`~structural.toDictF`, and
  created a new :class:`~structural.toDict`.

`0.2 </0.2>`_ - Sep 24th, 2021
------------------------------

Pretty minor update. I just want to push this out as soon as possible

Background stuff:

- Changed versioning system so that it makes more sense
- Added osic and mp tutorials
- Added more speed analysis in the cli tutorial

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Removed ``dirs`` and ``files`` parameters in :class:`~inp.ls`, as :class:`~filt.isFile` is good enough
- Disable module :mod:`~k1lib.bioinfo.cli.ctx` by default, to improve performance
- Replaced :class:`~filt.nonEmptyStream` to :class:`~filt.empty`

`0.1.13 </0.1.13>`_ - Sep 20th, 2021
------------------------------------

Background stuff:

- Removed walrus operator library-wide, so that it can be used with Python < 3.8

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Added :class:`~filt.breakIf`, :class:`~filt.isFile`
- Replaced :class:`~inp.infiniteF` with :class:`~structural.repeatF`
- Replaced :class:`~structural.infiniteFrom` with :class:`~structural.repeatFrom`
- Replaced :class:`~utils.dereference` with :class:`~utils.deref`
- Replaced :class:`ctx.dereference` with :class:`ctx.deref`
- Modified :class:`~modifier.applyMp` to use ``dill`` to deserialize everything
- Modified :class:`~utils.to1Str` so that it returns a string, instead of yielding
- Modified :class:`~utils.toStr` so that it can accept an optional column
- Modified :class:`~structural.splitList` so that it accepts \*args
- Removed :class:`~modifier.applySingle`, but retain :class:`~modifier.applyS`

.. currentmodule:: k1lib.callbacks

DL:

- Added class :class:`~k1lib.CaptureStdout`
- Patched :class:`torch.Tensor` with :meth:`~torch.Tensor.crissCross`,
  :meth:`~torch.Tensor.histBounds` and :meth:`~torch.Tensor.histScaled`

`0.1.12 </0.1.12>`_ - Sep 3rd, 2021
-----------------------------------

Background stuff:

- Removed docs's generated ``fonts`` folder, as it takes 8MB and isn't even used. Should now be sustainable for 100 versions on github pages.

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Removed wrapping ``__ror__`` operator if ``__init__`` is not defined, to make things performant.
- Added speed analysis in the `cli tutorial <tutorials.html>`_.
- Added :meth:`init.BaseCli.__call__`, :class:`~modifier.consume`, :meth:`ctx.ctx`, :class:`ctx.f`, :class:`~structural.peekF`, :class:`~structural.expandE`, :meth:`utils.dereference.__invert__`, :class:`~filt.unique`, :class:`~filt.notIn`, :class:`~modifier.sortF`, :class:`~utils.toMax`, :class:`~utils.toMin`, :class:`~filt.union`, :meth:`~inp.ls`, :meth:`~filt.instanceOf`, :class:`~modifier.randomize`
- Removed :class:`ctx.identity`
- Added shortcuts to :meth:`ctx.setC` and :meth:`ctx.getC`
- Made :meth:`~structural.headerIdx` context-aware
- Put :class:`ctx.Promise` dereferencing at :meth:`init.BaseCli.__ror__`, instead of dynamic patching at :mod:`k1lib.bioinfo.cli` construction time
- Get rid of :class:`~output.stdout` style inconsistencies. Previously, it looks like ``[1, 2] | stdout``, now it looks like ``[1, 2] | stdout()``.
- Added multiprocessing capabilities with :class:`~modifier.applyMp`
- Added ``maxDepth`` option for :class:`~utils.dereference`
- Added ``includeLast`` option to :class:`~structural.batched`
- Added ``float("inf")`` option to ``bs`` parameter of :class:`~structural.batched`
- Fixed :class:`~structural.permute` to be able to take in generator for rows.
- Fixed :class:`~output.stdout` to be able to display non-iterable inputs
- Fixed :class:`~utils.dereference` so that it will handle poking errors
- Fixed :class:`~structural.count` so that it can deal with list. Used to throw unhashable type: 'list'
- Added more flexibility with :meth:`~modifier.toFloat`, :meth:`~modifier.toInt` and :class:`~modifier.sort`

.. currentmodule:: k1lib.callbacks

DL:

- Added classes :class:`~k1lib.AutoIncrement`, :class:`~k1lib.Wrapper`
- Added functions :meth:`~k1lib.positionalEncode`, :meth:`~k1lib.debounce`
- Fixed :class:`~k1lib.executeNb`'s ``_globals`` doc-backref problem. Also clears plot automatically after executing a cell now.

`0.1.11 </0.1.11>`_ - Aug 25th, 2021
------------------------------------

Background stuff:

- Added testing section for unit tests (simple assert statements inside the notebooks)

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Added numpy/torch checks to :class:`~utils.dereference`
- Renamed :class:`~structural.sample` to :class:`~structural.peek`
- Added :class:`~structural.infiniteFrom`, :class:`~structural.joinStreamsRandom`,
  :class:`~structural.batched`, :class:`~structural.collate`, :class:`~structural.splitList`
- Added :class:`~inp.infiniteF`
- Added :class:`~utils.toTensor`
- Replaced :class:`~structural.infinite` in favor of :class:`~structural.repeat`
- Updated all cli tools to use ``super().__init__()``
- Added :mod:`~k1lib.bioinfo.cli.ctx` module, with :class:`~ctx.Promise`,
  :class:`~ctx.enum`, :class:`~ctx.identity` classes, and :meth:`~ctx.getC`,
  :meth:`~ctx.setC` methods

.. currentmodule:: k1lib.callbacks

DL:

- Added :class:`k1lib.data.CyclicRandomSampler` and :class:`k1lib.data.DatasetWithSampler`
- Added highlight feature in :meth:`callbacks.Callbacks.checkpointGraph`
- Added :meth:`k1lib.viz.Carousel.pop`, :meth:`k1lib.viz.Carousel.__getitem__`
- Added :meth:`k1lib.Learner.sample`
- Disallow :meth:`k1lib.executeNb` to execute lines that starts with "!", also
  removed parameter ``catchErrors``, as it's quite useless
- Added :meth:`k1lib.Object`

`0.1.10 </0.1.10>`_ - Aug 22nd, 2021
------------------------------------

Background stuff:

- Added notebook regression tests
- Added tutorials automated building tool
- Added :class:`k1lib.ignoreWarnings`
- Tutorials part moved to official docs (rather than .md files on github)
- Added `covid tutorial <tutorials.html>`_

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Reintroduced :class:`~structural.permute`, as :class:`~filt.rows` is inadequate
- Added :class:`~utils.lengths`, :class:`~modifier.applySingle`
- Exposed :class:`~init.serial`, :class:`~init.oneToMany`, :class:`~init.manyToMany`,
  and :class:`~init.manyToManySpecific`

.. currentmodule:: k1lib.callbacks

DL:

- Added :class:`confusionMatrix.ConfusionMatrix` and :meth:`k1lib.viz.confusionMatrix`
- Added :meth:`callbacks.Callbacks.checkpointGraph`
- Added :meth:`torch.nn.modules.Module.paramsContext`
- Modified :class:`k1lib.Object` to allow setting ``getdoc`` field
- Added :meth:`k1lib.viz.Carousel.saveBytes`, :meth:`k1lib.viz.Carousel.saveFile`,
  :meth:`k1lib.viz.Carousel.saveGraphviz`, and handle different image formats much
  better now

`0.1.9 </0.1.9>`_ - Aug 19th, 2021
----------------------------------

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Added :class:`k1lib.Domain` class
- Added ``__invert__`` option for :class:`~filt.rows` and :class:`~filt.columns` by
  incorporating :class:`k1lib.Domain`
- Sped up :class:`~filt.rows` significantly
- Removed cli tool :class:`~filt.every` as :class:`~filt.rows` is good enough
- Added ``__invert__`` option for :class:`~filt.head`. As a result, removed
  :class:`~filt.nhead`
- Added :meth:`~grep.grep.till` mechanism to :class:`~grep.grep` cli tool
- Added :mod:`~k1lib.bioinfo.cli.gb` cli module to deal with genbank file format
- Added :meth:`~structural.tableFromList` as alias of :meth:`~structural.listToTable`
- Renamed :class:`~utils.avg` to :class:`~utils.toAvg`
- Added :class:`~utils.toSum`

.. currentmodule:: k1lib.callbacks

DL:

- Added Callbacks tab completion to :class:`k1lib.Learner` and :class:`~callbacks.Callbacks`
- Refactored :class:`lossLandscape.LossLandscape` to :class:`landscape.Landscape`
  that can be used by any other callbacks, right now it's :class:`~loss_accuracy.Loss`
  and :class:`~loss_accuracy.Accuracy`
- Added :meth:`callbacks.Callback.pause` to help with :class:`~loss_accuracy.Accuracy`'s
  :class:`~landscape.Landscape`

`0.1.8 </0.1.8>`_ - Aug 15th, 2021
----------------------------------

- Fixed installation bug where readme.md would be absent, and setup.py won't work
  at all.

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Huge revamp of how tables are treated. Before, row elements are in a single string,
  separated by a delimiter. Now each row is a full fledged list
- Added :class:`~grep.grepToTable`, :class:`~structural.joinList`,
  :class:`~filt.contains`, :class:`~structural.table`, :class:`~structural.stitch`,
  :class:`~structural.listToTable`, :class:`~structural.insertColumn` cli tools
- Removed :class:`~structural.joinRows` but still keep :class:`~structural.joinStreams`
  as "joinRows" is not really obvious
- Removed :class:`~structural.permute` as :class:`~filt.columns` is pretty much identical
- Renamed :class:`~filt.inside` to :class:`~filt.inSet`
- Cut out nested functionality from :class:`~grep.grep` to :class:`~grep.grepToTable`

`0.1.7 </0.1.7>`_ - Aug 14th, 2021
----------------------------------

Interface with external modules:

- Swapped out ``register_backward_hook`` with :meth:`~torch.nn.Module.register_full_backward_hook`
  in :class:`~k1lib.callbacks.hookModule.HookModule` callback
- Added ``torch.nn.Module.preserveDevice()`` context manager

.. currentmodule:: k1lib.callbacks.callbacks

Callbacks:

- Changed :meth:`Callbacks.suspend` to take in names only
- Added :meth:`Callbacks.suspendClasses` to take in classes
- Changed :meth:`Callbacks.suspendEvaluation` to :meth:`Callbacks.suspendEval`, also
  added functionality for white and black lists
- Ripped out complex :meth:`Callback.__getattr__` mechanism (that automatically searches
  the parent learner for missing attributes) to improve speed
- Added :mod:`k1lib.callbacks.core` callbacks :class:`~k1lib.callbacks.core.CoreNormal`
  and :class:`~k1lib.callbacks.core.CoreRNN`
- Added more plot decorators for :class:`~k1lib.callbacks.profilers.memory.MemoryProfiler`,
  including backward-forward separator with their text
- Changed :class:`~k1lib.callbacks.lossLandscape.LossLandscape` callback so that it
  follows the common flow structure. Before, it implements a whole new ``cbs(...)``
  schema that essentially duplicated the loop inside of :class:`k1lib.Learner`

.. currentmodule:: k1lib

Learner:

- Implemented grace stop handling for :class:`Learner`. Before, if someone throws
  :exc:`CancelRunException` while executing a batch, then it will immediately jump
  to the end of the run. Changed it so that it will be caught in the batch loop,
  execute checkpoints ``cancelBatch`` and ``endBatch`` and rethrow it. Same thing
  with :exc:`CancelEpochException`
- Moved loss function from being a core functionality inside :class:`Learner`
  to an external callback, so that adapting multiple loss functions are possible
- Added :meth:`Learner.__call__`

.. currentmodule:: k1lib.bioinfo.cli

Bioinfo cli:

- Added :class:`~filt.isValue`, :class:`~filt.intersection`,
  :class:`~structural.AA_`, :class:`~structural.infinite`,
  :class:`~utils.dereference` cli tools
- Modified :class:`~inp.cat` to be able to take in file name by pipe
- Added new joining operator "+" between :class:`init.BaseCli`

.. currentmodule:: k1lib.callbacks.callbacks

Style changes:

- Changed :attr:`Callbacks.learner` to :attr:`Callbacks.l`
- Changed :attr:`Callback.learner` to :attr:`Callbacks.l`
- Removed :mod:`k1lib.eqn` from :mod:`k1lib.imports`'s namespace

0.1.6 - Aug 13th, 2021
----------------------

I don't really keep track of things 0.1.6 and before, so nothing here really.
