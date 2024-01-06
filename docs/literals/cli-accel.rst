.. code-block::

   ========== `array | cli` and `array | cli.all(int)` capability
   conv.toAvg                conv.toMax                  conv.toMin                     
   conv.toProd               conv.toStd                  conv.toSum                     
   modifier.sort             structural.batched          structural.joinStreams         
   structural.repeat         structural.repeatFrom       structural.transpose           
   utils.rItem               utils.reverse               utils.size                     
   utils.wrapList            
   
   ========== `array | cli.all(int)` capability alone
   utils.item                
   
   ========== `array | cli` capability alone
   conv.toArgmax             conv.toArgmin               conv.toCm                      
   conv.toFloat              conv.toInt                  conv.toPIL                     
   conv.toTensor             models.tsne                 modifier.apply                 
   modifier.clamp            modifier.randomize          modifier.roll                  
   output.plotImgs           structural.hist             structural.joinStreamsRandom   
   utils.deref               utils.ignore                utils.normalize                
   utils.smooth              utils.zeroes                
   
   ========== No array acceleration
   bio.complement            bio.idx                     bio.longAa                     
   bio.medAa                 bio.transcribe              bio.translate                  
   conv.toAnchor             conv.toAudio                conv.toBytes                   
   conv.toCsv                conv.toDataUri              conv.toDict                    
   conv.toGray               conv.toHtml                 conv.toIso                     
   conv.toLinks              conv.toList                 conv.toMovingAvg               
   conv.toRange              conv.toRgb                  conv.toRgba                    
   conv.toUnix               conv.toYMD                  init.BaseCli                   
   init.mtmS                 init.oneToMany              init.serial                    
   inp.catPickle             inp.cmd                     inp.kunzip                     
   inp.kzip                  inp.refineSeek              inp.splitSeek                  
   inp.walk                  models.bloom                models.complete                
   models.embed              models.kmeans               modifier.applyCl               
   modifier.applyMp          modifier.applyS             modifier.applySerial           
   modifier.applyTh          modifier.consume            modifier.integrate             
   modifier.op               modifier.sortF              modifier.stagger               
   output.file               output.intercept            output.pretty                  
   output.stdout             output.tee                  output.unpretty                
   structural.AA_            structural.activeSamples    structural.batchedTrigger      
   structural.count          structural.groupBy          structural.insert              
   structural.insertColumn   structural.insertIdColumn   structural.latch               
   structural.oneHot         structural.peek             structural.peekF               
   structural.permute        structural.reshape          structural.splitC              
   structural.splitW         structural.ungroup          structural.window              
   typehint.tCheck           typehint.tOpt               utils.backup                   
   utils.bindec              utils.clipboard             utils.dictFields               
   utils.iden                utils.join                  utils.lookup                   
   utils.rateLimit           utils.sketch                utils.syncStepper              
   utils.timeLimit           
