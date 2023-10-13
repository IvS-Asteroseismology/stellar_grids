## This script takes the GYRE formated output from MESA
## and converts it to the HDF5 GSM input that GYRE can
## recognize.
##
##
## C. Johnston - 12.02.2018
## Taken from https://github.com/colej/entropy3
## Adjusted by M. Michielsen

from sys import argv
import numpy as np
import h5py

#============================================================================================================================
#===  This section contains functions to convert GYRE Input files with the MESA format into HDF5 GSM GYRE Input files
#============================================================================================================================

def get_gyre_attributes_from_MESA_format(filename):
    '''
    @filename:   input  -- filename to read attributes from
    @attrs_data: output --
    '''

    ## Create data-types to be used
    dtype_i32_le     = np.dtype('<i4') ## 32-bit int
    dtype_i64_le     = np.dtype('<i8') ## 64-bit int
    dtype_f64_le     = np.dtype('<f8') ## 64-bit float


    ## This order corresponds to the order in which the variables in the
    ## first line are read in from the MESA format.
    ## This order is n, mass, radius, luminosity, and version number * 100
    ## NOTICE: the version number from MESA format is 100 whereas the version
    ## number for the GSM is 110, so we need to hardcore the GSM version below
    ordered_dtypes   = np.array( [ dtype_i64_le, dtype_f64_le, dtype_f64_le,
                                   dtype_f64_le, dtype_i32_le ] )

    ## The first line contains 5 values which correspond to the
    ## attributes of the GSM format. Extract here and cast to the
    ## appropriate data-type
    with open(filename,'r') as gyre_file:
        attrs_line = gyre_file.readlines()[0].replace('D','E')
        attrs_data = []
        for ii,attr in enumerate(attrs_line.strip().split()):
            attr_cast  = np.array([attr]).astype(ordered_dtypes[ii],order='F')
            attrs_data.append(attr_cast[0])

    return np.hstack(np.array([attrs_data]))

#============================================================================================================================


