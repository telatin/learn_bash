#!/usr/bin/env bash
set -e

VERSION=$(conda --version)
DATADIR="$HOME"/denovo-data/


if [[ $VERSION == *"conda 4."* ]]; then
    echo "Conda version 4.x detected"
else
    echo "Conda version 4.x not detected"
    exit 1
fi
echo -e " \e[1mInstalling packages for the \"de novo\" tutorial\e[0m"

#Installing bioinformatics software using bioconda
conda create -n dtp -c conda-forge -c bioconda "seqfu>1.10" wtdbg canu abricate unicycler --yes

#Prepare a folder under HOME USER
echo -e " \e[1mDownloading datasets\e[0m"
mkdir -p "$DATADIR"


#Download data
wget -O "$DATADIR"/illumina_1.fastq.gz ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/illumina_1.fastq.gz
wget -O "$DATADIR"/illumina_2.fastq.gz ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/illumina_2.fastq.gz
wget -O "$DATADIR"/JUb129_canu1.6.fa ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/JUb129_canu1.6.fa
wget -O "$DATADIR"/nanopore.fastq.gz ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/nanopore.fastq.gz
wget -O "$DATADIR"/Salmonella_enterica_subsp_enterica_serovar_Typhi_str_pBL60006_v1.1.fa ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/Salmonella_enterica_subsp_enterica_serovar_Typhi_str_pBL60006_v1.1.fa
wget -O "$DATADIR"/Salmonella_enterica_subsp_enterica_serovar_Typhi_str_pBL60006_v1.1.gff ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/Salmonella_enterica_subsp_enterica_serovar_Typhi_str_pBL60006_v1.1.gff
echo -e " \e[1mDone.\e[0m"
