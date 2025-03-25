#!/bin/bash

#SBATCH --job-name xai-active80
#SBATCH --output logs/xai-active80.log
#SBATCH --error logs/xai-active80.log
#SBATCH --mail-user enrico.rossignolo@studenti.unipd.it
#SBATCH --mail-type ALL
#SBATCH --time 14-00:00:00
#SBATCH --ntasks 1
#SBATCH --cpus-per-task=16
#SBATCH --partition allgroups
#SBATCH --mem 20G

set -e

cd ..

echo "### TRAINING ###"
srun ./autoxai4omics.sh -c 80active_SHAP_best500_seed.json -m train

