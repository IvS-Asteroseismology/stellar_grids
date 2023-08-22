"""Helpful functions in general. Making figures, reading HDF5, processing strings."""
import h5py, re, pkgutil, sys, glob
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from io import StringIO
from stellar_grids import functions_for_mesa as ffm

logger = logging.getLogger('logger.sf')
################################################################################
def split_line(line, sep) :
    """
    Splits a string in 2 parts.

    ------- Parameters -------
    line: string
        String to split in 2.
    sep: string
        Separator where the string has to be split around.

    ------- Returns -------
    head: string
        Part 1 of the string before the separator.
    tail: string
        Part 2 of the string after the separator.
    """
    head, sep_, tail = line.partition(sep)
    assert sep_ == sep
    return head, tail

################################################################################
def substring(line, sep_first, sep_second) :
    """
    Get part of a string between 2 specified separators.
    If second separator is not found, return everyting after first separator.

    ------- Parameters -------
    line: string
        String to get substring from.
    sep_first: string
        First separator after which the returned substring should start.
    sep_first: string
        Second separator at which the returned substring should end.

    ------- Returns -------
    head: string
        Part of the string between the 2 separators.
    """
    head, tail = split_line(line, sep = sep_first)
    if sep_second not in tail:
        return tail
    head, tail = split_line(tail, sep =sep_second)
    return head
################################################################################
def get_param_from_filename(file_path, parameters, values_as_float=False):
    """
    Get parameters from filename

    ------- Parameters -------
    file_path : string
        Full path to the file
    parameters: list of Strings
        Names of parameters to extract from filename

    ------- Returns -------
    param_dict: Dictionary
        Keys are strings describing the parameter, values are strings giving corresponding parameter values
    """

    param_dict = {}
    for parameter in parameters:
        try:
            p = substring(Path(file_path).stem, parameter, '_')
            if values_as_float:
                p = float(p)
            param_dict[parameter] = p
        except:
            param_dict[parameter] = '0'
            logger.info(f'In get_param_from_filename: parameter "{parameter}" not found in \'{file_path}\', value set to zero')

    return param_dict

################################################################################
def read_hdf5(filename):
    """
    Read a HDF5-format file (e.g. GYRE)

    ------- Parameters -------
    filename : string
        Input file

    ------- Returns -------
    attributes: dictionary
        Dictionary containing the attributes of the file.
    data: dictionary
        Dictionary containing the data from the file as numpy arrays.
    """
    # Open the file
    with h5py.File(filename, 'r') as file:
        # Read attributes
        attributes = dict(zip(file.attrs.keys(),file.attrs.values()))
        # Read datasets
        data = {}
        for k in file.keys() :
            data[k] = file[k][...]
    return attributes, data
################################################################################
def convert_units(quantity, input, convertto='cgs'):
    '''
    Converts from solar units to cgs and vice versa.
    ------- Parameters -------
    input: list of float
        Numbers to convert.
    quantity: string
        The quantity you want to convert. Options are: {radius, mass, luminosity}.
    convertto: string
        The unit system to convert to. Options are: {cgs,solar} with default: 'cgs'.
    ------- Returns -------
    out: list of float
        converted numbers
    '''
    # conversion factors used in MESA see $MESA_DIR/const/public/const_def.f90
    to_cgs = {'mass': 1.9892E33,
              'luminosity': 3.8418E33,
              'radius': 6.9598E10,
              'cgrav': 6.67428E-8} # gravitational constant (g^-1 cm^3 s^-2)

    # convert to cgs
    if convertto == 'cgs':
        return input * to_cgs[quantity]
    # convert to solar units
    elif convertto == 'solar':
        return input / to_cgs[quantity]
################################################################################
def ledoux_splitting(frequencies, betas, Mstar, Rstar, omega=0, m=1):
    """
    Calculate rotationally shifted frequencies in a perturbative way. (See Aerts et al. (2010), eq 3.357)
    ------- Parameters -------
    frequencies, betas: numpy array of floats
        frequency values (c/d) and beta values (eq 3.357, Aerts et al. (2010))
    Mstar, Rstar, omega: float
        stellar mass (g), radius (cm) and rotation frequency in units of critical velocity (omega_crit^-1)
    m: int
        azimuthal order

    ------- Returns -------
    shifted_freqs: numpy array of floats
        pulsation frequency values, shifted by the Ledoux splitting
    """

    G = 6.67428E-8 # gravitational constant (g^-1 cm^3 s^-2)
    omega_crit = (1/(2*np.pi))*(8*G*Mstar/(27*Rstar**3))**0.5 # Roche critical rotation frequency (s^-1)
    omega_cycday = omega*omega_crit*86400 # rotation frequency in units of c/d

    shifted_freqs = frequencies-(m*omega_cycday*(1-betas)) # shifted frequencies in units of c/d
    return shifted_freqs

