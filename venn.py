import common
import argparse

"""
This module includes function and a main that parses 2 SAMs in order to output
the elements they have in common and the differences between both using py sets
"""

"""
This function takes two SAMs as parameters and computes the differences in
lines and their intersections
Difference is sam1 - sam2
:param sam1: one of the SAM filenames
:param sam2: one of the SAM filenames
"""
def computes_difference_and_inter(sam1,sam2):
    set1 , set2 = common.computeSetOfLines(sam1) , common.computeSetOfLines(sam2)
    return (set1 - set2 , set2 - set1, set1 & set2)

"""
This function uses two SAMs, and outputs the read ID, CIGAR string and mapping
position of their differing mappings, followed by the relevent reads
:param sam1: one of the SAM filenames
:param sam2: one of the SAM filenames
:param reads: the reads file used to generate the mapping
"""
def output_diff(sam1,sam2,reads,diff_1_2,diff_2_1,diff_1_2_reads,diff_2_1_reads):
    print("These mappings are only seen in "+sam1+" and not in "+sam2+" : ")
    f1 = open(sam1,'r')
    line = common.skipAts(f1)
    while line != "":
        if line in diff_1_2:
            print("READ ID : "+line.split()[0])
            print("POS ON RED : "+line.split()[3])
            print("CIGAR : "+line.split()[5])
        line = f1.readline()
    f1.close()
    print("Now outputting the relevent reads : ")
    common.output_selected_reads(diff_1_2,reads)
    f2 = open(sam2,'r')
    line = common.skipAts(f2)
    print("These mappings are only seen in "+sam2+" and not in "+sam1+" : ")
    while line != "":
        if line in diff_2_1:
            print("READ ID : "+line.split()[0])
            print("POS ON RED : "+line.split()[3])
            print("CIGAR : "+line.split()[5])
        line = f2.readline()
    f2.close()
    print("Now outputting the relevent reads : ")
    common.output_selected_reads(diff_2_1,reads)



"""
This function uses two SAMs, and outputs the read ID, CIGAR string and mapping
position of their common parts
:param sam1: one of the SAM filenames
:param sam2: one of the SAM filenames
:param reads: the reads file used to generate the mapping
"""
def output_intersection(sam1,sam2,reads,inter,inter_reads):

    print("These are the common mappings between both files : ")
    f = open(sam1,'r')
    line = common.skipAts(f)
    while line != "":
        if line in inter:
            print("READ ID : "+line.split()[0])
            print("POS ON RED : "+line.split()[3])
            print("CIGAR : "+line.split()[5])
        line = f.readline()
    f.close()
    print("Now outputting the relevent reads : ")
    common.output_selected_reads(inter_reads,reads)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Python script which computes and outputs intersection and differences between two sets of mappings")

    parser.add_argument("samFile1", help="One of the SAM files to be studied")
    parser.add_argument("samFile2", help="The second SAM file to be studied")
    parser.add_argument("outfileDifferences1", help="Name of the file where the mappings in file1 but not in file2 will be outputted")
    parser.add_argument("outfileDifferences2", help="Name of the file where the mappings in file2 but not in file1 will be outputted")
    parser.add_argument("outfileIntersection", help="Name of the file where the intersection will be outputted")

    args = parser.parse_args()

    o_diff1, o_diff2 , o_inter = open(args.outfileDifferences1,"w+") , open(args.outfileDifferences2,"w+") , open(args.outfileIntersection,"w+")
    o_diff1.write("Mappings found in "+args.samFile1+" and not in "+args.samFile2+"\n")
    o_diff2.write("Mapping found in "+args.samFile1+" and not in "+args.samFile2+"\n")
    o_inter.write("This file will contain the common mappings between both SAM files "+args.samFile1+" and "+args.samFile2+"\n")

    f1 , f2 = open(args.samFile1,'r') , open(args.samFile2, 'r')
    line1 , line2 = common.skipAts(f1) , common.skipAts(f2)

    while line1 !="" or line2 != "":
        read1 , read2 = line1.split()[0] , line2.split()[0]
        if read1 < read2:
            splitted = line1.split()
            o_diff1.write("Mappings with read ID"+splitted[0]+" :\n\n")
            while line1!="" and splitted[0] == read1:
                o_diff1.write("POS ON REF : "+splitted[3]+"\n")
                o_diff1.write("CIGAR : "+splitted[5]+"\n")
                line1 = f1.readline()
                splitted = line1.split()
            o_diff1.write("\n\n")
        elif read2 < read1:
            splitted = line2.split()
            o_diff2.write("Mappings with read ID "+read2+" :\n\n")
            while line2!="" and splitted[0] == read2:
                o_diff2.write("POS ON REF : "+splitted[3]+"\n")
                o_diff2.write("CIGAR : "+splitted[5]+"\n\n")
                line2 = f2.readline()
                splitted = line2.split()
            o_diff2.write("\n\n")
        else:
            d1 , d2 = dict() , dict()
            splitted1 , splitted2 = line1.split() , line2.split()
            while line1!="" and splitted1[0] == read1:
                d1[(splitted1[0],splitted1[3])] = splitted1[5]
                line1 = f1.readline()
                splitted1 = line1.split()
            while line2!="" and splitted2[0] == read2:
                d2[(splitted2[0],splitted2[3])] = splitted2[5]
                line2 = f2.readline()
                splitted2 = line2.split()
            diff_1_2 , diff_2_1 , inter = set() , set() , set()
            for key1 in d1:
                if key1 in d2:
                    inter.add(key1)
                else:
                    diff_1_2.add(key1)
            for key2 in d2:
                if key2 in d1:
                    inter.add(key2)
                else:
                    diff_2_1.add(key2)
            if len(diff_1_2)!=0:
                o_diff1.write("Mappings with read ID "+read1+" :\n\n")
                for t in diff_1_2:
                    o_diff1.write("POS ON REF : "+t[1]+"\n")
                    o_diff1.write("CIGAR : "+d1[t]+"\n\n")
            if len(diff_2_1)!=0:
                o_diff2.write("Mappings with read ID "+read1+" :\n")
                for t in diff_2_1:
                    o_diff2.write("POS ON REF : "+t[1]+"\n")
                    o_diff2.write("CIGAR : "+d2[t]+"\n\n")
            if len(inter)!=0:
                o_inter.write("Mappings with read ID "+read1+" :\n")
                for t in inter:
                    o_inter.write("POS ON REF : "+t[1]+"\n")
                    o_inter.write(args.samFile1+" CIGAR : "+d1[t]+"\n\n")
                    o_inter.write(args.samFile2+" CIGAR : "+d2[t]+"\n\n")

    if line1 != "":
        while line1 != "":
            splitted = line1.split()
            read1 = splitted[0]
            o_diff1.write("Mappings with read ID "+read1+" :\n\n")
            while line1!="" and splitted[0] == read1:
                o_diff1.write("POS ON REF : "+splitted[3]+"\n")
                o_diff1.write("CIGAR : "+splitted[5]+"\n\n")
                line1 = f1.readline()
                splitted = line1.split()
            o_diff1.write("\n")

    elif line2 != "":
        while line2 != "":
            splitted = line2.split()
            read2 = splitted[0]
            o_diff2.write("Mappings with read ID "+read2+" :\n\n")
            while line2!="" and splitted[0] == read2:
                o_diff2.write("POS ON REF : "+splitted[3]+"\n")
                o_diff2.write("CIGAR : "+splitted[5]+"\n\n")
                line2 = f2.readline()
                splitted = line2.split()
            o_diff2.write("\n")
