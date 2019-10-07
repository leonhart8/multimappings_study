import common
import argparse

"""
This module is used to check the coherence of the multimappings selected by bowtie2
Namely if no multimappings are lost when being given less selective options and
that when using -k N, no new read is being mapped N times using -a as an option
(checking for coherence)
"""

"""
Given 3 SAM files with only multimappings, this function parses each SAM file
produces a set containing all multimapped reads and checks their inclusion from
file X to file Z, checking that set X c set Y c set Z
:param file[letter]: SAM files
:returns: Bool,
            True  if the condition is satisfied
            False otherwise
"""
def check_inclusion(fileX,fileY,fileZ):

    fx, fy, fz = open(fileX,'r'), open(fileY,'r'), open(fileZ,'r')
    setX, setY, setZ = set(), set(), set()
    lineX, lineY, lineZ = common.skipAts(fx), common.skipAts(fy), common.skipAts(fz)

    #Generating sets one by one for simplicity
    while lineX!="":
        setX.add(lineX.split()[0])
        lineX = fx.readline()

    while lineY!="":
        setY.add(lineY.split()[0])
        lineY = fy.readline()

    while lineZ!="":
        setZ.add(lineZ.split()[0])
        lineZ = fz.readline()

    fx.close()
    fy.close()
    fz.close()

    return setX <= setY <= setZ

"""
Counts occurences of multimapped reads in a SAM file containing only multimapped
reads obtained with a -k N option and a -a option to check if no new read is being
mapped N times when using the -a option
:param files[number]: files described earlier
:param k: int, the value supplied to the -k option when SAM file was produced
:return: Bool,
            True if for every read mapped N times using -a there is a corresponding read mapped N times using -k N
            False otherwise
"""
def check_coherence(fileX,fileY,reads,k):

    ret = True

    weirdAdditionnalOccurences = set()

    #Counting occurences for fileX
    readOccX = common.count_occurences(fileX)

    #Counting occurences for fileY
    readOccY = common.count_occurences(fileY)

    for readY in readOccY:
        #We check if a mapping occurs less than k times in -a with more mappings compared to -k
        if (readY in readOccX and readOccX[readY]<k and readOccY[readY]>readOccX[readY]):
            ret = False
            weirdAdditionnalOccurences.add(readY)

    fx , fy = open(fileX,'r') , open(fileY, 'r')

    line_x , line_y = common.skipAts(fx) , common.skipAts(fy)

    print("\nIncoherent mappings obtained with -k "+str(k)+"\n")
    while line_x!="":
        if line_x.split()[0] in weirdAdditionnalOccurences:
            read_id = line_x.split()[0]
            print("\nThere is an incoherence with read "+read_id+" here are its mappings\n")
            while(line_x.split()[0] == read_id and line_x!=""):
                print(line_x)
                line_x = fx.readline()
        else:
            line_x = fx.readline()

    print("\nIncoherent mappings obtained with -a \n")
    while line_y!="":
        if line_y.split()[0] in weirdAdditionnalOccurences:
            read_id = line_y.split()[0]
            print("\nThere is an incoherence with read "+read_id+" here are its mappings\n")
            while(line_y.split()[0] == read_id and line_y!=""):
                print(line_y)
                line_y = fy.readline()
        else:
            line_y = fy.readline()

    fx.close()
    fy.close()

    common.output_selected_reads(weirdAdditionnalOccurences,reads)

    return ret

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Python script checking for coherence on 3 different SAM format files, namely that no multimapped read disappears when using more permissive options, and that no new occurerence of a read mapped N times appears in -a and not in -k N")

    parser.add_argument("fileAlignedDefault", help="The sam file obtained by using bowtie2 with the default option")
    parser.add_argument("fileAlignedUsingK", help="The sam file obtained by using bowtie2 with the k option")
    parser.add_argument("fileAlignedUsingA", help="The sam file obtained by using bowtie2 with the -a option")
    parser.add_argument("readsFile", help="The reads file used for the alignement")
    parser.add_argument("k", type=int, help="The integer supplied to -k when aligning using bowtie2")

    args = parser.parse_args()

    if (check_inclusion(args.fileAlignedDefault,args.fileAlignedUsingK,args.fileAlignedUsingA)):
        print("Each set of multimapped reads are included into each other in the right order")

    else:
        print("Each set of multimapped reads are not included into each other in the right order")

    if(check_coherence(args.fileAlignedUsingK,args.fileAlignedUsingA,args.readsFile,args.k)):
        print("No new read is being aligned "+str(args.k)+" times using -a that has not been found using -k "+str(args.k))

    else:
        print("New read(s) are being aligned "+str(args.k)+" times using -a that have not been found using -k "+str(args.k))
