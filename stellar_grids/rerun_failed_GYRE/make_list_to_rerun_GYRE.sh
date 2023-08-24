
files=/scratch/leuven/324/vsc32464/extended_convective_penetration/GYRE_out/rot0.4805/job_errs/*.err
for f in $files
do
    ff=${f%.err}.in
    gyre_inlist="/scratch/leuven/324/vsc32464/extended_convective_penetration/GYRE_setup/inlists/rot0.4805_${ff#*job_errs/}"
    gyre_inlist="${gyre_inlist/Mini/M}"
    gyre_inlist="${gyre_inlist/Zini/Z}"
#    echo "run $gyre_inlist"
#    err_file="/scratch/leuven/324/vsc32464/extended_convective_penetration/GYRE_out/rot0.4805/job_errs_retry/${f#*job_errs/}"

    echo $gyre_inlist >> inlist_to_rerun.csv
    
#    echo $gyre_inlist
#    echo $err_file
#    echo $GYRE_DIR/bin/gyre $gyre_inlist '2>>'$err_file '1>>'${err_file%.err}.log >> list_to_rerun
#    find $err_file -type f -size 0 -exec rm {} \;
done
