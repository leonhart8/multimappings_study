import argparse
import common


if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Given two SAM files obtainted using -k and -a, outputs the alignements generated with -a and not with -k")

    parser.add_argument("SAMobtainedByK",help="SAM file obtained with the -k option")
    parser.add_argument("k",type=int,help="The value of k used when producing SAMobtainedByK")
    parser.add_argument("SAMobtainedByA",help="SAM file obtained with the -a option")

    args = parser.parse_args()

    fk, fa = open(args.SAMobtainedByK,'r'), open(args.SAMobtainedByA,'r')

    occK, occA = common.count_occurences(args.SAMobtainedByK), common.count_occurences(args.SAMobtainedByA)

    ligne_k, ligne_a = common.skipAts(fk), common.skipAts(fa)

    while ligne_k!="" and ligne_a!="":

        if ligne_a.split()[0] not in occK:
            read_a = ligne_a.split()[0]
            print("Alignement(s) produit(s) par -a mais pas par -k")
            while ligne_a!="" and ligne_a.split()[0] == read_a:
                print(ligne_a)

        else:
            if occK[ligne_k.split()[0]] < occA[ligne_a.split()[0]]:
                read_id_k = ligne_k.split()[0]
                lignes_set_k = set()
                #We add every line from the file obtained with k to the set
                while ligne_k.split()[0] == read_id_k and ligne_k!="":
                    lignes_set_k.add(ligne_k)
                    ligne_k = fk.readline()
                #We now test which lines have been added in -a
                print("\nAlignements présents en plus grand nombres dans le fichier produit par -a que par -k")
                print("\nAlignements dans le fichier aligné par -a\n")
                while ligne_a.split()[0] == read_id_k and ligne_a!="":
                    if ligne_a not in lignes_set_k:
                        print(ligne_a)
                    ligne_a = fa.readline()
                print("\nAlignements dans le fichier aligné par -k\n")
                for key in lignes_set_k:
                    print(key)

    fa.close()
    fk.close()
