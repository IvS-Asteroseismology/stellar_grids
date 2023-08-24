export OMP_NUM_THREADS=1

while IFS=, read -r a1 a2 a3 a4 a5 a6 a7 a8
do
bash run_GYRE.sh $a1 $a2 $a3 $a4 $a5 $a6 $a7 $a8

done < redo_GYRE_parameters.csv
