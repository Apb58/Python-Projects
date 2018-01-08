# Python-Projects

Small Projects or applications written in Python:

1. *PCR Duplicate Remover for SAM files:* Program takes sorted SAM file and several optional arguments and removes all putative PCR duplicates (indicated by matching chromosome, position, strand, and randomer/UMI tag, among reads) and writes new duplicate free file to repo where the SAM file sits. [Requires Python3+]

2. *VCF Surgeon*: Program that allows the user to select a text file with a list of variants (Positions, Ref/Alt, vaf) that they would like to add to a given VCF file, and then creates a new VCF file with the added variant rows for those variants.

3. *Seq Demultiplexer*: Program to demultiplex dual indexed short read sequencing output (fastq format) into library specific read sets, with additional quality and index filtering.

4. *FASTA Dup Remover*: This program finds and removes FASTA reads with duplicate tags in a FASTA file, given a tag to remove (will leave one read of the given tag).

5. *Gene Validator*: Text list comparison script that takes two lists of genes as inputs; compares one list 1 against list 2 (index) to determine if there are any gene names in list 1 that are NOT in list 2.

