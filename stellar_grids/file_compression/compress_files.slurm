#!/bin/bash
#SBATCH --cluster=wice
#SBATCH --job−name='FileConversion'
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=72
#SBATCH --time='24:00:00'
#SBATCH --account=XXXX
#SBATCH --mail-type ='BEGIN,END,FAIL,TIME_LIMIT'
#SBATCH --mail-user='XXXXX.XXXXX@kuleuven.be'


module purge
source $VSC_HOME/.bashrc

# Export your python path here, e.g.
# export PATH="/data/leuven/324/vsc32464/Software/miniconda3/bin:$PATH"

python do_file_conversion.py .
