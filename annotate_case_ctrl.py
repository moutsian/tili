#!/usr/bin/python

## Given a case fam file and a ctrl fam file, this simply assigns case/ctrl status to  a fam file from these files that doesn't contain this inormation

import sys, getopt
ctrlfile = ''
casefile = ''
fullfile = ''
DIR = "/lustre/scratch115/projects/crohns/exome/TIH/exomeseq/"
opts, args = getopt.getopt(sys.argv[1:],"h:C:c:f:",["help","case=","ctrl=","filetoannotate="])
for opt, arg in opts:
	if opt == '-h':
		print 'annotate_case_ctrl.py --ctrl <ctrlfile> --case <casefile> -f <filetoannotate>'
		sys.exit()
	elif opt in ("-C", "--case"):
		casefile = DIR+arg
	elif opt in ("-c", "--ctrl"):
		ctrlfile = DIR+arg
	elif opt in ("-f","--filetoannotate"):
		fullfile = DIR+arg	
print 'case file is "', casefile
print 'ctrl file is "', ctrlfile
print 'file to annotate is "',fullfile
#ctrlfile=DIR+"tili.poly.biallelic.v5.gq30.miss10pc.HWEpass.qc2.ctrls.fam"
#casefile=DIR+"tili.poly.biallelic.v5.gq30.miss10pc.HWEpass.qc2.cases.fam"
#fullfile=DIR+"tili.poly.biallelic.v5.gq30.miss10pc.HWEpass.nodiffmiss.qc2.pruned.fam"
outfile =fullfile+".updated"
SAMPLES={}
with open(casefile,'r') as f:
	for line in f.readlines():
		IDcase=line.split()[0]
		SAMPLES[IDcase]=line.split()
f.close()
with open(ctrlfile,'r') as f:
        for line in f.readlines():
                IDctrl=line.split()[0]
                SAMPLES[IDctrl]=line.split()
f.close()

with open(fullfile,'r') as f,  open(outfile,'w') as outf:
        for line in f.readlines():
		ID=line.split()[0]
		if ID in SAMPLES:
	                outf.write(" ".join(SAMPLES[ID]))
			outf.write("\n")
		else:
			outf.write(line)
f.close()
outf.close()
