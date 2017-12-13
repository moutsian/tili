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

#chrpos=collections.OrderedDict()
p2 = re.compile(r'gnomAD_NFE_AF=([(0-9|e)\.]+);') #for the frequency in float format
p3 = re.compile(r'gnomAD_NFE_AF=([+\-]?[^A-Za-z]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+));') #for the frequency in scientific format
p4 = re.compile(r'AC=([(0-9)\.]+);') #for the allele counts 
p5 = re.compile(r'AN=([(0-9)\.]+);') #or the total allele number
p6 = re.compile(r'EUR_AF=([(0-9|e)\.]+);') #for the 1KG frequency in float format
p7 = re.compile(r'EUR_AF=([+\-]?[^A-Za-z]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+));') #for the 1KG frequency in scientific format


#first open the variants file:
var_chrpos=collections.OrderedDict()
with open(varfile,'r') as f:
	for line in f.readlines():
		chr_pos=line.split()[0]+":"+line.split()[1]
		AC=p4.search(line)
		AN=p5.search(line)
		if not chr_pos in var_chrpos:
			var_chrpos[chr_pos]=[line.split()[:3]]
			var_chrpos[chr_pos].append(AC.groups()[0])
			var_chrpos[chr_pos].append(AN.groups()[0])
f.close()

for keys,values in var_chrpos.items()[:10]:
	print("{}:{}".format(keys,values))

#now open the annot file and the output file and start the calculation of the binomial test
chrpos=[]
with open(annotfile,'r') as f, open(outfile,'w') as outf:
	#header
	outf.write("chr\tpos\trsID\tAC\tAN\tgnomAD_NFE_freq\tEUR1KG_freq\tpval_binom_with_gnomAD\tpval_binom_with_EUR1KG\n")
	for line in f.readlines():
		if not line.startswith("#"):
			chr_pos=line.split()[1];
			if not chr_pos in chrpos: #this is because the .annot file contains many entries per variant (one per transcript)
				chrpos.append(chr_pos)
				gnomad_freq_sci=p3.search(line.split()[13])
				gnomad_freq=p2.search(line.split()[13])
				freq1KG=p6.search(line.split()[13])
				freq1KGsci=p7.search(line.split()[13])
				#now get gnomAD freq in the right form
				if (gnomad_freq is None) and (gnomad_freq_sci is None): #if there is no gnomAD frequency input in the annot file
					gnfreq="NA"
				elif gnomad_freq is None:
					gnfreq=gnomad_freq_sci.groups()[0]
				else:
					gnfreq=gnomad_freq.groups()[0]
				#same for 1KG
				if (freq1KG is None) and (freq1KGsci is None): #if there is no 1KG frequency input in the annot file
					freq1000g="NA"
				elif freq1KG is None:
					freq1000g=freq1KGsci.groups()[0]
				else:
					freq1000g=freq1KG.groups()[0]
				#now get output
				if chr_pos in var_chrpos:
					outf.write("{}\t{}\t{}\t{}\t{}\t".format(var_chrpos[chr_pos][0][0],var_chrpos[chr_pos][0][1],var_chrpos[chr_pos][0][2],var_chrpos[chr_pos][1],var_chrpos[chr_pos][2])) #chr pos rsID AC AN
					if gnfreq=="NA": #variant in ctrls and not in gnomAD
						pval_gn="variant_not_in_gnomAD"
					else: #variant in ctrls and in gnomAD
						pval_gn=binom_test(float(var_chrpos[chr_pos][1]),float(var_chrpos[chr_pos][2]),float(gnfreq))
					if freq1000g=="NA": #variant in ctrls and not in gnomAD
						pval_1KG="variant_not_in_1KG"
					else: #variant in ctrls and in gnomAD
						pval_1KG=binom_test(float(var_chrpos[chr_pos][1]),float(var_chrpos[chr_pos][2]),float(freq1000g))
					outf.write("{}\t{}\t{}\t{}\n".format(gnfreq,freq1000g,pval_gn,pval_1KG)) 
				elif gnfreq!="NA": #variant not in ctrls but in gnomAD - here I will use a fixed AN of 982 which in reality is not always the case (due to missingness) but should have minor impact.
					pval_gn=binom_test(0,982,float(gnfreq))
					if freq1000g!="NA":
						pval_1KG=binom_test(0,982,float(freq1000g))
					else:
						pval_1KG="variant_not_in_1KG"
					outf.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(line.split()[1].split(':')[0],line.split()[1].split(':')[1],line.split()[0],0,"982*",gnfreq,freq1000g,pval_gn,pval_1KG))
				else: #variant not in ctrls and not in gnomAD (probably present in cases)
					pval_gn="variant_not_in_gnomAD_and_not_in_ctrls"
					if freq1000g!="NA":
						pval_1KG=binom_test(0,982,float(freq1000g))
					else:
						pval_1KG="variant_not_in_1KG"
					outf.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(line.split()[1].split(':')[0],line.split()[1].split(':')[1],line.split()[0],0,"982*",0,freq1000g,pval_gn,pval_1KG))
f.close()

