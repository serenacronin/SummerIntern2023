"""
Created on Wed Jul 20 14:03:27 2022

@author: Serena A. Cronin

This script smooths a datacube using a 2D Gaussian kernel.
It finds pixels that deviate from their neighbors by +/- 100 km/s and
fills in the average of the nearest neighbors.

"""

# ========================================================================================
# IMPORTS
# ========================================================================================
from astropy.convolution import Gaussian2DKernel, convolve
import numpy as np

# ========================================================================================
# DEFINE FUNCTIONS
# ========================================================================================
def gauss_2d_kernel(sigma):
    
    """
    
    Input : 
        sigma for a 2D Gaussian Kernel.
        
    Output: 
        kernel array where the center is negative, the surrounding values
        are positive, and the entire kernel averages to 0.
        
    Requires Gaussian2DKernel from astropy.convolution
    
    """
    
    # create the kernel
    kernel = Gaussian2DKernel(x_stddev=sigma)
    
    # get the center of the kernel; this should be the max of the kernel, too
    center_index = kernel.shape[0]//2, kernel.shape[1]//2  # integer divide
    kern_arr = kernel.array  # get the kernel array
    
    # make the center pixel positive and the rest negative
    kern_arr[center_index]*=-1
    kern_arr*=-1
    
    # make sure the entire kernel averages to 0
    kern_arr[center_index] = -1*np.sum(kern_arr[kern_arr<0.])
    
    return kern_arr

# ========================================================================================
# DEFINE VARIABLES
# ========================================================================================

beam =  'FIXME' # beamsize taken from the header
mask_kern = 'FIXME'*beam  # sigma for 2D Gaussian kernel to do the masking
fill_kern = 'FIXME'*beam  # sigma for 2D Gaussian kernel to fill in masked values

orig_cube == 'FIXME'  # open the original datacube
orig_data == 'FIXME'  # grab the data from the original datacube

# ========================================================================================
# SMOOTH THE MAPS
# ========================================================================================

kern_arr = gauss_2d_kernel(sigma=mask_kern)  # build the kernel
   
 # convolve with the original map; this will find pixels that deviate
 # a lot from their neighbors
new_image = convolve(orig_data, kern_arr, normalize_kernel=False, nan_treatment='fill')

# set a threshold: we want to find pixels that deviate by +/- 100
# blank out these pixels; this is our mask!
mask = np.abs(new_image) < 100
copy_im = orig_data.copy()
copy_im[~mask] = np.nan

# now we want to fill in these nan pixels with the average
# of the nearest neighbors
kernel = Gaussian2DKernel(fill_kern)
final_image = convolve(copy_im, kernel)

# this adds some weird stuff to the edges, so lets blank the edges back out
# so we have the original dimensions again
final_image[np.isnan(orig_cube[1])] = np.nan # [0] has some nans within

## FIXME: save the final image as a FITS file
