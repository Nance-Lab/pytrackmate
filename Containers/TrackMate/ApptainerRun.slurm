#!/bin/bash


##SBATCH --job-name=test_Apptainer

#SBATCH -p compute
#SBATCH -A cheme

#SBATCH --nodes=8
#SBATCH --time=28:00:00
#SBATCH --ntasks=1
#SBATCH --mem=40G

#SBATCH --chdir=.

module load apptainer
export APPTAINERENV_NEWHOME=$(pwd)
apptainer run pytrackmate_latest.sif

exit 0