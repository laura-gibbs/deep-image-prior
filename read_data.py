import array
import os
import numpy as np


def define_dims(res):
    r"""Defines dimensions of image according to resolution.

    Args:
        res (float): degree resolution.

    Returns:
        II (int): x axis dimensions.
        JJ (int): y axis dimensions.
  
    """
    II = int(360/res)
    JJ = int(180/res)
    return II, JJ


def parse_res(filename):
    for letter in range(len(filename)):
        if filename[letter:letter+2] == 'rr':
            res = 1/int(filename[letter+2:letter+6])
            return res


def parse_mdt(filename):
    r"""Checks whether input file is MDT by counting number of underscores.
    
    Args:
        filename (String)

    Returns:
        boolean

    """
    if filename.count("_") == 3:
        return True
    else:
        return False


def reshape_data(filename, res=None, mdt_bool=None):
    r"""Reshapes surface from 1d array into an array of
    (JJ, II) records.

    Ignores the header and footer of each record.

    Args:
        file (np.array): A .dat file containing a 1D array of floats
            respresenting input surface.

    Returns:
        np.array: size (JJ, II)
    """
    if res is None:
        res = parse_res(filename)
    if mdt_bool is None:
        mdt_bool = parse_mdt(filename)

    II, JJ = define_dims(res)

    fid = open(filename, mode='rb')
    a = array.array("i")
    a.fromfile(fid, 1)

    b = a[0]
    floats = array.array("f")
    floats.fromfile(fid, b//4+1)
    floats = floats[1:]
    floats = np.asarray(floats)
    floats = np.reshape(floats, (JJ, II))
    if mdt_bool:
        floats[floats < -1.8e+19] = np.nan
    
    return floats, mdt_bool


def write_dat(data, filename, nan_mask=None, overwrite=False):
    r"""
    """
    if os.path.exists(filename) and not overwrite:
        raise OSError("Yo there's aleady a file here. If you want me to to overwrite it pass overwrite=True.")

    if filename[len(filename)-4:] != '.dat':
        filename += '.dat'

    # Grab height and width, then convert data to 1d array
    JJ, II = data.shape
    floats = data.flatten()

    # Convert the NaNs back to how gay fortran likes em
    if nan_mask is not None:
        floats = floats * nan_mask
    floats[np.isnan(floats)] = -1.9e+19

    # Calculate header (number of total bytes in MDT)
    header = np.array(JJ * II * 4)

    # Convert everything to bytes and write
    floats = floats.tobytes()
    header = header.tobytes()
    footer = header
    fid = open(filename, mode='wb')
    fid.write(header)
    fid.write(floats)
    fid.write(footer)
    fid.close()
    
    return True

def calc_residual(arr1, arr2):
    r""" Calculates the residual between two surfaces.

    Checks whether input arrays have the same dimensions.

    Args:
        arr1 (np.array): surface 1.
        arr2 (np.array): surface 2.

    Returns:
        np.array: An array representing the residual surface
            i.e. the difference between the input surfaces.
    """
    if np.shape(arr1) == np.shape(arr2):
        return np.subtract(arr1, arr2)
    else:
        return print("Cannot compute residual: surfaces are not same shape")


# def batch_reshape():
#     for filename in filenames:
#         reshape_data(filename, parse_res(filename), mdt=)


def main():
    print("read_data.py main")


if __name__ == '__main__':
    main()
