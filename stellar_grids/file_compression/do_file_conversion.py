from glob import glob
import os
from sys import argv
import multiprocessing
import hdf5_io_support as h5_io

def processGYRE(original_gyre_file):
    name_to_save_to = original_gyre_file.split('.GYRE')[0]+'.h5_GYRE'
    rval = h5_io.convert_gyre_input_from_MESA_format(original_gyre_file,name_to_save_to)
    # print('Convert to %s: '%name_to_save_to,rval)
    # print(os.remove(original_gyre_file))
    os.remove(original_gyre_file)

def processProf(original_profile_file):
    name_to_save_to = original_profile_file.split('.prof')[0]+'.h5_prof'
    rval = h5_io.convert_profile_to_hdf5(original_profile_file,name_to_save_to)
    # print('Convert to %s: '%name_to_save_to,rval)
    # print(os.remove(original_profile_file))
    os.remove(original_profile_file)
def processHist(original_history_file):
    name_to_save_to = original_history_file.split('.hist')[0]+'.h5_hist'
    rval = h5_io.convert_history_to_hdf5(original_history_file,name_to_save_to)
    # print('Convert to %s: '%name_to_save_to,rval)
    # print(os.remove(original_history_file))
    os.remove(original_history_file)

path = argv[1]
p = multiprocessing.Pool()
#----------------------------------------------------------------------
#               Convert gyre input files to hdf5
#----------------------------------------------------------------------
# gyre_files = glob(path + '/*/gyre/*.GYRE')
# p.map(processGYRE, gyre_files)
# print('GYRE files converted')
#----------------------------------------------------------------------
#               Convert history file to hdf5
#----------------------------------------------------------------------
history_files = glob(path + '/*/history/*.hist')
p.map(processHist, history_files)
history_files = glob(path + '/*/preMS/*.hist')
p.map(processHist, history_files)
print('History files converted')
#----------------------------------------------------------------------
#               Convert profile files to hdf5
#----------------------------------------------------------------------
profile_files = glob(path + '/*/profiles/*.prof')
p.map(processProf, profile_files)
print('Profile files converted')
