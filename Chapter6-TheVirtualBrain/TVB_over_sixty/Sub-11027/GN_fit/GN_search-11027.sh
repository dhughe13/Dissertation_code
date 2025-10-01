#!/bin/bash

#SBATCH -N 1
#SBATCH -c 20
#SBATCH -t 1-00:00:00
#SBATCH -p general
#SBATCH -q public
#SBATCH -e slurm.%j.err
#SBATCH --mail-type=ALL
#SBATCH --export=NONE

#load required modules
module load mamba/latest
source activate tvb_env

#run commands
~/.conda/envs/tvb_env/bin/python GN_search-11027.py
