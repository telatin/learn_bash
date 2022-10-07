#!/usr/bin/env bash
set -e

VERSION=$(conda --version)
DATADIR="$HOME"/denovo-data/
BOLD=$(tput bold)
RESET=$(tput sgr0)
ENVNAME="denovotut"
CONDA="conda"
if [[ $VERSION == *"conda 4."* ]]; then
    echo "Conda version 4.x detected"
else
    echo "Conda version 4.x not detected"
    exit 1
fi

# Check if mamba is available
if command -v mamba &> /dev/null
then
    $CONDA="mamba"
fi
echo -e "=== ${BOLD}Installing packages for the \"de novo\" tutorial${RESET}"

# check if the environmnet dtp is already present
if [[ -d "$HOME"/miniconda3/envs/$ENVNAME ]]; then
    echo "${BOLD}INFO${RESET}: Environment $ENVNAME already present"
else
    #Installing bioinformatics software using bioconda
    $CONDA create -n ${ENVNAME} -c conda-forge -c bioconda "seqfu>1.10" flye unicycler abricate --yes
fi

#Prepare a folder under HOME USER
echo -e "=== ${BOLD}Downloading datasets${RESET}"
mkdir -p "$DATADIR"


#Download data
# From the paper Klemm et al 2018: https://doi.org/10.1128/mBio.00105-18
for FILE in illumina_1.fastq.gz illumina_2.fastq.gz JUb129_canu1.6.fa nanopore.fastq.gz Salmonella_enterica_subsp_enterica_serovar_Typhi_str_pBL60006_v1.1.fa Salmonella_enterica_subsp_enterica_serovar_Typhi_str_pBL60006_v1.1.gff;
do
  wget --quiet -O "$DATADIR"/${FILE} "ftp://ftp.sanger.ac.uk/pub/project/pathogens/ap13/${FILE}"
  echo " * Downloaded $FILE"
done
echo -e "${BOLD}Done${RESET}"
