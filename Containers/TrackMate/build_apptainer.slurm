#!/bin/bash


##SBATCH --job-name=test_Apptainer

#SBATCH -p compute
#SBATCH -A cheme

#SBATCH --nodes=1
#SBATCH --time=0:5:00
#SBATCH --ntasks=1
#SBATCH --mem=10G

#SBATCH --chdir=.

module load apptainer
export APPTAINERENV_NEWHOME=$(pwd)
apptainer build apptainerSif.sif docker://nlsschim/pytrackmate
