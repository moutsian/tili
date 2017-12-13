#!/usr/bin/python

## Given a case fam file and a ctrl fam file, this simply assigns case/ctrl status to  a fam file from these files that doesn't contain this inormation

import sys, getopt, collections
samplefile = ''
eigenfile = ''
infofile = ''
DIR = "/lustre/scratch115/projects/crohns/exome/TIH/exomeseq/"
opts, args = getopt.getopt(sys.argv[1:],"hs:i:e:",["help","sample=","info=","eigen="])
for opt, arg in opts:
	if opt == '-h':
		print 'prepare_sample_for_snptest.py --sample <samplefile> --info <infofile> --eigen <eigenfile>'
		sys.exit()
	elif opt in ("-s", "--sample"):
		samplefile = DIR+arg
	elif opt in ("-e", "--eigen"):
		eigenfile = DIR+arg
	elif opt in ("-i","--info"):
		infofile = DIR+arg	
print 'sample file is "', samplefile,'"' #for instance, tili.poly.biallelic.v5.gq30.miss10pc.HWEpass.qc3.annot.sample
print 'file with eigenvalues "', eigenfile,'"' #for instance, TILI.qc3.30.evec
print 'file with case/ctrl info is "',infofile, '"' #for instance, tili.poly.biallelic.v5.gq30.miss10pc.HWEpass.qc2.fam
outfile =samplefile+".updated"
SAMPLES=collections.OrderedDict()
#load sample file 
with open(samplefile,'r') as f:
	for line in f.readlines():
		ID=line.split()[0]
		SAMPLES[ID]=line.split()
		if ID=="ID_1": #this is the header line
			SAMPLES[ID]+="pc1 pc2 pc3 pc4 pc5 pc6 pc7 pc8 pc9 pc10\n".split()	
		elif ID=="0": #this is the second line
			SAMPLES[ID]+="C C C C C C C C C C\n".split()
f.close()

#now update case-ctrl status
with open(infofile,'r') as f:
        for line in f.readlines():
		ID=line.split()[0]
		if ID in SAMPLES:
                	SAMPLES[ID][4]=str(int(line.split()[5])-1)
f.close()
#now add the PCs 
with open(eigenfile,'r') as f:
        for line in f.readlines():
		ID=line.split()[0].partition(':')[0]
		if ID in SAMPLES:
#			SAMPLES[ID].append(line.split()[1:11])
			SAMPLES[ID]+=line.split()[1:11]
f.close()

#Now output updated .sample file
with open(outfile,'w') as outf:
	for k,v in SAMPLES.items():
		outf.write(" ".join(v))
		outf.write("\n")
outf.close()
