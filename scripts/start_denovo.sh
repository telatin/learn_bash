#!/usr/bin/env bash
set -e

CONDA_VERSION=$(conda --version)
DATADIR="$HOME"/denovo-data/
BOLD=$(tput bold)
RESET=$(tput sgr0)
ENVNAME="denovotut"
CONDA="conda"

if [[ ! -z ${1+x} ]]; then
    if [[ $CONDA_VERSION == *"conda 4."* ]]; then
        echo "[INFO] Conda version 4.x detected"
    else
        CONDA="notfound"
    fi

    # Check if mamba is available
    if command -v mamba &> /dev/null
    then
        echo "[INFO] Mamba is also available!"
        CONDA="mamba"
    fi

    if [[ $CONDA == "notfound" ]]; then
        echo "ERROR: conda/mamba not found"
        exit 1
    fi

    # check if the environmnet dtp is already present
    ENV_FOUND=$($CONDA info --envs | grep $ENVNAME | wc -l)
    if [[ $ENV_FOUND == *"0"* ]]; then
        echo -e "=== ${BOLD}Installing packages for the \"de novo\" tutorial${RESET}"
        $CONDA create -n $ENVNAME -c conda-forge -c bioconda --quiet  --yes "seqfu>1.12" "flye" "fastp" "unicycler" "skesa" "abricate" 
    fi
else
    echo "Conda environment will not be created"
    echo 'Try: conda create -n denovo -c conda-forge -c bioconda "seqfu>1.12" "flye" "fastp" "unicycler" "skesa" "abricate" '
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
