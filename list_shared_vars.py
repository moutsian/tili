#!/usr/bin/python

#get two .variants file, and output only shared variants in var\tpos form.
DIR = "/lustre/scratch115/projects/crohns/exome/TIH/exomeseq/"

import sys, getopt, collections
outfile = ''
var1file = ''
var2file = ''
opts, args = getopt.getopt(sys.argv[1:],"h1:2:O:",["help","var1=","var2=","out="])
for opt, arg in opts:
        if opt == '-h':
                print 'list_shared_vars.py --var1 <var1file> --var2 <var2file> --out <outfile>'
                sys.exit()
        elif opt in ("-1", "--var1"):
                var1file = DIR+arg
	elif opt in ("-2", "--var2"):
		var2file = DIR+arg
	elif opt in ("-O", "--out"):
		outfile = DIR+arg
print ' output file is "', outfile,'"' 


chrpos=collections.OrderedDict()
with open(var1file,'r') as f:
	for line in f.readlines():
		chr=line.split()[0];
		pos=line.split()[1];
		chr_pos=chr+"_"+pos
		chrpos[chr_pos]=line.split()[:2]
f.close()

for keys,values in chrpos.items()[:10]:
    print("{}:{}".format(keys,values))

with open(var2file,'r') as f,  open(outfile,'w') as outf:
	for line in f.readlines():
		chr=line.split()[0];
		pos=line.split()[1];
		chr_pos=chr+"_"+pos
		if chr_pos in chrpos:
			outf.write("\t".join(chrpos[chr_pos]))
			outf.write("\n")
outf.close()
f.close()			
