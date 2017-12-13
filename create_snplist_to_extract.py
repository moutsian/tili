#!/usr/bin/python

#the file from this script is to be used in bcftools with -T option
import sys, getopt
outfile = ''
hwefile = '' #the file with hwe info in the format provided as output by vcftools. For instance "tili.poly.biallelic.nomiss.recode.rs1.ctrls.bcf.hwe"
varfile = '' #the .variants file I've extracted from the vcf file. (first 7-8 columns). For instance, "tili.poly.biallelic.v5.gq30.miss10pc.ctrls.variants"
DIR = "/lustre/scratch115/projects/crohns/exome/TIH/exomeseq/"
opts, args = getopt.getopt(sys.argv[1:],"hO:V:H:",["help","out=","varfile=","hwe="])
for opt, arg in opts:
        if opt == '-h':
                print 'create_snplist_to_extract.py --out <outfile> --varfile <varfile> --hwe <hwefile>'
                sys.exit()
        elif opt in ("-V", "--varfile"):
                infofile = DIR+arg
	elif opt in ("-H", "--hwe"):
		hwefile = DIR+arg
	elif opt in ("-O", "--out"):
		outfile = DIR+arg
print 'hwe file is "', hwefile,'"'

CHROMS=[]
POSITIONS=[]
IDs=[]
POS_DICT={}
with open(varfile,'r') as f:
	for line in f.readlines():
		li=line.lstrip()
		if not li.startswith("#"):
			CHR, POS, ID, REF, ALT, SCORE, QUAL, INFO = li.split()
			CHROMS.append(CHR)
			POSITIONS.append(POS)
			IDs.append(ID)
			POS_DICT[CHR+POS]=ID
f.close()

OUTOFHWE=[]
with open(hwefile,'r') as f:
	f.readline() #skip header
	for line in f.readlines():
		pHWE=line.split()[5]
		Chr=line.split()[0]
		Pos=line.split()[1]
		Chr_Pos=Chr+Pos
		if float(pHWE)<1e-08:
			if Chr_Pos in POS_DICT:
			#idx=POSITIONS.index(line.split()[1])
			#if CHROMS[idx]==line.split()[0]:
			#OUTOFHWE.append(IDs[idx])
				OUTOFHWE.append(POS_DICT[Chr_Pos])
f.close()
#now save OUTOFHWE list to file
with open(outfile,'w') as outf:
	for item in OUTOFHWE:
		outf.write("%s\n" % item)
outf.close()
