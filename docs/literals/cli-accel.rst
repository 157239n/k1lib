.. code-block::

   ========== `array | cli` and `array | cli.all(int)` capability
   conv.toArgmax              conv.toArgmin               conv.toAvg                     
   conv.toMax                 conv.toMedian               conv.toMin                     
   conv.toNdArray             conv.toProd                 conv.toStd                     
   conv.toSum                 conv.toTensor               filt.cut                       
   filt.rows                  modifier.clamp              modifier.randomize             
   modifier.roll              modifier.sort               structural.batched             
   structural.insert          structural.insertIdColumn   structural.joinStreams         
   structural.repeat          structural.repeatFrom       structural.transpose           
   structural.window          utils.item                  utils.normalize                
   utils.rItem                utils.reverse               utils.size                     
   utils.wrapList             
   
   ========== `array | cli.all(int)` capability alone
   filt.head                  modifier.applyS             utils.smooth                   
   
   ========== `array | cli` capability alone
   conv.idxsToNdArray         conv.toCm                   conv.toFloat                   
   conv.toImg                 conv.toInt                  conv.toUnix                    
   filt.contains              filt.filt                   filt.filtStd                   
   filt.inSet                 filt.mask                   filt.unique                    
   models.tsne                modifier.apply              output.plotImgs                
   structural.groupBy         structural.hist             structural.joinStreamsRandom   
   structural.peek            structural.peekF            structural.splitC              
   structural.splitW          utils.deref                 utils.ignore                   
   utils.zeroes               
   
   ========== No array acceleration
   bio.complement             bio.idx                     bio.longAa                     
   bio.medAa                  bio.transcribe              bio.translate                  
   conv.toAnchor              conv.toAngle                conv.toAudio                   
   conv.toBytes               conv.toCsv                  conv.toDataUri                 
   conv.toDict                conv.toDist                 conv.toFileType                
   conv.toGray                conv.toHtml                 conv.toIso                     
   conv.toLinks               conv.toList                 conv.toMovingAvg               
   conv.toPdf                 conv.toRange                conv.toRgb                     
   conv.toRgba                conv.toYMD                  conv.toYaml                    
   filt.breakIf               filt.empty                  filt.intersection              
   filt.tail                  filt.trigger                filt.tryout                    
   filt.union                 init.BaseCli                init.mtmS                      
   init.oneToMany             init.serial                 inp.catPickle                  
   inp.cmd                    inp.kunzip                  inp.kzip                       
   inp.refineSeek             inp.splitSeek               inp.walk                       
   models.bloom               models.complete             models.embed                   
   models.kmeans              modifier.applyCl            modifier.applyMp               
   modifier.applySerial       modifier.applyTh            modifier.consume               
   modifier.integrate         modifier.iterDelay          modifier.op                    
   modifier.sortF             modifier.stagger            output.file                    
   output.intercept           output.pretty               output.stdout                  
   output.tee                 output.unpretty             structural.AA_                 
   structural.activeSamples   structural.batchedTrigger   structural.count               
   structural.insertColumn    structural.latch            structural.oneHot              
   structural.permute         structural.reshape          structural.ungroup             
   typehint.tCheck            typehint.tOpt               utils.backup                   
   utils.bindec               utils.branch                utils.clipboard                
   utils.getitems             utils.iden                  utils.join                     
   utils.lookup               utils.lookupRange           utils.rateLimit                
   utils.sketch               utils.syncStepper           utils.timeLimit                
