# remove GYRE error files that contain the following warning

find . | xargs grep -l "WARNING: Discarding imaginary part of atmospheric radial wavenumber" | awk '{print "rm "$1}' > list_remove.sh
#vi list_remove.sh // check for murphy and his law
#source list_remove.sh #run this to run the remove list
