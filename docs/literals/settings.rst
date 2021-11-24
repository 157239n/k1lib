.. code-block:: text

   Settings:                                         
   - svgScale = 0.7                                  ​default svg scales for clis that displays graphviz graphs                                                           
   - wd       = /home/kelvin/repos/labs/k1lib/docs   ​default working directory, will get from `os.getcwd()`. Will update using `os.chdir()` automatically when changed   
   - bio      = <Settings>                           ​everything related to biology                                                                                       
     - blast = None                                  ​location of BLAST database                                                                                          
   - cli      = <Settings>                           ​from k1lib.cli module                                                                                               
     - defaultDelim  = 	                             ​default delimiter used in-between columns when creating tables. Defaulted to tab character.                         
     - defaultIndent =                               ​default indent used for displaying nested structures                                                                
     - oboFile       = None                          ​gene ontology obo file location                                                                                     
     - strict        = False                         ​turning it on can help you debug stuff, but could also be a pain to work with                                       
     - lookupImgs    = True                          ​sort of niche. Whether to auto looks up extra gene ontology relationship images                                     
     - inf           = inf                           ​infinity definition for many clis. Here because you might want to temporarily not loop things infinitely            
   - eqn      = <Settings>                           ​from k1lib.eqn module                                                                                               
     - spaceBetweenValueSymbol = True                ​                                                                                                                    
     - eqnPrintExtras          = True                ​                                                                                                                    
   - mo       = <Settings>                           ​from k1lib.mo module                                                                                                
     - overOctet = False                             ​whether to allow making bonds that exceeds the octet rule                                                           
                                                     