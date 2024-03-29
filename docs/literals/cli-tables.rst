+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| conv                         | structural                               | utils                         | filt                          | modifier                         |
+==============================+==========================================+===============================+===============================+==================================+
| :class:`~conv.toTensor`      | :class:`~structural.transpose`           | :class:`~utils.size`          | :class:`~filt.filt`           | :class:`~modifier.applyS`        |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toRange`       | :class:`~structural.T`                   | :class:`~utils.shape`         | :class:`~filt.filter_`        | :class:`~modifier.aS`            |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toList`        | :class:`~structural.reshape`             | :class:`~utils.item`          | :class:`~filt.inSet`          | :class:`~modifier.apply`         |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toSum`         | :class:`~structural.insert`              | :class:`~utils.rItem`         | :class:`~filt.contains`       | :class:`~modifier.map_`          |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toProd`        | :class:`~structural.splitW`              | :class:`~utils.iden`          | :class:`~filt.empty`          | :class:`~modifier.applyMp`       |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toAvg`         | :class:`~structural.splitC`              | :class:`~utils.join`          | :meth:`~filt.isNumeric`       | :class:`~modifier.parallel`      |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toMean`        | :class:`~structural.joinStreams`         | :class:`~utils.wrapList`      | :meth:`~filt.instanceOf`      | :class:`~modifier.applyCl`       |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toStd`         | :class:`~structural.joinSt`              | :class:`~utils.equals`        | :class:`~filt.head`           | :class:`~modifier.applyTh`       |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toMax`         | :class:`~structural.joinStreamsRandom`   | :class:`~utils.reverse`       | :class:`~filt.tail`           | :class:`~modifier.applySerial`   |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toMin`         | :class:`~structural.activeSamples`       | :class:`~utils.ignore`        | :class:`~filt.cut`            | :class:`~modifier.sort`          |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toArgmin`      | :meth:`~structural.table`                | :class:`~utils.rateLimit`     | :class:`~filt.rows`           | :class:`~modifier.sortF`         |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toArgmax`      | :class:`~structural.batched`             | :class:`~utils.timeLimit`     | :class:`~filt.intersection`   | :class:`~modifier.consume`       |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toPIL`         | :class:`~structural.batchedTrigger`      | :meth:`~utils.tab`            | :class:`~filt.union`          | :class:`~modifier.randomize`     |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toImg`         | :class:`~structural.window`              | :meth:`~utils.indent`         | :class:`~filt.unique`         | :class:`~modifier.stagger`       |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toRgb`         | :class:`~structural.groupBy`             | :class:`~utils.clipboard`     | :class:`~filt.breakIf`        | :class:`~modifier.op`            |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toRgba`        | :class:`~structural.ungroup`             | :class:`~utils.deref`         | :class:`~filt.mask`           | :class:`~modifier.integrate`     |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toGray`        | :class:`~structural.insertColumn`        | :class:`~utils.bindec`        | :class:`~filt.tryout`         | :class:`~modifier.roll`          |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toDict`        | :class:`~structural.insertIdColumn`      | :class:`~utils.smooth`        | :meth:`~filt.resume`          | :class:`~modifier.clamp`         |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toFloat`       | :class:`~structural.insId`               | :meth:`~utils.disassemble`    | :class:`~filt.trigger`        |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toInt`         | :meth:`~structural.unsqueeze`            | :meth:`~utils.tree`           | :class:`~filt.filtStd`        |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toBytes`       | :class:`~structural.count`               | :class:`~utils.lookup`        |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toDataUri`     | :class:`~structural.hist`                | :class:`~utils.dictFields`    |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toAnchor`      | :class:`~structural.permute`             | :class:`~utils.backup`        |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toHtml`        | :class:`~structural.AA_`                 | :class:`~utils.sketch`        |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :meth:`~conv.toAscii`        | :class:`~structural.peek`                | :class:`~utils.syncStepper`   |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :meth:`~conv.toHash`         | :class:`~structural.peekF`               | :class:`~utils.zeroes`        |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toCsv`         | :class:`~structural.repeat`              | :class:`~utils.normalize`     |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toAudio`       | :meth:`~structural.repeatF`              |                               |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toUnix`        | :class:`~structural.repeatFrom`          |                               |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toIso`         | :class:`~structural.oneHot`              |                               |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toYMD`         | :class:`~structural.latch`               |                               |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toLinks`       |                                          |                               |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toMovingAvg`   |                                          |                               |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+
| :class:`~conv.toCm`          |                                          |                               |                               |                                  |
+------------------------------+------------------------------------------+-------------------------------+-------------------------------+----------------------------------+