def get_gyre_datasets_from_MESA_format(filename):

    ## Create data-types to be used
    dtype_f64_le     = np.dtype('<f8') ## 64-bit float

    ## Declare lists for each dataset
    k,r,M_r,L_r,P,T,rho,nabla,N2         = [],[],[],[],[],[],[],[],[]
    gamma_1,nabla_ad,delta,kap,kkT,kkRho = [],[],[],[],[],[]
    eps,eeT,eeRho,omega_rot              = [],[],[],[]

    ## Each column of the MESA formatted output corresponds to a
    ## different dataset that will be added to the GSM file.
    ## NOTICE: The ordering is different, so we need to take care of
    ## the order we Extract in, however, the order in which we add
    ## datasets later is not important.
    ##
    ## We loop over each line and append each value to its appropriate array
    ## while casting it as the proper data-type.
    with open(filename,'r') as gyre_file:
        dataset_lines = gyre_file.readlines()[1:] #.replace('D','E')
        dataset_data  = []

        for oline in dataset_lines:
            line = oline.replace('D','E').strip().split()

            k.append(         np.array( line[0]  ).astype(dtype_f64_le,order='F') )
            r.append(         np.array( line[1]  ).astype(dtype_f64_le,order='F') )
            M_r.append(       np.array( line[2]  ).astype(dtype_f64_le,order='F') )
            L_r.append(       np.array( line[3]  ).astype(dtype_f64_le,order='F') )
            P.append(         np.array( line[4]  ).astype(dtype_f64_le,order='F') )
            T.append(         np.array( line[5]  ).astype(dtype_f64_le,order='F') )
            rho.append(       np.array( line[6]  ).astype(dtype_f64_le,order='F') )
            nabla.append(     np.array( line[7]  ).astype(dtype_f64_le,order='F') )
            N2.append(        np.array( line[8]  ).astype(dtype_f64_le,order='F') )
            gamma_1.append(   np.array( line[9]  ).astype(dtype_f64_le,order='F') )
            nabla_ad.append(  np.array( line[10] ).astype(dtype_f64_le,order='F') )
            delta.append(     np.array( line[11] ).astype(dtype_f64_le,order='F') )
            kap.append(       np.array( line[12] ).astype(dtype_f64_le,order='F') )
            kkT.append(       np.array( line[13] ).astype(dtype_f64_le,order='F') )
            kkRho.append(     np.array( line[14] ).astype(dtype_f64_le,order='F') )
            eps.append(       np.array( line[15] ).astype(dtype_f64_le,order='F') )
            eeT.append(       np.array( line[16] ).astype(dtype_f64_le,order='F') )
            eeRho.append(     np.array( line[17] ).astype(dtype_f64_le,order='F') )
            omega_rot.append( np.array( line[17] ).astype(dtype_f64_le,order='F') )

    k         = np.hstack( np.array( [ k         ] ) )
    r         = np.hstack( np.array( [ r         ] ) )
    M_r       = np.hstack( np.array( [ M_r       ] ) )
    L_r       = np.hstack( np.array( [ L_r       ] ) )
    P         = np.hstack( np.array( [ P         ] ) )
    T         = np.hstack( np.array( [ T         ] ) )
    rho       = np.hstack( np.array( [ rho       ] ) )
    nabla     = np.hstack( np.array( [ nabla     ] ) )
    N2        = np.hstack( np.array( [ N2        ] ) )
    gamma_1   = np.hstack( np.array( [ gamma_1   ] ) )
    nabla_ad  = np.hstack( np.array( [ nabla_ad  ] ) )
    delta     = np.hstack( np.array( [ delta     ] ) )
    kap       = np.hstack( np.array( [ kap       ] ) )
    kkT       = np.hstack( np.array( [ kkT       ] ) )
    kkRho     = np.hstack( np.array( [ kkRho     ] ) )
    eps       = np.hstack( np.array( [ eps       ] ) )
    eeT       = np.hstack( np.array( [ eeT       ] ) )
    eeRho     = np.hstack( np.array( [ eeRho     ] ) )
    omega_rot = np.hstack( np.array( [ omega_rot ] ) )

    datasets  = [k,r,M_r,L_r,P,T,rho,nabla,N2,gamma_1,
                 nabla_ad,delta,kap,kkT,kkRho,eps,eeT,
                 eeRho,omega_rot]

    return datasets

#============================================================================================================================


