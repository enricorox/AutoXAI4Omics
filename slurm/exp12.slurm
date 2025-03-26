#!/bin/bash

#SBATCH --job-name exp12
#SBATCH --output logs/exp12.log
#SBATCH --error logs/exp12.log
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
srun ./autoxai4omics.sh -c exp12.json -m train

