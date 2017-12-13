#!/usr/bin/python
DIR = "/lustre/scratch115/projects/crohns/exome/TIH/exomeseq/"
rsIDfile="snps_to_remove_due_to_diffmiss.txt"
varposfile="tili.i2.pb.gq30.ab1e03.miss10.rs1.HWE.variants" #check if the rsIDs have been updated, if not use tili.poly.biallelic.v5.gq30.miss10pc.HWEpass.variants
VARPOSFILE = DIR+varposfile
RSIDFILE = DIR+rsIDfile
OUTFILE=DIR+"snps_to_remove_due_to_diffmiss.varpos.i2.txt"

CHROMS=[]
POSITIONS=[]
IDs=[]
ID_DICT={}
with open(VARPOSFILE,'r') as f:
	for line in f.readlines():
		li=line.lstrip()
		if not li.startswith("#"):
			CHR, POS, ID, REF, ALT, SCORE, QUAL, INFO = li.split()
			CHROMS.append(CHR)
			POSITIONS.append(POS)
			IDs.append(ID)
			ID_DICT[ID]=(CHR,POS)
#print IDs[:10]
f.close()

OUT_VARPOS=[]
with open(RSIDFILE,'r') as f:
	for line in f.readlines():
		ID=line.split()[0]
		if ID in ID_DICT:
			OUT_VARPOS.append(ID_DICT[ID])
f.close()
with open(OUTFILE,'w') as outf:
	for item in OUT_VARPOS:
		outf.write("{}\t{}\n".format(item[0],item[1]));
outf.close()
#str(mytuple)[1:-1]
