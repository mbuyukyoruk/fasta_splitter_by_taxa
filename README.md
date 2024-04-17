# fasta_splitter_by_taxa

Author: Murat Buyukyoruk

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
	
