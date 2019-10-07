import sys
import common
import argparse
import math
from functools import cmp_to_key

"""
Python scripts that filters a given SAM file from stdin and outputs on stdout
a SAM file with lines selected according to a quality criteria given by the user
as input
"""

"""
This function parses a SAM file and outputs multimapped reads that are mapped on
the same reference only
:param IO stream: IO stream of a SAM file
:return: None
"""
def filterByReference(IOstream):
    line = common.outputHeader(IOstream)
    while line!="":
        multiMaps = list()
        multiMaps.append(line)
        readID = line.split()[0]
        line = IOstream.readline()
        while line!="" and line.split()[0]==readID:
            multiMaps.append(line)
            line = IOstream.readline()
        readsMultimappedSameRef = set()
        for i in range(len(multiMaps)-1):
            for j in range(i+1,len(multiMaps)):
                if common.compareReadIDReferences(multiMaps[i],multiMaps[j])==0:
                    readsMultimappedSameRef.add(multiMaps[i])
                    readsMultimappedSameRef.add(multiMaps[j])
        for outputLine in multiMaps:
            if outputLine in readsMultimappedSameRef:
                sys.stdout.write(outputLine)

"""
This function parses a SAM file and filters out chimeric reads
Splits are determined by using a split_distance which is the overlap tolerated
between two subsequences of a sequence.
:param IO stream: IO stream of a SAM file
:param distance: an int of the specified split_distance
:return: None
"""
def filterChimericReads(IOstream,distance):
    line = common.outputHeader(IOstream)
    while line!="":
        multiMaps = list()
        multiMaps.append(line)
        readID = line.split()[0]
        line = IOstream.readline()
        while line!="" and line.split()[0]==readID:
            multiMaps.append(line)
            line = IOstream.readline()
        splitMappings = set()
        for i in range(len(multiMaps)-1):
            for j in range(i+1,len(multiMaps)):
                splitted_i, splitted_j = multiMaps[i].split(), multiMaps[j].split()
                ipos_b, ipos_e  = common.beg_end_of_seq(splitted_i[5])
                jpos_b, jpos_e  = common.beg_end_of_seq(splitted_j[5])
                if (jpos_b - ipos_e) >= -distance:
                    splitMappings.add(multiMaps[i])
                    splitMappings.add(multiMaps[j])
                elif (ipos_b - jpos_e) >= -distance:
                    splitMappings.add(multiMaps[i])
                    splitMappings.add(multiMaps[j])
        for outputLine in multiMaps:
            if outputLine not in splitMappings:
                sys.stdout.write(outputLine)

if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Allows to filter reads from a SAM file using position criterions, if no option is given or multiple options are given, nothing happens")

    parser.add_argument("-chimeric", nargs=1, dest="split_distance", type=int, help="Chimeric reads are filtered out, the amount of overlap to be filtered is supplied by the user, in amount of nucleotides")
    parser.add_argument("-reference", dest="reference_flag", action='store_true', help="Only give queries multimapped on same reference")

    if(len(sys.argv)==1):
        parser.print_help()
        exit()

    args = parser.parse_args()

    if (args.split_distance and not args.reference_flag):
        filterChimericReads(sys.stdin,args.split_distance[0])
        exit()

    elif (args.reference_flag and not args.split_distance):
        filterByReference(sys.stdin)
        exit()

    else:
        parser.print_help()