def convert_gyre_input_from_MESA_format(filename,name_to_save_to):

    ## Create data-types to be used
    dtype_i32_le     = np.dtype('<i4')
    dtype_i64_le     = np.dtype('<i8')
    dtype_f64_le     = np.dtype('<f8')


    ## Get attributes
    attributes  = get_gyre_attributes_from_MESA_format(filename)

    attr_n_value       = attributes[0]
    attr_M_star_value  = attributes[1]
    attr_R_star_value  = attributes[2]
    attr_L_star_value  = attributes[3]
    attr_version_value = 110 #attributes[4]

    ## Create attribute with names and value
    ## and match with appropriate data-type
    attr_n         = [ 'n'       , attr_n_value,       dtype_i64_le ]
    attr_version   = [ 'version' , attr_version_value, dtype_i32_le ]
    attr_R_star    = [ 'R_star'  , attr_R_star_value,  dtype_f64_le ]
    attr_M_star    = [ 'M_star'  , attr_M_star_value,  dtype_f64_le ]
    attr_L_star    = [ 'L_star'  , attr_L_star_value,  dtype_f64_le ]

    attribute_list = [ attr_n, attr_version, attr_R_star,
                       attr_M_star, attr_L_star ]


    datasets = get_gyre_datasets_from_MESA_format(filename)

    dataset_r_value           = datasets[1 ]
    dataset_M_r_value         = datasets[2 ]
    dataset_L_r_value         = datasets[3 ]
    dataset_P_value           = datasets[4 ]
    dataset_T_value           = datasets[5 ]
    dataset_rho_value         = datasets[6 ]
    dataset_nabla_value       = datasets[7 ]
    dataset_N2_value          = datasets[8 ]
    dataset_Gamma_1_value     = datasets[9 ]
    dataset_nabla_ad_value    = datasets[10]
    dataset_delta_value       = datasets[11]
    dataset_kap_value         = datasets[12]
    dataset_kap_kap_T_value   = datasets[13]
    dataset_kap_kap_rho_value = datasets[14]
    dataset_eps_value         = datasets[15]
    dataset_eps_eps_T_value   = datasets[16]
    dataset_eps_eps_rho_value = datasets[17]
    dataset_Omega_rot_value   = datasets[18]


    ## Create dataset names and match with appropriate data-type
    dataset_r           = [ 'r'           , dataset_r_value,           dtype_f64_le ]
    dataset_M_r         = [ 'M_r'         , dataset_M_r_value,         dtype_f64_le ]
    dataset_L_r         = [ 'L_r'         , dataset_L_r_value,         dtype_f64_le ]
    dataset_P           = [ 'P'           , dataset_P_value,           dtype_f64_le ]
    dataset_rho         = [ 'rho'         , dataset_rho_value,         dtype_f64_le ]
    dataset_T           = [ 'T'           , dataset_T_value,           dtype_f64_le ]
    dataset_N2          = [ 'N2'          , dataset_N2_value,          dtype_f64_le ]
    dataset_Gamma_1     = [ 'Gamma_1'     , dataset_Gamma_1_value,     dtype_f64_le ]
    dataset_nabla_ad    = [ 'nabla_ad'    , dataset_nabla_ad_value,    dtype_f64_le ]
    dataset_delta       = [ 'delta'       , dataset_delta_value,       dtype_f64_le ]
    dataset_nabla       = [ 'nabla'       , dataset_nabla_value,       dtype_f64_le ]
    dataset_kap         = [ 'kap'         , dataset_kap_value,         dtype_f64_le ]
    dataset_kap_kap_T   = [ 'kap_kap_T'   , dataset_kap_kap_T_value,   dtype_f64_le ]
    dataset_kap_kap_rho = [ 'kap_kap_rho' , dataset_kap_kap_rho_value, dtype_f64_le ]
    dataset_eps         = [ 'eps'         , dataset_eps_value,         dtype_f64_le ]
    dataset_eps_eps_T   = [ 'eps_eps_T'   , dataset_eps_eps_T_value,   dtype_f64_le ]
    dataset_eps_eps_rho = [ 'eps_eps_rho' , dataset_eps_eps_rho_value, dtype_f64_le ]
    dataset_Omega_rot   = [ 'Omega_rot'   , dataset_Omega_rot_value,   dtype_f64_le ]



    dataset_list        = [ dataset_r, dataset_M_r, dataset_L_r, dataset_P,  dataset_rho,
                            dataset_T, dataset_N2, dataset_Gamma_1, dataset_nabla_ad,
                            dataset_delta, dataset_nabla, dataset_kap, dataset_kap_kap_T,
                            dataset_kap_kap_rho, dataset_eps, dataset_eps_eps_T,
                            dataset_eps_eps_rho, dataset_Omega_rot ]


    try:
        ## Open the hdf5 file
        hdf5_file = h5py.File( name_to_save_to , 'a' )

        ## Loop over the attribute list and add each attribute to the "root" group
        ## of the hdf5 file
        for attr in attribute_list:
            # print('Writing %s with value '%attr[0], attr[1],'as ',attr[2])
            hdf5_file.attrs.create(attr[0],attr[1],dtype=attr[2])

        ## Loop over the dataset list and add each dataset to the "root" group
        ## of the hdf5 file
        for dataset in dataset_list:
            hdf5_file.create_dataset(dataset[0],data=dataset[1],dtype=dataset[2])#,chunks=True,compression="gzip")

        hdf5_file.close()
        return True
    except:
        return False



