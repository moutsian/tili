#!/usr/bin/python

## Given two bim files, check the allele order between the two files and report mismatches (based on their rsID)
import sys
f1=sys.argv[1]
f2=sys.argv[2]
DIR = "/lustre/scratch115/projects/crohns/exome/TIH/exomeseq/"
#f1=DIR+"1KG_for_PCA_allchr_ready.bim"
#f2=DIR+"tili.ex.QC2.pruned.bim"
outfile=DIR +"files.mismatch.txt"

IDf1={}
with open(f1,'r') as f:
	for line in f.readlines():
		ID=line.split()[1]
		IDf1[ID]=line.split()
f.close()
correct=0
total=0
not_present=0
mismatch=0
otherway=0
to_remove=[]
with open(f2,'r') as f,  open(outfile,'w') as outf:
        for line in f.readlines():
		ID=line.split()[1]
		if ID in IDf1:
			if line.split()[4]==IDf1[ID][4] and line.split()[5]==IDf1[ID][5]:
				correct+=1
	                else:
				if line.split()[4]==IDf1[ID][5] and line.split()[5]==IDf1[ID][4]:
					otherway+=1
				else:
					print("This has different alleles between the two files: {}".format(ID))
					to_remove.append(ID)
				outf.write(" ".join(IDf1[ID]))
				outf.write(" ")
				outf.write(" ".join(line.split()))
				outf.write("\n")
				mismatch+=1
		else:
			not_present+=1
		total+=1;
f.close()
outf.close()
print("Out of {} variants, {} are matching, {} are missing and {} are a mismatch (out of which {} are just arranged the other way around).\nThese are saved in {}\n".format(total,correct,not_present,mismatch,otherway,outfile))


outfile2="snps_with_different_alleles.txt"
with open(outfile2,'w') as outf:
	for variant in to_remove:
		outf.write("{}\n".format(variant))
outf.close()
