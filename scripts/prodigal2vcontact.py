#!/usr/bin/env python3
"""
Use the FASTA output from Prodigal to create a VContact file
protein to genome mapping
"""

import argparse
import sys
"""
>k141_2513||full_1 # 1 # 264 # -1 # ID=1_1;partial=10;start_type=ATG;rbs_motif=None;rbs_spacer=None;gc_cont=0.402
MQKIEKQIKIQEKLKDEMQKKCAKEGTEFDESKFESGIPIESLEMFENIAFLMHKHGDPD
QPDDINEWLDQFETFDIYEILPEIMEMW
>k141_2513||full_2 # 381 # 917 # -1 # ID=1_2;partial=01;start_type=Edge;rbs_motif=None;rbs_spacer=None;gc_cont=0.447
LQESDTGEITFDTPFAVPGSVSLSLEAQGELTPFYADGIKYYVSSSNSGYEGDWEMALIT
DEFREKILSEYIDKNKVMLEEATAKVKRFALGFEIDGDVRGTRFWFYCCTSTRPTTESST
TEDAIEPTTDTVTVSASAVQLGTAKKMAVRAKTTADTTDDLYEKWFDKVYIPDQEVAA*
>k141_636||full_1 # 1 # 573 # 1 # ID=2_1;partial=10;start_type=Edge;rbs_motif=None;rbs_spacer=None;gc_cont=0.478
DRKTFARLDRLAKSNNVSKKDFLSCALEYFEKYGINPVEHESPAKEMQKLIKRCDQVIAF
IRKQEQDFLRPACEAMGSTSMRVTMSMDSILTEKKFSQYQKDNDLFMRDLASLAGIREQA
"""

def read_fasta(path):
    import gzip
    seqName = None
    seqComment = None
    with (gzip.open if path.endswith('.gz') else open)(path, 'rt') as fasta:
        for line in fasta:
            if line.startswith('>'):
                if seqName is not None:
                    yield seqName, seqComment, sequence
                seqName = line[1:].split()[0]
                seqComment = line[1:].split()[1:] if len(line[1:].split()) > 1 else ""
                sequence = ""
                
            else:
                sequence += line.strip()
    yield seqName, seqComment, sequence
if __name__ == "__main__":
    args = argparse.ArgumentParser("Create a VContact file from Prodigal output")
    args.add_argument("FASTA", help="FASTA file")
    args.add_argument("-o", "--output", help="VContact mapping file")
    args = args.parse_args()

    outfh = open(args.output, 'w') if args.output else sys.stdout
    print("protein_id,contig_id,keywords", file=outfh)

    for name, comment, seq in read_fasta(args.FASTA):
        if '||' not in name:
            raise ValueError("FASTA file does not appear to be from Prodigal")
        contig = name.split("||")[0]
        print("{},{},{}".format(name, contig, ""), file=outfh)


        