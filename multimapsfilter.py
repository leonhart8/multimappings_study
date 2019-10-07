import sys
import common
import argparse

"""
Script that takes a SAM file as input and outputs a SAM file containing
only multimapped reads in order for them to be filtered, stored in a file or pipelined
piped to another process

author : Luqman FERDJANI
"""

"""
This function counting for occurrences of reads in a SAM file and returns a set
containing the IDs of the multimapped sequences

:param IOstream: IO stream of SAM file
:return: set of multimapped reads IDs
"""
def extractMultiMappings(IOstream):
    IOstream.seek(0)
    multimappedReads = set()
    occurrences = dict()
    #We start by skipping the @ lines
    line = common.skipAts(IOstream)
    while line!='':
        readID = line.split()[0]
        if readID in occurrences:
            if occurrences[readID]==1:
                multimappedReads.add(readID)
            occurrences[readID]+=1
        else:
            occurrences[readID]=1
        line = IOstream.readline()
    return multimappedReads

"""
This function takes a set containing the IDs of multimapped reads and a SAM file
and outputs on stdout only the SAM file lines about the aforementionned reads

:param multimappedReadsSet: set containing the IDs of multimappedReads
:param IOstream: IO stream of SAM file
"""
def outputMultimappedReads(IOstream,multimappedReadsSet):
    IOstream.seek(0)
    line = common.outputHeader(IOstream)
    while line!='':
        readID = line.split()[0]
        if readID in multimappedReadsSet:
            sys.stdout.write(line)
        line = IOstream.readline()


if __name__=='__main__':

    parser = parser = argparse.ArgumentParser(description="Takes a SAM file and outputs only the multimapped reads on stdout while keeping the SAM format")

    parser.add_argument("sam_files", help="The sam file to be filtered by this script")

    args = parser.parse_args()


    samFile = open(args.sam_files,'r')
    multimappedReadsSet = extractMultiMappings(samFile)
    outputMultimappedReads(samFile,multimappedReadsSet)
    samFile.close()