################################################################################
def calc_scanning_range(gyre_file_path, npg_min=-50, npg_max=-1, l=1, m=1, omega_rot=0.0, unit_rot = 'CYC_PER_DAY', rotation_frame='INERTIAL'):
    """
    Calculate the frequency range for the sought radial orders of the g modes.
    ------- Parameters -------
    gyre_file_path: string
        absolute path to the gyre file that needs to be scanned
    n_min, n_max: integer
        lower and upper values of the required range in radial order
    l, m: integer
        degree (l) and azimuthal order (m) of the modes
    omega_rot: float
        rotation frequency of the model
    unit_rot: string
        unit of the rotation frequency, can be CYC_PER_DAY or CRITICAL (roche critical)
    rotation_frame: string
        rotational frame of reference for the pulsation freqencies

    ------- Returns -------
    f_min, f_max: float
        lower and upper bound of frequency range that needs to be scanned in oder
        to retrieve the required range of radial orders
    """
    directory, gyre_file = split_line(gyre_file_path, 'gyre/') # get directory name and GYRE filename
    Xc_file = float(substring(gyre_file, 'Xc', '.GYRE'))       # get Xc
    MESA_hist_name, tail = split_line(gyre_file, '_Xc')        # Get the MESA history name form the GYRE filename
    hist_file = glob.glob(f'{directory}history/{MESA_hist_name}.*hist')[0]   # selects MESA history file (.hist or .h5_hist) corresponding to the GYRE file

    header, data  = ffm.read_mesa_file(hist_file)
    Xc_values = np.asarray(data['center_h1'])
    P0_values = np.asarray(data['Asymptotic_dP'])

    # Obtain the asymptotic period spacing value/buoyancy radius at the Xc value closest to that of the gyre file
    diff = abs(Xc_file - Xc_values)
    xc_index = np.where(diff == np.min(diff))[0]
    P0 = P0_values[xc_index][0]/86400 # asymptotic period spacing value/buoyancy radius, /86400 to go from sec to day

    # Calculate the scanning range a bit broader than the purely asymptotic values, just to be safe.
    n_max_used = abs(npg_min-3)
    n_min_used = abs(min(-1, npg_max+3))

    if omega_rot==0:
        # If no rotation, use asymptotic values
        f_min = np.sqrt(l*(l+1)) / (n_max_used*P0)
        f_max = np.sqrt(l*(l+1)) / (n_min_used*P0)
    else:
        if unit_rot == 'CRITICAL': # Roche critical
            model_mass   = convert_units('mass',   np.asarray(data['star_mass'])[xc_index], convertto='cgs')
            model_radius = convert_units('radius', 10**np.asarray(data['log_R'])[xc_index], convertto='cgs')
            G = convert_units('cgrav', 1)
            Roche_rate = (1/(2*np.pi))*np.sqrt((8*G*model_mass)/(27*model_radius**3)) # Roche crit rotation rate in cycles per second
            Roche_rate = Roche_rate * 86400 # Roche crit rotation rate in cycles per day
            omega_rot = omega_rot * Roche_rate # Multiply by fraction of the crit rate, to get final omega_rot in cycles per day

        # Make a pandas dataframe containing an interpolation table for lambda (eigenvalues of LTE - TAR)
        data = pkgutil.get_data(__name__, 'lambda.csv')
        data_io = StringIO(data.decode(sys.stdout.encoding))
        df = pd.read_csv(data_io, sep=",")

        # will add extra functionality to calculate the bounds explicitly, making use of GYRE

        # Select nu (spin parameter) and lambda column when values in l and m column correspond to requested values
        NuLambda = df.loc[(df['l'] == l) & (df['m'] == m)][['nu', 'Lambda']]

        # Generate numpy array from pandas dataframe series
        nu = NuLambda['nu'].to_numpy()
        Lambda = NuLambda['Lambda'].to_numpy()

        # Generate difference between pulsation frequency and asymptotic value (in co-rotating frame) in units of c/d
        diff_max = nu/(2.*omega_rot) - P0*n_max_used/np.sqrt(Lambda)
        diff_min = nu/(2.*omega_rot) - P0*n_min_used/np.sqrt(Lambda)
        # Obtain index of minimal difference/distance
        index_max = np.where(abs(diff_max) == np.min(abs(diff_max)))[0]
        index_min = np.where(abs(diff_min) == np.min(abs(diff_min)))[0]
        # Calculate the rotationally shifted frequency (TAR approximation)
        ### in the inertial frame
        if rotation_frame == 'INERTIAL':
            f_min = (np.sqrt(Lambda[index_max]) / (P0*n_max_used) + m*omega_rot)[0]
            f_max = (np.sqrt(Lambda[index_min]) / (P0*n_min_used) + m*omega_rot)[0]
        ### in the co-rotating frame
        else:
            f_min = (np.sqrt(Lambda[index_max]) / (P0*n_max_used))[0]
            f_max = (np.sqrt(Lambda[index_min]) / (P0*n_min_used))[0]
    return f_min, f_max
################################################################################
