#!/bin/bash

#SBATCH --job-name exp13
#SBATCH --output logs/exp13.log
#SBATCH --error logs/exp13.log
#SBATCH --mail-user enrico.rossignolo@studenti.unipd.it
#SBATCH --mail-type ALL
#SBATCH --time 14-00:00:00
#SBATCH --ntasks 1
#SBATCH --cpus-per-task=16
#SBATCH --partition allgroups
#SBATCH --mem 200G

set -e

cd ..

echo "### TRAINING ###"
srun ./autoxai4omics.sh -c exp13.json -m train

