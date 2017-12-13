#!/usr/bin/python


import sys, getopt, collections
samplefile = ''
DIR = "/lustre/scratch115/projects/crohns/exome/TIH/exomeseq/"
opts, args = getopt.getopt(sys.argv[1:],"hs:",["help","sample="])
for opt, arg in opts:
	if opt == '-h':
		print 'prepare_sample_for_snptest.py --sample <samplefile> '
		sys.exit()
	elif opt in ("-s", "--sample"):
		samplefile = DIR+arg
print 'sample file is "', samplefile,'"' #for instance, tili.poly.biallelic.v5.gq30.miss10pc.HWEpass.qc3.annot.sample
outfile =samplefile+".for_epacts.ped"
SAMPLES=collections.OrderedDict()
#load sample file 
with open(samplefile,'r') as f:
	for line in f.readlines():
		ID=line.split()[0]
		if ID=="ID_1": #this is the header line
			SAMPLES[ID]="#FAM_ID IND_ID FAT_ID MOT_ID SEX DISEASE pc1 pc2 pc3 pc4 pc5 pc6 pc7 pc8 pc9 pc10\n".split()
		elif ID=="0": #this is the second line, skip it
			#do nothing
			print("Pod")
		else:
	                SAMPLES[ID]=line.split()[:2]
			SAMPLES[ID]+=" 0 0 -9 ".split()
			SAMPLES[ID]+=str(int(line.split()[4])+1)
			SAMPLES[ID]+=line.split()[5:15]	
f.close()

#Now output updated .sample file
with open(outfile,'w') as outf:
	for k,v in SAMPLES.items():
		outf.write("\t".join(v))
		outf.write("\n")
outf.close()
