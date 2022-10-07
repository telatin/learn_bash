#!/usr/bin/env python3
"""
reads fasta file(s) and creates a database in the hashsum format
The fasta file(s) must be one locus per line. The first allele is the assumed reference.
Each sequence ID must have the format locus_allele.
Input:
Fasta file
Output:
- A reference fasta file
- A TSV file with all the alleles
"""

import sys
import os
import argparse

def translate(seq):
    # From: https://www.geeksforgeeks.org/dna-protein-python-3/
    stop = '*'
    table = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',                 
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA': stop, 'TAG': stop,
        'TGC':'C', 'TGT':'C', 'TGA': stop, 'TGG':'W',
    }
    protein =""
    
    for i in range(0, len(seq), 3):
        codon = seq[i:i + 3]
        if len(codon) != 3:
            return protein
        protein+= table[codon]
    return protein

def read_fasta(path):
    # FASTA name/seq/comment iterator
    if path.endswith('.gz'):  
        import gzip      
        fasta = gzip.open(path, 'rt')
    else:
        fasta = open(path, 'rt')
    name = None
    comment = ''
        
    for line in fasta:
        if line.startswith('>'):
            if name is not None:
                yield name, seq, comment
            nameparts = line[1:].rstrip().split()
            name = nameparts[0]
            comment = ' '.join(nameparts[1:]) if len(nameparts) > 1 else ''
            seq = ''
        else:
            seq += line.rstrip()
    yield name, seq, comment
 
def main():
    args = argparse.ArgumentParser()
    args.add_argument("FASTA", help="Fasta file(s) with alleles having name as locus_id", nargs="+")
    args.add_argument("-o", "--out", help="Output file")
    args.add_argument("--verbose", help="Print verbose information", action="store_true")
    args = args.parse_args()

    if args.out is None:
        output = sys.stdout
    else:
        output = open(args.out, 'wt')
    

    # Precheck all input files exist
    for fastafile in args.FASTA:
        if not os.path.exists(fastafile):
            raise ValueError("ERROR: File %s does not exist" % fastafile)
    
    for fastafile in args.FASTA:
        for name, seq, comment in read_fasta(fastafile):
            print(translate(seq), " len=%s" % len(seq))


if __name__ == "__main__":
    quit(main())