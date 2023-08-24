#!/bin/bash

# make a new csv list of GYRE parameters based on the missing log files

# export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
# export Z_ini= $1
# export M_ini= $2
# export log_Dmix= $3
# export aov= $4
# export fov= $5
# export Xc= $6
# GYRE inlist = $7
# export output_dir= $8


while IFS=, read -r a1 a2 a3 a4 a5 a6 a7 a8

do

export OUTPUT_DIR="${a8}"
export LOG_DIR="${OUTPUT_DIR%/*}"

cd $LOG_DIR

log_file=$LOG_DIR/job_logs/Zini"$a1"_Mini"$a2"_logD"$a3"_aov"$a4"_fov"$a5"_Xc"$a6".log

if [ ! -f "$log_file" ]; then
    echo "$a1,$a2,$a3,$a4,$a5,$a6,$a7,$a8"
    #echo "$log_file not exist"
fi
done < GYRE_parameters.csv >> GYRE_missing_logs.csv
