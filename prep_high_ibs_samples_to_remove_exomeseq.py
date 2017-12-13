#!/usr/bin/python
DIR = "/lustre/scratch115/projects/crohns/exome/TIH/exomeseq/"

import sys, getopt, collections
outfile = ''
missfile = ''
ibsfile = ''
opts, args = getopt.getopt(sys.argv[1:],"hI:M:O:",["help","ibs=","miss=","out="])
for opt, arg in opts:
        if opt == '-h':
                print 'prepare_sample_for_snptest.py --ibs <ibsfile> --miss <missfile> --out <outfile>'
                sys.exit()
        elif opt in ("-I", "--ibs"):
                ibsfile = DIR+arg
	elif opt in ("-M", "--miss"):
		missfile = DIR+arg
	elif opt in ("-O", "--out"):
		outfile = DIR+arg
print ' output file is "', outfile,'"' #for instance, "tili.poly.biallelic.v5.gq30.miss10pc.HWEpass.rsID.highrelatedness.txt"

VARFILE = ibsfile
IID1=[]
IID2=[]
with open(VARFILE,'r') as f:
	f.readline() #skip header
	for line in f.readlines():
		iid1=line.split()[0];
		iid2=line.split()[1];
		IID1.append(iid1)
		IID2.append(iid2)
print IID2[:]
f.close()

#get missingness per sample in
MISSFILE=missfile
MISSDATA={}
with open(MISSFILE,'r') as f:
	f.readline() #skip header
	for line in f.readlines():
		iid=line.split()[0]
		miss=line.split()[4]
		if (iid in IID1) or (iid in IID2) :
			MISSDATA[iid]=miss
f.close()

#now pick a sample to remove from each high IBS pair based on missingness
samples_to_remove=[]
for i,item in enumerate(IID1):
	if MISSDATA[item] > MISSDATA[IID2[i]] :
		samples_to_remove.append(item)
	else:
		samples_to_remove.append(IID2[i])

set_samples_to_remove=set(samples_to_remove)
print set_samples_to_remove

OUTFILE = outfile 
with open (OUTFILE,'w') as outf:
	for str in set_samples_to_remove:
			outf.write("{}\n".format(str));
outf.close()
