#!/bin/bash

#SBATCH -N 1
#SBATCH -c 23
#SBATCH -t 0-04:00:00
#SBATCH -p general
#SBATCH -q public
#SBATCH -e slurm.%j.err
#SBATCH --mail-type=ALL
#SBATCH --export=NONE

#clear all previously loaded modules
#module purge

#load required modules
module load mamba/latest
source activate tvb_env

#conda info --env

#run commands
#python GN_search-10009.py
~/.conda/envs/tvb_env/bin/python Ji_search-10009.py