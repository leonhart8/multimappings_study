import argparse
import subprocess
import os

if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Python script using the bowtie2 mapper with varying combinations of -k -N and -a options, expects fasta as -f is used")

    parser.add_argument("index_file", help="The index to be used by bowtie2 in order to proceed with the mapping")
    parser.add_argument("reads_files", nargs='+', help="The reads files to be mapped using the indexed reference")
    parser.add_argument("-k", type=int, dest="k", help="Test value for -k")
    parser.add_argument("-f", action="store_true", help="Input files are fasta /default")
    parser.add_argument("-q", action="store_true", help="Input files are fastq")

    args = parser.parse_args()

    if(args.f and args.q):
        print("input files cannot be fasta and fastq at the same time")
        exit()

    elif(args.f):
        fileOpt = "-f"

    elif(args.q):
        fileOpt = "-q"

    else:
        fileOpt = "-f"

    for i in range(len(args.reads_files)):
        print("Mapping with read file "+args.reads_files[i]+" using default options")
        subprocess.check_call(" ".join(["bowtie2",fileOpt,"-x",args.index_file,"-U",args.reads_files[i],"-S",args.reads_files[i]+"_default"+".sam"]),shell=True)

    for i in range(len(args.reads_files)):
        for k in range(2):
            print("Mapping with read file "+args.reads_files[i]+" using -k "+str(args.k)+" and -N "+str(k))
            sh = " ".join(["bowtie2",fileOpt,"-k",str(args.k),"-N",str(k),"-x",args.index_file,"-U",args.reads_files[i],"-S",args.reads_files[i]+"_k_"+str(args.k)+"_N_"+str(k)+".sam"])
            subprocess.check_call(sh,shell=True)

    for i in range(len(args.reads_files)):
        for j in range(2):
            print("Mapping with read file "+args.reads_files[i]+" using -a and -N "+str(j))
            sh = " ".join(["bowtie2",fileOpt,"-a","-N",str(j),"-x",args.index_file,"-U",args.reads_files[i],"-S",args.reads_files[i]+"_a_"+"N_"+str(j)+".sam"])
            subprocess.check_call(sh,shell=True)
