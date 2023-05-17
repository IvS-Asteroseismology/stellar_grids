"""A few helpful functions to process MESA output."""
# from foam import functions_for_mesa as ffm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import h5py
from stellar_grids import support_functions as sf

################################################################################
def read_mesa_file(file_path, index_col=None):
    """
    Read in a mesa profile or history file and return 2 dictionaries.
    The first with the header info, and the second with the data.
    If the format is hdf5, assumes the attributes are the MESA header.
    If the format is not an hdf5 file, assumes the default MESA output format.
    This format is an ascii file delimited by whitespace with the following structure:
    line 1: header names
    line 2: header data
    line 3: blank
    line 4: main data names
    line >4:main data values

    ------- Parameters -------
    file_path: String
        The path to the MESA profile or history file to read in.
    ------- Returns -------
    header: dictionary
        A dictionary holding the header info of the MESA file.
    data: dictionary
        A dictionary holding the data columns of the MESA file as numpy arrays.
    """
    if h5py.is_hdf5(file_path):
        return sf.read_hdf5(file_path)

    else:   # assumes the default MESA output format
        header_df = pd.read_table(file_path, delim_whitespace=True, nrows=1, header=1)
        data_df = pd.read_table(file_path, delim_whitespace=True, skiprows=3, header=1, index_col=index_col)

        header={}
        for k in header_df.keys():
            header.update({k: header_df[k].to_numpy()[0]})
        data = {}
        for k in data_df.keys():
            data.update({k: data_df[k].to_numpy()})

        return header, data

################################################################################
def check_hydro_eq(profile_file, treshold_for_plot=5E-8):
    """
    Calculates the normalised differences between the terms on both sides of the hydrostatic equilibrium equation.
    Makes a plot if the values exceed a given treshold.
    This shows how well hydrostatic equilibrium has been fulfilled in the MESA model.
    ------- Parameters -------
    profile_file: String
        The path to the profile file to be checked.
    treshold_for_plot: float
        Make a plot if the max difference between the left and right hand side of the equation is greater than this number.
    """
    header, data = read_mesa_file(profile_file)
    # Compute the hydrostatic equilibrium quality factor q - See e.g. Aerts et al. (2010)
    lhs=np.delete(data['hyeq_lhs'], 0)  # remove the values at the surface, since these are 0
    rhs=np.delete(data['hyeq_rhs'], 0)

    norm = np.max(np.vstack([lhs, rhs]), axis=0)
    hyeq = np.abs(lhs - rhs) / np.abs(norm)

    # Make the plot if the treshold criterion is met
    if max(hyeq) > treshold_for_plot:
        # print the maximal deviation and profile name
        print(max(hyeq))
        print(profile_file)
        # make a semilog plot
        fig=plt.figure()
        ax = fig.add_subplot(111)
        ax.semilogy(np.delete(data['radius'], 0), hyeq, 'ko-') #also remove surface value, to have same amount of datapoints
        plt.show()
        plt.clf()
        plt.close('all')

################################################################################
def calculate_number_densities(hist_file):
    '''
    Calculate surface number densities for all isotopes in the MESA grid.
    All isotopes in the used nuclear network need to be be written in the history file,
    otherwise this will function give wrong numbers.
    ------- Parameters -------
    hist_file: String
        The path to the MESA history file.
    ------- Returns -------
    number_densities: dictionary
        Column keys specify the element (surf_X_per_N_tot), values are number densities of that element.
    '''
    header, data = read_mesa_file(hist_file)
    element_list = {}
    number_densities = {}
    inverse_average_atomic_mass = np.zeros(len(data[ list(data.keys())[0] ]))
    for column_name in data.keys():
        if '_per_Mass_tot' in column_name:
            element_list.update({column_name: data[column_name]})
            inverse_average_atomic_mass += data[column_name]

    average_atomic_mass = inverse_average_atomic_mass**(-1)
    for key in element_list.keys():
        number_densities.update({ key.replace('_per_Mass_tot', '_per_N_tot') : element_list[key]*average_atomic_mass})

    return number_densities
