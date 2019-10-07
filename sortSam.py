"""
Script that allows for sorting of SAM files by read ID
"""

import sys
import common
import functools
import argparse

if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Sort a SAM file by several criteria, for now you cannot sort by pos or ref only, only id, id/pos, id/ref, id/pos/ref. The order used between read IDs is the alphabetic order. For sorting using samtools use the sortSam2 script.")

    parser.add_argument("-id", dest="id", action="store_true", help="Allows sorting of SAM file by read ID")
    parser.add_argument("-pos", dest="pos", action="store_true", help="Allows sorting of SAM file by position number")
    parser.add_argument("-ref", dest="ref", action="store_true", help="Allows sorting of SAM file by reference number")

    args = parser.parse_args()

    toBeSorted = list()

    line = common.outputHeader(sys.stdin)

    while line!="":
        toBeSorted.append(line)
        line = sys.stdin.readline()

    if args.pos and args.ref and args.id:
        toBeSorted.sort(key=functools.cmp_to_key(common.compareReadIDReferencesPositions))

    elif args.id and args.pos:
        toBeSorted.sort(key=functools.cmp_to_key(common.compareReadIDPositions))

    elif args.id and args.ref:
        toBeSorted.sort(key=functools.cmp_to_key(common.compareReadIDReferences))

    elif args.id:
        toBeSorted.sort(key=functools.cmp_to_key(common.compareReadID))

    else:
        parser.print_help()
        exit()

    for line in toBeSorted:
        sys.stdout.write(line)
