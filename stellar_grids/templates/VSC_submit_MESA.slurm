#!/bin/bash
#SBATCH --cluster=wice
#SBATCH --job−name='mesa_grid'
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=72
#SBATCH --partition=batch_long
#SBATCH --time='7-00:00:00'
#SBATCH --account=XXXX
#SBATCH --mail-type ='BEGIN,END,FAIL,TIME_LIMIT'
#SBATCH --mail-user='XXXXX.XXXXX@kuleuven.be'

module purge
source $VSC_HOME/.bashrc
export OMP_NUM_THREADS=1

bash run_MESA.sh $Zini $Mini $logD $aov $fov $output_dir $MESA_work_dir

# This script is submitted to the cluster with the following commands
# module use /apps/leuven/skylake/2021a/modules/all
# module load worker/1.6.12-foss-2021a-wice
# wsub -data MESA_parameters.csv -batch submit_MESA.slurm

# Adjust the #SBATCH settings at the top of this file (email, nodes, walltime, etc.) according to your needs.
