.. code-block::

   ========== `array | cli` and `array | cli.all(int)` capability
   conv.toAvg                conv.toMax                 conv.toMin                     
   conv.toProd               conv.toStd                 conv.toSum                     
   modifier.sort             structural.batched         structural.joinStreams         
   structural.repeat         structural.repeatFrom      structural.transpose           
   utils.rItem               utils.reverse              utils.size                     
   utils.wrapList            
   
   ========== `array | cli.all(int)` capability alone
   utils.item                
   
   ========== `array | cli` capability alone
   conv.toFloat              conv.toInt                 conv.toPIL                     
   conv.toTensor             modifier.apply             modifier.randomize             
   output.plotImgs           structural.hist            structural.joinStreamsRandom   
   utils.deref               utils.smooth               
   
   ========== No array acceleration
   bio.complement            bio.idx                    bio.longAa                     
   bio.medAa                 bio.transcribe             bio.translate                  
   conv.toBytes              conv.toDict                conv.toGray                    
   conv.toHtml               conv.toList                conv.toRange                   
   conv.toRgb                conv.toRgba                init.BaseCli                   
   init.mtmS                 init.oneToMany             init.serial                    
   inp.cmd                   inp.kunzip                 inp.kzip                       
   inp.refineSeek            inp.splitSeek              inp.walk                       
   models.complete           models.embed               models.kmeans                  
   modifier.applyCl          modifier.applyMp           modifier.applyS                
   modifier.applySerial      modifier.applyTh           modifier.consume               
   modifier.integrate        modifier.op                modifier.sortF                 
   modifier.stagger          output.file                output.intercept               
   output.pretty             output.stdout              output.tee                     
   structural.AA_            structural.activeSamples   structural.count               
   structural.expandE        structural.groupBy         structural.insert              
   structural.insertColumn   structural.oneHot          structural.peek                
   structural.peekF          structural.permute         structural.reshape             
   structural.splitC         structural.splitW          structural.ungroup             
   structural.window         typehint.tCheck            typehint.tOpt                  
   utils.backup              utils.bindec               utils.clipboard                
   utils.dictFields          utils.iden                 utils.ignore                   
   utils.join                utils.lookup               utils.rateLimit                
   utils.sketch              utils.syncStepper          utils.timeLimit                
