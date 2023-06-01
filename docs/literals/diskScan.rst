.. code-block:: text

   ------------------------------------------------------------ Distributed folders ------------------------------------------------------------
   Path                                                                                 Total size   Size on each node (node id and thread count)     
                                                                                                     ae5f4, 8 thr   244f4, 16 thr   f776e, 8 thr      
   ----------------------------------------                                             ----------   ------------   ------------    ------------      
   /home/kelvin/ssd2/data/genome/RegulationFeatureActivity                              16.19 GB     4.11 GB        7.91 GB         4.16 GB           
   /home/kelvin/ssd2/data/genome/go/release_geneontology_org                            8.35 GB      2.07 GB        4.17 GB         2.11 GB           
   /home/kelvin/ssd2/data/genome/RegulationFeatureActivity.backup                       1.72 GB      568.88 MB      552.89 MB       600.61 MB         
   /home/kelvin/ssd2/data/genome/00-common_all.idx                                      1.01 GB      341.74 MB      671.14 MB       0.0 B             
   /home/kelvin/ssd2/data/genome/genbank/ch1.dat.gz                                     50.71 MB     25.36 MB       0.0 B           25.36 MB          
   /home/kelvin/ssd2/test                                                               546.03 kB    136.15 kB      273.53 kB       136.35 kB         
   /home/kelvin/ssd2/data/genome/genbank/ch1                                            0.0 B        0.0 B          0.0 B           0.0 B             
   
   A distributed folder is a folder that has many files and folders inside, but their names
   are all different from each other. It's managed by applyCl.balanceFolder()
   
   ------------------------------------------------------------ Replicated files ------------------------------------------------------------
   Path                                                                                 Total size   Size on each node (node id and thread count)     
                                                                                                     ae5f4, 8 thr   244f4, 16 thr   f776e, 8 thr      
   ----------------------------------------                                             ----------   ------------   ------------    ------------      
   /home/kelvin/ssd2/data/genome/dummy.txt                                              3.3 kB       1.1 kB         1.1 kB          1.1 kB            
   
   A replicated file is a file that has been copied to multiple nodes. Size of all file
   copies should be the same. It's managed by applyCl.replicateFile()
   
   ------------------------------------------------------------ Distributed files ------------------------------------------------------------
   Path                                                                                 Total size   Size on each node (node id and thread count)     
                                                                                                     ae5f4, 8 thr   244f4, 16 thr   f776e, 8 thr      
   ----------------------------------------                                             ----------   ------------   ------------    ------------      
   /home/kelvin/ssd2/data/genome/00-All.vcf                                             130.95 GB    32.74 GB       65.48 GB        32.74 GB          
   /home/kelvin/ssd2/data/genome/MotifFeatures/homo_sapiens.GRCh38.motif_features.gff   55.86 GB     13.96 GB       27.93 GB        13.96 GB          
   /home/kelvin/ssd2/data/genome/00-common_all.vcf                                      9.42 GB      2.35 GB        4.71 GB         2.35 GB           
   
   A distributed file is a file that has been split into multiple pieces and sent to other
   nodes. It's managed by applyCl.balanceFile()
   