#============================================================================================================================
#===  This section contains functions to convert MESA profiles into compressed HDF5 files
#============================================================================================================================


def get_profile_attributes(filename):

    ## Create data-types to be used
    dtype_i32_le     = np.dtype('<i4') ## 32-bit int
    dtype_i64_le     = np.dtype('<i8') ## 64-bit int
    dtype_s64_le     = np.dtype('a25') ## string of length 25 characters

    ## The dtype for the first row is i32
    ## The second row will be the attribute names
    ## The third row will have dtypes: i64 / i64 / f64 for the rest

    ## We can read in the columns as recarrays and then convert them later!

    with open(filename,'r') as gyre_file:
        attrs_line   = gyre_file.readlines()[1:3]
        attrs_data   = []
        attrs_dtypes = []
        attrs_names  = [ name for name in attrs_line[0].strip().split() ]

        for ii,value in enumerate(attrs_line[1].strip().split()):
            if ( (ii==0) or (ii==1)):
                select_dtype = dtype_i64_le
            else:
                select_dtype = dtype_s64_le

            attrs_cast = np.array([value]).astype(select_dtype,order='F')
            attrs_data.append( attrs_cast[0] )
            attrs_dtypes.append( select_dtype )

    attrs_names  = np.hstack([attrs_names ])
    attrs_data   = np.hstack([attrs_data  ])
    attrs_dtypes = np.hstack([attrs_dtypes])

    return attrs_names, attrs_data, attrs_dtypes


#============================================================================================================================


def get_profile_datasets(filename):

    datasets = np.genfromtxt(filename,skip_header=5,names=True)

    return datasets


#============================================================================================================================


def convert_profile_to_hdf5(filename,name_to_save_to):
    ## This function converts a MESA Model to a compressed hdf5 file.
    ## The first 3 lines are read in to be stored as attributes
    ## The remaining data will be stored as datasets

    ## Create data-types to be used
    dtype_i32_le     = np.dtype('<i4') ## 32-bit int
    dtype_i64_le     = np.dtype('<i8') ## 64-bit int
    dtype_f64_le     = np.dtype('<f8') ## 64-bit float

    #name_to_save_to = filename+'.h5'

    ## Get attribute names and values
    attrs_names, attrs_values, attrs_dtypes = get_profile_attributes(filename)

    ## Get dataset names and values
    datasets = get_profile_datasets(filename)

    try:
        hdf5_file = h5py.File( name_to_save_to , 'w' )

        ## Write attributes to 'root' group
        for ii,attr in enumerate(attrs_names):
            hdf5_file.attrs.create(attr,attrs_values[ii],dtype=attrs_dtypes[ii])

        for name in datasets.dtype.names:
            hdf5_file.create_dataset(name,data=datasets[name],dtype=dtype_f64_le,chunks=True,compression="gzip")

        hdf5_file.close()
        return True
    except:
        return False


#============================================================================================================================


def get_history_attributes(filename):

    ## Create data-types to be used
    # dtype_i32_le     = np.dtype('<i4') ## 32-bit int
    # dtype_i64_le     = np.dtype('<i8') ## 64-bit int
    # dtype_f64_le     = np.dtype('<f8') ## 64-bit float
    dtype_s64_le     = np.dtype('a25') ## string of length 25 characters

    ## The dtype for the first row is i32
    ## The second row will be the attribute names
    ## The third row will have dtypes: i64 / i64 / f64 for the rest

    ## We can read in the columns as recarrays and then convert them later!

    with open(filename,'r') as gyre_file:
        attrs_line   = gyre_file.readlines()[1:3]
        attrs_data   = []
        attrs_dtypes = []
        attrs_names  = [ name for name in attrs_line[0].strip().split() ]

        for ii,value in enumerate(attrs_line[1].strip().split()):
            # if (ii==0):
            #     select_dtype = dtype_i64_le
            # else:
            select_dtype = dtype_s64_le

            attrs_cast = np.array([value.replace('"','')]).astype(select_dtype,order='F')
            attrs_data.append( attrs_cast[0] )
            attrs_dtypes.append( select_dtype )

    attrs_names  = np.hstack([attrs_names ])
    attrs_data   = np.hstack([attrs_data  ])
    attrs_dtypes = np.hstack([attrs_dtypes])

    return attrs_names, attrs_data, attrs_dtypes


