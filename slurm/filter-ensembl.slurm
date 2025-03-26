#!/bin/bash

#SBATCH --job-name filter-ensembl
#SBATCH --output logs/filter-ensembl.log
#SBATCH --error logs/filter-ensembl.log
#SBATCH --mail-user enrico.rossignolo@studenti.unipd.it
#SBATCH --mail-type ALL
#SBATCH --time 14-00:00:00
#SBATCH --ntasks 1
#SBATCH --cpus-per-task=1
#SBATCH --partition allgroups
#SBATCH --mem 40G

set -e

cd /nfsd/bcb/bcbg/rossigno/PNRR/AutoXAI4Omics/data

srun grep -F -f filter-ensembl.txt /nfsd/bcb/bcbg/EleonoraSignor/AutoXAI4Omics/data/features_data.csv > filtered.csv

srun cat header.csv filtered.csv > features_data_ensembl.csv
