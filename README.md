# label_recherche

Study of multi-mapped reads using several aligners
This repository contains several scripts useful for :
  -  filtering SAM files according to specific criteria
  -  sorting SAM files by readID/ref/position on the ref genome
  -  outputting intersection and differences in alignements between 2 SAM files
  - also added scripts that specifically test bowtie2

# Scripts descriptions

- multimapsfilter.py:  
  The MVP of these scripts. The alpha and the omega, the one with which all of
  this adventure began.  
  A SAM file filter. Takes a SAM file as argument and outputs the result on STDOUT. Removes all reads mapped only once.  
  Example : $ py multimapsfilter.py <example.sam>  
  Will output only the multimapped reads in example.sam  
  More info with : $ py multimapsfilter.py  

- samFilterByPosition.py:  
  A SAM file filter. Takes a SAM file from STDIN and outputs the result on STDOUT. Can filter by reference, or splitted reads.  
  Example : $ cat example.sam | py samFilterByPositon -chimeric 10  
  Will filter all splitted reads with an overlap lesser or equal to 10 bases  
  More info with : $ py samFilterByPositon -h  

- samFilterByQuality.py:  
  A SAM file filter. Takes a SAM file from STDIN and outputs the result on STDOUT.  
  Filters all the mappings with quality strictly inferior to MAPQ passed as argument.  
  Example : $ $ cat example.sam | py samFilterByQuality 30  
  Will output only mappings with MAPQ superior or equal to 30.  
  More info with : $ py samFilterByQuality -h  

 - sortSam.py:  
  A SAM file sorter. Takes a SAM file from STDIN and outputs the result on STDOUT.  
  Sorts lines of a SAM file by read ID, rID and ref, rID and pos, or rID pos and ref, using the .sort python methods and the functools module.  
  The ordering used is the lexicographical one.  
  Example : $ cat example.sam | py sortSam.py -id  
  Will sort example.sam by read ID and output it on STDOUT.  
  More info with : py sortSam.py -h  

- sortSam2.py:  
  A SAM file sorter. Takes a sam or bam filename as argument and sorts it by
  read IDs.  
  If the file is a SAM file, it converts it in a bam with name out.bam, sorts it
  and outputs the sorted SAM on STDOUT.  
  Else, add -b as an option, and the file will be directly sorted and outputted
  on STDOUT.  
  Example : $ py sortSam2.py -b <example.bam>  
  Will sort and output the sorted file in SAM format on STDOUT  
  More info with : py sortSam2.py -h  

- testOptionsBowtie.py:  
  Allows to automate test with bowtie2. Requires a list of reads files an index  
  prefix a value for -k, and options -f/-q indicating the format of the reads
  files. The alignements are then performed.  
  Example : $ py testOptionsBowtie -k 5 -f <index.prefix> <reads1.fasta> ... <readsn.fasta>  
  Will align all reads files using the supplied index with default parameters,
  -k 5 (N0/1) and -a (N0/1)  
  More info with : py testOptionsBowtie.py -h  

- testCoherenceBowtie.py:  
  Used to perform tests on SAM files produced by bowtie2. Takes as argument a  
  SAM file aligned using default options, a SAM file aligned using -k and another
  file aligned using -a in this exact order. Also requires the value used for -k.  
  The script also requires the reads files to output the reads that have failed
  the tests.  
  And produces on STDOUT the results of the test.  
  Checks the following inclusion of alignements : default c -k N c -a  
  Checks if mappings appearing less than N times obtained with -k N don't appear
  in higher amounts with -a  
  Example : $ py testCoherenceBowtie.py <sam_default.sam> <sam_k.sam> <sam_a.sam> -k 5  
  Will perform all of these tests assuming that the SAM file obtained with -k was
  obtained with -k 5.  
  More info with : py testCoherenceBowtie.py -h  

- venn.py:  
  Used to output the intersection and differences between mappings of two SAM
  files. The SAM files required as input MUST BE SORTED BY READ ID.  
  I REPEAT. THEY. MUST. BE. SORTED. BY. READ. ID  
  DROP UNSORTED FILES AND YOU WILL GET GARBAGE.  
  Example : $ py venn.py <file1.sam> <file2.sam> <diff1.> <diff2.> <inter.>  
  Will compare file1 and file2 and output the mappings seen in file1 and not file2
  in diff1 and vice-versa for diff2. The mappings seen in both will be outputted
  in inter.  
  More info with : py venn.py -h  

# COMMANDS

In order to clean the repository of indexes, and sam files:
  $ make clean
