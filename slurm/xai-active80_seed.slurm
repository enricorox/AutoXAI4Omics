#!/bin/bash

#SBATCH --job-name xai-active80-seed
#SBATCH --output logs/xai-active80-seed.log
#SBATCH --error logs/xai-active80-seed.log
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
srun ./autoxai4omics.sh -c active80_seed.json -m train

