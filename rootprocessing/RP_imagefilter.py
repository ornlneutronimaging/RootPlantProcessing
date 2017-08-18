import numpy as np
from astropy.io import fits
import time
import scipy.ndimage as imp
import datetime

from scipy import ndimage
from skimage.morphology import skeletonize
import scipy.misc
from scipy.signal import medfilt
from PIL import Image
import os

from rootprocessing.RP_timerstart import RP_timerstart
from rootprocessing.RP_timerprogress import RP_timerprogress
from rootprocessing.RP_timerend import RP_timerend
from rootprocessing.RP_windowrange import RP_windowrange

def RP_imagefilter(parameters):
    '''
    SUMMARY: 
    'RP_imagefilter': conducts a simple filtering process of an image for later processing.
    
    USING CODE:
    Image located in 'image_filename' will be read in and will be converted into a binary image,
    after which a median filter will be applied with a windowsize specified in 'medfilterval'.  
    From that image, an area filter will be applied - all 'True' pixels with a total pixel count 
    higher than 'bwareaval' will be removed from the image.  
    
    
    PARAMETERS:
    1. image_filename: filename of evaluated image. 
    2. output_filename: filename where image is to be saved.
    3. bwareaval: scalar value of the minimum pixel count (i.e. area) to be removed.
    4. medfilterval: window size to be used in the median filter.
    
    SAMPLE INPUT: 
    #Chamber 2
    wd_filename = '/Users/kdecarlo/Python_scripts'
    image_filename = wd_filename+'/stitched/Chamber10_inj_stitched.fits'
    output_filename = wd_filename+'/wc/Chamber10_inj_wc.fits'
    bwareaval = 800
    medfilterval = 5
    
    '''
    
    starttime = time.time()
    scriptname = 'imagefilter'
    RP_timerstart(scriptname)

    image_filename = parameters['image_filename']
    output_filename = parameters['output_filename']
    bwareaval = parameters['bwareaval']
    medfilterval = parameters['medfilterval']
    
    IO_mask = os.path.isfile(image_filename)
    if IO_mask is not True:
        raise ValueError('mask file not found.  Please re-check input files.')
        
    
    #image = fits.open(image_filename)[0].data
    image = Image.open(image_filename)
    image = np.array(image)
    
    image = medfilt(image, kernel_size = medfilterval)
    imdim = np.shape(image)
    
    img = image > 0
    mask_L = ndimage.measurements.label(img)
    mask_label = mask_L[0]
    
    
        
    
    #List of all labeled values
    labelcount = np.asarray(range(0,mask_L[1]+1))
    
    #Number of pixels per labeled object
    surface_areas = np.bincount(mask_label.flat)[0:]
    
    #labels to be converted to 0 - same size as label list, but all 
    #replaced values changed to 0
    removedvals = np.zeros([mask_L[1]+1])
    for i in range(0,mask_L[1]+1):
        if surface_areas[i] <= bwareaval:
            removedvals[i] = 0
        else:
            #0 will be large due to background but needs to remain 0
            if labelcount[i] == 0:
                removedvals[i] = 0
            else:
                removedvals[i] = 1
    
    a = np.array(mask_label.flat)
    palette = labelcount
    key = removedvals
    
    index = np.digitize(a.ravel(), palette, right=True)
    imdim = np.shape(mask_label)
    img = key[index].reshape(imdim[0], imdim[1])
    
    img = Image.fromarray(img)
    img.save(output_filename)
    
    RP_timerend(starttime)

    #imghdu = fits.PrimaryHDU(img)
    #hdulist = fits.HDUList([imghdu])
    #hdulist.writeto(output_filename)
    