#============================================================================================================================
#===  This section contains functions to convert MESA History files into compressed HDF5 files
#============================================================================================================================


def get_history_datasets(filename):

    datasets = np.genfromtxt(filename,skip_header=5,names=True)

    return datasets


#============================================================================================================================


def convert_history_to_hdf5(filename,name_to_save_to):

    ## This function converts a MESA history file to a compressed hdf5 file.
    ## The first 3 lines are read in to be stored as attributes
    ## The remaining data will be stored as datasets

    ## Create data-types to be used
    dtype_i32_le     = np.dtype('<i4') ## 32-bit int
    dtype_i64_le     = np.dtype('<i8') ## 64-bit int
    dtype_f64_le     = np.dtype('<f8') ## 64-bit float

    #name_to_save_to = filename+'.h5'

    ## Get attribute names and values
    attrs_names, attrs_values, attrs_dtypes = get_history_attributes(filename)

    ## Get dataset names and values
    datasets = get_history_datasets(filename)

    try:
        hdf5_file = h5py.File( name_to_save_to , 'w' )

        ## Write attributes to 'root' group
        for ii,attr in enumerate(attrs_names):
            hdf5_file.attrs.create(attr,attrs_values[ii],dtype=attrs_dtypes[ii])

        for name in datasets.dtype.names:
            hdf5_file.create_dataset(name,data=datasets[name],dtype=dtype_f64_le)

        hdf5_file.close()
        return True
    except:
        return False


#============================================================================================================================
#===  This section contains functions to read compressed HDF5 MESA profiles & History Files
#============================================================================================================================

def read_hdf5_profile(filename,fields=None):

    ## This function reads MESA profiles stored in HDF5 format

    profile = h5py.File(filename,'r')

    attr_keys = profile.attrs.keys()
    keys = profile.keys()

    r_attrs      = {}
    r_quantities = {}
    ## Print Attributes
    # print('Attributes:')
    for akey in attr_keys:
        #print '\t%s:  %f'%(akey,profile.attrs[akey])
        r_attrs[akey] = profile.attrs[akey]

    ## Print profile quantities
    # print('Quantities:')
    if fields is not None:
        for key in fields:
            #print '\t%s: %f'%(key,profile[key].value[0])
            r_quantities[key] = profile[key].value
    else:
        for key in keys:
            r_quantities[key] = profile[key].value
            #print '\t%s:  %f'%(key,profile[key].value[0])

    profile.close()

    return r_quantities

def read_hdf5_history(filename,fields=None,return_attributes=False):

    ## This function reads MESA profiles stored in HDF5 format

    track = h5py.File(filename,'r')

    ## Get Attributes
    if return_attributes:
        r_attrs = {}
        for akey in track.attrs.keys():
            r_attrs[akey] = track.attrs[akey]
        #r_attrs = [ (akey,track.attrs[akey]) for akey in track.attrs.keys() ]
    else:
        r_attrs = None

    ## Get evolutionary quantities
    if fields is not None:
        r_quantities = {}
        for key in fields:
            r_quantities[key] = np.array(track[key].value)
        #r_quantities = [ (key,track[key].value) for key in fields ]
    else:
        r_quantities = {}
        for key in track.keys():
            r_quantities[key] = track[key].value
        #r_quantities = [ (key,track[key].value) for key in tracks.keys() ]

    track.close()

    return r_attrs, r_quantities
