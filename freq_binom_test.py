#!/usr/bin/python

#get counts (AC) from the control file, then the frequency from gnomAD NFE population,
#end check for deviations of the counts using a binomial test.
DIR = "/lustre/scratch115/projects/crohns/exome/TIH/exomeseq/"

import re,sys, getopt, collections
from scipy.stats import binom_test
outfile = ''
varfile = ''
annotfile = ''
opts, args = getopt.getopt(sys.argv[1:],"hV:A:O:",["help","var=","ann=","out="])
for opt, arg in opts:
	if opt == '-h':
		print 'list_shared_vars.py --var <varfile> --ann <annotfile> --out <outfile>'
		sys.exit()
	elif opt in ("-1", "--var"):
		varfile = DIR+arg
	elif opt in ("-2", "--ann"):
		annotfile = DIR+arg
	elif opt in ("-O", "--out"):
		outfile = DIR+arg
print ' output file is "', outfile,'"' 

chrpos=collections.OrderedDict()
p2 = re.compile(r'gnomAD_NFE_AF=([(0-9|e)\.]+);') #for the frequency in float format
p3 = re.compile(r'gnomAD_NFE_AF=([+\-]?[^A-Za-z]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+));') #for the frequency in scientific format
p4 = re.compile(r'AC=([(0-9)\.]+);') #for the allele counts 
p5 = re.compile(r'AN=([(0-9)\.]+);') #or the total allele number
#first open the annot file and start from it
with open(annotfile,'r') as f:
	for line in f.readlines():
		if not line.startswith("#"):
			chr_pos=line.split()[1];
			if not chr_pos in chrpos:
				chrpos[chr_pos]=line.split()
				gnomad_freq_sci=p3.search(line.split()[13])
				gnomad_freq=p2.search(line.split()[13])
				if (gnomad_freq is None) and (gnomad_freq_sci is None): #if there is no gnomAD frequency input in the annot file
					chrpos[chr_pos]+="999"
				elif gnomad_freq is None:
                                        chrpos[chr_pos]+=gnomad_freq_sci.groups()
				else:
					chrpos[chr_pos]+=gnomad_freq.groups()
f.close()

with open(varfile,'r') as f, open(outfile,'w') as outf:
	#header
	outf.write("chr\tpos\trsID\tAC\tAN\tgonmAD_NFE_freq\tpval_binom\n")
	for line in f.readlines():
		chr_pos=line.split()[0]+":"+line.split()[1]
		AC=p4.search(line)
		AN=p5.search(line)
		if chr_pos in chrpos and float(chrpos[chr_pos][-1])<=1:
			print("{},{},{},AC:{},AN:{},gnomad_freq:{}\n".format(line.split()[0],line.split()[1],line.split()[2],AC.groups()[0],AN.groups()[0],chrpos[chr_pos][-1]))
			pval=binom_test(float(AC.groups()[0]),float(AN.groups()[0]),float(chrpos[chr_pos][-1]))
			print("pval:{}".format(pval))
			outf.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(line.split()[0],line.split()[1],line.split()[2],AC.groups()[0],AN.groups()[0],chrpos[chr_pos][-1],pval))
		else:
			#just print as is ?
			outf.write("{}\t{}\t{}\t{}\t{}\tNA\tvariant_not_in_gnomAD\n".format(line.split()[0],line.split()[1],line.split()[2],AC.groups()[0],AN.groups()[0]))
outf.close()
f.close()

for keys,values in chrpos.items()[:10]:
    print("{}:{}".format(keys,values))

