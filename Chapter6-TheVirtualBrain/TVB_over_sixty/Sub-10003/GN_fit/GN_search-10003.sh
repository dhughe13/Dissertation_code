#!/bin/bash

#SBATCH -N 1
#SBATCH -c 20
#SBATCH -t 1-00:00:00
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
#python GN_search-10003.py
~/.conda/envs/tvb_env/bin/python GN_search-10003.py
