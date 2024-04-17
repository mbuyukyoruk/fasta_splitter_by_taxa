import argparse
import re
import sys
import subprocess
import os
import textwrap

try:
    from tqdm import tqdm
except:
    print("tqdm module is not installed! Please install tqdm and try again.")
    sys.exit()

try:
    from Bio import SeqIO
except:
    print("SeqIO module is not installed! Please install SeqIO and try again.")
    sys.exit()

parser = argparse.ArgumentParser(prog='python fasta_splitter_by_taxa.py',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=textwrap.dedent('''\

    Author: Murat Buyukyoruk
    Associated lab: Wiedenheft lab

        fasta_splitter_by_taxa help:

This script is developed to split sequences based on taxonomy information that is provided separately.

        Accession   Name                    Kingdom     Phylum
        CH902601.1  Vibrio angustum S14     Bacteria    Gammaproteobacteria
        CP000117.1  Anabaena variabilis     Bacteria    Cyanobacteriota

SeqIO package from Bio is required to fetch flank sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.
        
Syntax:

        python fasta_splitter_by_taxa.py -i demo.fasta -l taxa_list.txt

fasta_splitter_by_taxa dependencies:

Bio module and SeqIO available in this package          refer to https://biopython.org/wiki/Download

tqdm                                                    refer to https://pypi.org/project/tqdm/
	
Input Paramaters (REQUIRED):
----------------------------
	-i/--input		FASTA			Specify a fasta file.

	-l/--list		Number			Specify a list of accessions and associated taxonomy name.

Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.
	
      	'''))
parser.add_argument('-i', '--input', required=True, type=str, dest='filename', help='Specify a fastafile.\n')
parser.add_argument('-l', '--list', required=True, type=str, dest='taxa', help='Specify taxonomy file.\n')

results = parser.parse_args()
filename = results.filename
taxa = results.taxa

proc = subprocess.Popen("grep -c '>' " + filename, shell=True, stdout=subprocess.PIPE, text=True)
length = int(proc.communicate()[0].split('\n')[0])

try:
    os.mkdir("originals")
except:
    pass

with tqdm(range(length)) as pbar:
    pbar.set_description('Splitting...')
    for record in SeqIO.parse(filename, "fasta"):
        pbar.update()
        acc = record.id.rsplit('_',2)[0]
        try:
            proc = subprocess.Popen("grep '" + acc + "' " + taxa, shell=True, stdout=subprocess.PIPE, text=True)
            info = str(proc.communicate()[0].split('\n')[0])

            kingdom = info.split('\t')[2]

            if info.split('\t')[3] == "Proteobacteria":
                phylum = info.split('\t')[4].split('\n')[0].replace(" ","")
            else:
                phylum = info.split('\t')[3].replace(" ","")

            out = filename.split(".fasta")[0] + "_" + phylum + ".fasta"
            f = open(out, 'a')
            sys.stdout = f

            print(">" + record.description + " | " + kingdom + " | " + phylum)
            print(re.sub("(.{60})", "\\1\n", str(record.seq), 0, re.DOTALL))

        except:

            out = filename.split(".fasta")[0] + "_NA.fasta"
            # print out
            f = open(out, 'a')
            sys.stdout = f

            print(">" + record.description + " | NA | NA")
            print(re.sub("(.{60})", "\\1\n", str(record.seq), 0, re.DOTALL))

os.system("mv " + filename + " originals")
