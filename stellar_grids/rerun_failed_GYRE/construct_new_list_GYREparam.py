import pandas as pd
from foam import support_functions as sf

list_to = pd.read_table('inlist_to_rerun.csv', header=None)

with open('GYRE_parameters.csv', 'r') as f:
    header = f.readline()
    lines = f.readlines()


with open('redo_GYRE_parameters.csv', 'w') as f:
    f.write(header)
    for line in lines:
        inlist = sf.substring(line, '/lustre1/scratch/', ',/lustre1/scratch/')
        if (f'/scratch/leuven/{inlist}' in list_to[0].values):
            f.write(line)
