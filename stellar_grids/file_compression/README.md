How to package a gird of models for convenient transfer and storage.

1) Convert history and profile files to hdf5 format by using the `do_file_conversion.py` script, placing this script in your MESA_out folder. (One level above the history, profiles, gyre, preMS folders.)
Submit this on the vsc to a node using `sbatch compress_files.pbs` using an adjusted version of that pbs file.

2) compress all the individual files to tarballs using the `create_tar_MESA.py` and `create_tar_GYRE.py` scripts.
Submit this on the vsc to a node using `sbatch tar_files.pbs` using an adjusted version of that pbs file.

3) Archive the whole subdirectories uncompressed (so just archiving), so that it can be more easily transferred.
The command do do this is: `tar -cf myfolder.tar myfolder`
(Zip the gyre, profiles, and history subdirectories separately if they are large)


4) Once transferred, the files can be extracted from their archived and compressed format by using the scripts `untar_MESA.py` and `untar_GYRE.py`.
