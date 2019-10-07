import argparse
import subprocess

if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Sorting script using samtools instead of python .sort list method, converts the input back to SAM and outputs on stdout. This script doesn't delete the sorted BAM used in the process")

    parser.add_argument("-b", action='store_true', help="Option to indicate that the input file is a BAM")
    parser.add_argument("inputFile", help="SAM or BAM (if -b is supplied) file to be sorted by reference")

    args = parser.parse_args()

    if args.b:
        bam_filename = args.inputFile

    if not args.b:
        print("Converting file to BAM first")
        bam_filename = "out.bam"
        print(" ".join(["samtools","view","-Sb",args.inputFile,">",bam_filename]))
        subprocess.check_call(" ".join(["samtools","view","-Sb",args.inputFile,">",bam_filename]),shell=True)

    print("Sorting ...")
    sorted_bam_prefix = bam_filename.rstrip(".bams")+"_sorted"
    print(" ".join(["samtools","sort","-n",bam_filename,sorted_bam_prefix]))
    subprocess.check_call(" ".join(["samtools","sort","-n",bam_filename,sorted_bam_prefix]),shell=True)

    print("Converting BAM back to SAM")
    print(" ".join(["samtools","view","-h",sorted_bam_prefix+".bam"]))
    subprocess.check_call(" ".join(["samtools","view","-h",sorted_bam_prefix+".bam"]),shell=True)
