#!/bin/bash

#SBATCH -p compute
#SBATCH -A cheme
#SBATCH --nodes=1
#SBATCH --time=1:00:00
#SBATCH --mem=40G

#SBATCH --chdir=.
#SBATCH --ntasks=1
#SBATCH --mem=40G

#SBATCH --signal=USR2
#SBATCH --output=quality_hist_output.log
#SBATCH --error=quality_hist_job_error.log

echo 'sourcing bashrc'
source ~/.bashrc
#load env
echo 'activating diff_suite'
conda activate diff_suite

# Run your command or script
cd /gscratch/cheme/nlsschim/pytrackmate/pytrackmate/Containers/TrackMate
echo 'starting script...'
python quality_histograms.py
echo 'Done running script'