#!/usr/bin/env bash
set -e

echo -e " \e[1mInstalling packages for the \"de novo\" tutorial\e[0m"

#Installing bioinformatics software using bioconda
conda create -n dtp -c conda-forge -c bioconda tiptoft wtdbg assembly-stats canu abricate unicycler --yes
#Prepare a folder under HOME USER
echo -e " \e[1mDownloading datasets\e[0m"
mkdir -p $HOME/data
cd $HOME/data
#Download data
wget ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/illumina_1.fastq.gz
wget ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/illumina_2.fastq.gz
wget ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/JUb129_canu1.6.fa
wget ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/nanopore.fastq.gz
wget ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/Salmonella_enterica_subsp_enterica_serovar_Typhi_str_pBL60006_v1.1.fa
wget ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/Salmonella_enterica_subsp_enterica_serovar_Typhi_str_pBL60006_v1.1.gff
echo -e " \e[1mDone.\e[0m"
