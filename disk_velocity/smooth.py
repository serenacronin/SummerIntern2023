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
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

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

beam =  'FIXME' # beamsize taken from the header (in arcsec)
mask_kern = 'FIXME'*beam  # sigma for 2D Gaussian kernel to do the masking
fill_kern = 'FIXME'*beam  # sigma for 2D Gaussian kernel to fill in masked values

orig_cube == 'FIXME'  # path to open the original datacube
orig_data == 'FIXME'  # grab the data from the original datacube

plot = False  # set to True if you want to plot the intermediate steps
              # to help you figure out what beam to smooth to

# ========================================================================================
# SMOOTH THE MAPS
# ========================================================================================
kern_arr = gauss_2d_kernel(sigma=mask_kern)  # build the kernel
   
# convolve with the original map; this will find pixels that deviate
# a lot from their neighbors
new_image = convolve(orig_data, kern_arr, normalize_kernel=False, nan_treatment='fill')

if plot == True:
    vmin = 'FIXME: SET VELOCITY MIN FOR PLOTTING'
    vmax = 'FIXME: SET VELOCITY MAX FOR PLOTTING'
    ax = plt.subplot(2, 2, 1)
    ax.imshow(orig_data, vmin=vmin, vmax=vmax, origin='lower', cmap='RdBu_r')
    ax.set_title('Original', fontsize=20)
    ax.tick_params(axis='both', which='both',direction='in',
                   width=2.5, labelsize=16, length=7)
    ax.set_xlabel('x pixels', fontsize=20)
    ax.set_ylabel('y pixels', fontsize=20)

# set a threshold: we want to find pixels that deviate by +/- 100
# blank out these pixels; this is our mask!
mask = np.abs(new_image) < 100  # feel free to mess with this threshold!
copy_im = orig_data.copy()
copy_im[~mask] = np.nan

if plot == True:
    ax = plt.subplot(2, 2, 2)
    im = ax.imshow(mask, origin='lower', cmap='Greys_r')
    ax.set_title('Mask', fontsize=20)
    ax.tick_params(axis='both', which='both',direction='in',
                   width=2.5, labelsize=16, length=7)
    ax.coords[0].set_auto_axislabel(False)
    ax.coords[0].set_ticklabel_visible(False)
    ax.coords[1].set_auto_axislabel(False)
    ax.coords[1].set_ticklabel_visible(False)
    
    # add an annotation
    at = AnchoredText(
    '%sx beam' % int(round(mask_kern/beam,1)), prop=dict(size=18), frameon=True, loc='lower right')
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)

# now we want to fill in these nan pixels with the average
# of the nearest neighbors
kernel = Gaussian2DKernel(fill_kern)
final_image = convolve(copy_im, kernel)

if plot == True:
    ax = plt.subplot(2, 2, 3)
    ax.imshow(final_image, vmin=-160, vmax=160, origin='lower',cmap='RdBu_r')
    ax.set_title('Smoothed Image',fontsize=20)
    ax.tick_params(axis='both', which='both',direction='in',
                    width=2.5, labelsize=16, length=7)
    
    # add an annotation
    at = AnchoredText(
    '%sx beam' % int(round(fill_kern/beam,1)), prop=dict(size=18), frameon=True, loc='lower right')
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)

    ax.coords[0].set_auto_axislabel(False)
    ax.coords[0].set_ticklabel_visible(False)
    ax.coords[1].set_auto_axislabel(False)
    ax.coords[1].set_ticklabel_visible(False)

# this adds some weird stuff to the edges, so lets blank the edges back out
# so we have the original dimensions again
final_image[np.isnan(orig_cube[1])] = np.nan # [0] has some nans within

if plot == True:
    ax.imshow(final_image, vmin=vmin, vmax=vmax, origin='lower',cmap='RdBu_r')
    ax.set_title('Final Image',fontsize=20)
    ax.tick_params(axis='both', which='both',direction='in',
                    width=2.5, labelsize=16, length=7)
    ax.coords[0].set_auto_axislabel(False)
    ax.coords[0].set_ticklabel_visible(False)
    ax.coords[1].set_auto_axislabel(False)
    ax.coords[1].set_ticklabel_visible(False)

    plt.show()

## FIXME: save the final image as a FITS file
