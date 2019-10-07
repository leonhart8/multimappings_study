import sys

"""
Module containing general utility functions used by other modules
"""

"""
Allows to count occurrences of each read inside a SAM file
:param sam: a SAM format filename
:return: a dict object containing occurences of each read
"""
def count_occurences(sam):
    fsam = open(sam,'r')
    occurrences = dict()
    #We start by skipping the @ lines
    line = skipAts(fsam)
    while line!='':
        readID = line.split()[0]
        if readID in occurrences:
            occurrences[readID]+=1
        else:
            occurrences[readID]=1
        line = fsam.readline()
    fsam.close()
    return occurrences

"""
Function that parses a SAM file and builds a py set of its reads IDs
:param sam: SAM filename
:return: py set containing all of its reads
"""
def computeSetOfIDs(sam):
    f = open(sam,'r')
    s = set()
    line = skipAts(f)
    while line != "":
        s.add(line.split()[0])
        line = f.readline()
    f.close()
    return s

"""
Function that parses a SAM file and builds a py set of its lines
:param sam: SAM filename
:return: py set containing all of its lines
"""
def computeSetOfLines(sam):
    f = open(sam,'r')
    s = set()
    line = skipAts(f)
    print("compute set of lines for "+sam)
    while line != "":
        s.add(line)
        f.readline()
    f.close()
    return s

"""
This function converts a set of lines into a set of read IDs only
:param lines: set of SAM file lines
:return: set of read IDs only
"""
def convert_lines_to_IDs(lines):
    new_set = set()
    for line in lines:
        new_set.add(line.split()[0])

"""
Function that given a set of reads and a reads file outputs the reads given
in the set. This allows for specific "problematic" reads to be added to files
for further study. This operation only works for fasta format files.
:param read_set: a set of mapped reads IDs
:param reads: a reads filename
"""
def output_selected_reads(read_set,filename):
    reads = open(filename,'r')
    line = reads.readline()
    print("Problematic reads :\n")
    while line!="":
        if line.split()[0].lstrip('>') in read_set:
            print(line)
            print(reads.readline())
        else:
            reads.readline()
        line = reads.readline()
    reads.close()

"""
Skips the first header line starting with '@' in a SAM file and returns last
read line to avoid its loss
:param IOstream: IO stream
:return: last read line
"""
def skipAts(IOstream):
    line = IOstream.readline()
    while line[0]=='@':
        line = IOstream.readline()
        if line =="":
            return line
    return line

"""
Outputs the SAM header and returns first non-header line
:param IOstream: IO stream
:return: last read line
"""
def outputHeader(IOstream):
    line = IOstream.readline()
    while line[0]=='@':
        sys.stdout.write(line)
        line = IOstream.readline()
    return line

"""
Parses a CIGAR field and returns a percentage of similarity
:param cigar: Str, a cigar string
:returns: float, the similarity percentage between a given sequence and the sequence
it is being mapped to

DISCLAIMER : not a very reliable number as M could indicate mismatch in CIGAR strings
presented using the legacy format
"""
def parseCigar(cigar):
    i = int()
    matches = int()
    sequenceLength = int()
    for i in range(0,len(cigar)):
        if cigar[i]=='M' or cigar[i]=='=':
            matches += cigar[i-1]
            sequenceLength += cigar[i-1]
        if cigar[i]=='I' or cigar[i]=='S' or cigar[i]=='X':
            sequenceLength += cigar[i-1]
    return matches/sequenceLength

"""
Parses a CIGAR field and returns SEQ's size
:param cigar: Str, a cigar string
:returns: int, size of the sequence represented by the CIGAR
"""
def sizeSeq(cigar):
    seq_size = int()
    for char in cigar:
        if char=='M' or char=='I' or char=='S' or char=='=' or char=='X':
            seq_size+=1
    return seq_size

"""
This function detects the beginning and end position of a mapped portion
of a read, it is to be used in the detection of split mappings
:param cigar: str, cigar string of mapped read
:returns: tuple, a double containing the beginning position and the end position
          of the sub sequence of the read involved in the mapping
"""
def beg_end_of_seq(cigar):
    beg_pos = 0
    first_m, last_m = cigar.find('M') , cigar.rfind('M')
    i = int()
    digit_string = str()
    while i<first_m:
        if cigar[i].isdigit():
            digit_string+=cigar[i]
        else:
            beg_pos+=int(digit_string)
            digit_string = str()
        i+=1
    end_pos = beg_pos + int(digit_string)
    digit_string = str()
    i+=1
    while i<=last_m:
        if cigar[i].isdigit():
            digit_string+=cigar[i]
        else:
            end_pos += int(digit_string)
            digit_string = str()
        i+=1
    return (beg_pos,end_pos)


"""
Comparison functions
"""

"""
Given two lines of a SAM file, compares their read IDs
:param lineX: line of a SAM file
:param lineY: line of a SAM file
"""
def compareReadID(lineX,lineY):
    readIDX = lineX.split()[0]
    readIDY = lineY.split()[0]
    if readIDX<readIDY:
        return -1
    elif readIDX>readIDY:
        return 1
    else:
        return 0

"""
Given two lines of a SAM file, compares their read IDs and their references
for sorting operations
:param lineX: line of a SAM file
:param lineY: line of a SAM file
"""
def compareReadIDReferences(lineX,lineY):
    readIDX = lineX.split()[0]
    readIDY = lineY.split()[0]
    if readIDX<readIDY:
        return -1
    elif readIDX>readIDY:
        return 1
    else:
        if lineX.split()[2]<lineY.split()[2]:
            return -1
        elif lineX.split()[2]>lineY.split()[2]:
            return 1
        else:
            return 0

"""
Given two lines of a SAM file, compares their read IDs and positions
for sorting operations
:param lineX: line of a SAM file
:param lineY: line of a SAM file
"""
def compareReadIDPositions(lineX,lineY):
    readIDX = lineX.split()[0]
    readIDY = lineY.split()[0]
    if readIDX[0]<readIDY[0]:
        return -1
    elif readIDX[0]>readIDY[0]:
        return 1
    else:
        if int(lineX.split()[3])<int(lineY.split()[3]):
            return -1
        elif int(lineX.split()[3])>int(lineY.split()[3]):
            return 1
        else:
            return 0

"""
Given two lines of a SAM file, compares their read IDs, then read alignements
then positions for sorting operations
:param lineX: line of a SAM file
:param lineY: line of a SAM file
"""
def compareReadIDReferencesPositions(lineX,lineY):
    readIDX = lineX.split()[0]
    readIDY = lineY.split()[0]
    if readIDX<readIDY:
        return -1
    elif readIDX>readIDY:
        return 1
    else:
        if lineX.split()[2]<lineY.split()[2]:
            return -1
        elif lineX.split()[2]>lineY.split()[2]:
            return 1
        else:
            if int(lineX.split()[3])<int(lineY.split()[3]):
                return -1
            elif int(lineX.split()[3])>int(lineY.split()[3]):
                return 1
            else:
                return 0
