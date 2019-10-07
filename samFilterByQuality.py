import sys
import common
import argparse

"""
Python scripts that filters a given SAM file from stdin and outputs on stdout
a SAM file with lines selected according to a quality criteria given by the user
as input
"""

"""
This function parses a SAM format file and outputs the lines that satisfy a quality
criteria
:param IOstream: a SAM file IO stream
:quality: an integer representing the quality threshold of the selected lines
:return: None
"""
def filterByQuality(IOstream,quality):
    line = common.outputHeader(IOstream)
    while line!="":
        readQuality = int(line.split()[4])
        if readQuality>=quality:
            sys.stdout.write(line)
        line = IOstream.readline()

"""
Prints script's usage
"""
def usage():
    print("\nsamFilterByQuality.py parses a SAM file and outputs lines of mapped reads having a MAPping quality (Col 5 of a SAM file mapping) superior or equal to the quality given by user as input\n")
    print("Usage : python3 samFilterByQuality.py [SAM file] [MAPping Quality number]\n")
    print("Example : python3 samFilterByQuality.py example.sam 30\n")
    print("In order to select only mapped reads with quality superior or equal to 30\n")

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Allows to filter reads from a SAM file using a quality criterion")

    parser.add_argument("MAPQ", type=int, help="the lower bound for the MAPQ score of mappings to be kept")

    args = parser.parse_args()

    if (args.MAPQ):
        filterByQuality(sys.stdin,args.MAPQ)

    else:
        args.print_help()