+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| typehint                               | inp                        | output                       | init                       | kxml                      |
+========================================+============================+==============================+============================+===========================+
| :class:`~typehint.tBase`               | :meth:`~inp.cat`           | :class:`~output.stdout`      | :class:`~init.BaseCli`     | :class:`~kxml.node`       |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :class:`~typehint.tAny`                | :class:`~inp.catPickle`    | :class:`~output.tee`         | :class:`~init.Table`       | :class:`~kxml.maxDepth`   |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :class:`~typehint.tList`               | :class:`~inp.splitSeek`    | :class:`~output.file`        | :meth:`~init.T`            | :class:`~kxml.tags`       |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :class:`~typehint.tIter`               | :class:`~inp.refineSeek`   | :class:`~output.pretty`      | :meth:`~init.fastF`        | :class:`~kxml.pretty`     |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :class:`~typehint.tSet`                | :meth:`~inp.wget`          | :class:`~output.unpretty`    | :meth:`~init.yieldT`       | :class:`~kxml.display`    |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :class:`~typehint.tCollection`         | :meth:`~inp.ls`            | :meth:`~output.display`      | :class:`~init.serial`      |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :class:`~typehint.tExpand`             | :class:`~inp.cmd`          | :meth:`~output.headOut`      | :class:`~init.oneToMany`   |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :class:`~typehint.tNpArray`            | :class:`~inp.walk`         | :class:`~output.intercept`   | :class:`~init.mtmS`        |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :class:`~typehint.tTensor`             | :meth:`~inp.requireCli`    | :class:`~output.plotImgs`    |                            |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :meth:`~typehint.tListIterSet`         | :meth:`~inp.urlPath`       |                              |                            |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :meth:`~typehint.tListSet`             | :class:`~inp.kzip`         |                              |                            |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :meth:`~typehint.tListIter`            | :class:`~inp.kunzip`       |                              |                            |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :meth:`~typehint.tArrayTypes`          | :class:`~inp.unzip`        |                              |                            |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :meth:`~typehint.inferType`            |                            |                              |                            |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :class:`~typehint.TypeHintException`   |                            |                              |                            |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :meth:`~typehint.tLowest`              |                            |                              |                            |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :class:`~typehint.tCheck`              |                            |                              |                            |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+
| :class:`~typehint.tOpt`                |                            |                              |                            |                           |
+----------------------------------------+----------------------------+------------------------------+----------------------------+---------------------------+

+---------------------------+-------------------------------+-------------------------+--------------------------------+
| nb                        | grep                          | trace                   | optimizations                  |
+===========================+===============================+=========================+================================+
| :meth:`~nb.cells`         | :class:`~grep.grep`           | :class:`~trace.trace`   | :meth:`~optimizations.dummy`   |
+---------------------------+-------------------------------+-------------------------+--------------------------------+
| :meth:`~nb.grabTags`      | :class:`~grep.grepTemplate`   |                         |                                |
+---------------------------+-------------------------------+-------------------------+--------------------------------+
| :meth:`~nb.executeTags`   |                               |                         |                                |
+---------------------------+-------------------------------+-------------------------+--------------------------------+
| :class:`~nb.pretty`       |                               |                         |                                |
+---------------------------+-------------------------------+-------------------------+--------------------------------+
| :class:`~nb.execute`      |                               |                         |                                |
+---------------------------+-------------------------------+-------------------------+--------------------------------+

