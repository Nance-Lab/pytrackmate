#!/bin/bash

##SBATCH --job-name-Apptainer
#SBATCH -p compute
#SBATCH -A cheme
#SBATCH --nodes=1
#SBATCH --time=10:00:00

#SBATCH --chdir=.
#SBATCH --ntasks=8
#SBATCH --mem=150G

#SBATCH --signal=USR2
#SBATCH --output=output.log
#SBATCH --error=job_error.log
module load apptainer
export APPTAINERENV_NEWHOME=$(pwd)
apptainer run --bind /gscratch --cleanenv apptainerSif.sif

exit 0
