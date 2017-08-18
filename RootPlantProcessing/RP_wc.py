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

def RP_wc(parameters):
    '''
    SUMMARY: 
    'RP_wc': creates water content map from specified image using equations specified 
    in Kang et al., 2013.  
    
    USING CODE:
    Calculation assumes a uniform sandy (i.e. primarily Si) soil medium of thickness 'x_s', 
    with two thin sheets of aluminum with combined thickness 'x_a on each side.  Calculated 
    image is a total thickness of water in each pixel, which is then normalized by the 
    thickness of the pixel in total.  
    
    PARAMETERS:
    1. image_filename: filename of evaluated image. 
    2. output_filename: filename where image is to be saved.
    3. b_w: scattering coefficient of water [cm^-2]
    4. s_w: attenuation coefficient of water [cm^-1]
    5. s_a: attenuation coefficient of aluminum [cm^-1]
    6. s_s: attenuation coefficient of silicon [cm^-1]
    7. x_s: thickness of soil [cm]
    8. x_a: thickness of aluminum [cm]
    
    SAMPLE INPUT: 
    #Chamber 2
    wd_filename = '/Users/kdecarlo/Python_scripts'
    image_filename = wd_filename+'/stitched/Chamber10_inj_stitched.fits'
    output_filename = wd_filename+'/wc/Chamber10_inj_wc.fits'
    
    '''
    starttime = time.time()
    scriptname = 'wc'
    
    RP_timerstart(scriptname)
    
    image_filename = parameters['image_filename']
    
    IO_mask = os.path.isfile(image_filename)
    if IO_mask is not True:
        raise ValueError('mask file not found.  Please re-check input files.')
        
    output_filename = parameters['output_filename']
    b_w = parameters['b_w']
    s_w = parameters['s_w']
    s_a = parameters['s_a']
    s_s = parameters['s_s']
    x_s = parameters['x_s']
    x_a = parameters['x_a']
    
    #image = fits.open(image_filename)[0].data
    image = Image.open(image_filename)
    image = np.array(image)    
    
    checkval = np.sum(image == 0)
    if np.sum(image == 0) > 0:
        raise ValueError('Image is blank.  Please re-check inputted data.')
        
    
    #Conversion from transmission data to water thickness [see Kang et al., 2013]
    C1 = s_w/(2*b_w)
    C2_s = s_a*x_s+s_s*x_s

    image[image == 0] = 'nan'
    image[image < 0] = 'nan'
    x = C1*C1-(np.log(image)-C2_s)/b_w
    maskneg = np.isnan(x)
    np.shape(maskneg)
    x[np.isnan(x)] = 0
    x[x < 0] = 0

    x_w = -C1 - np.sqrt(x)
    x_w[x_w == -C1] = 'nan'
    x_w = x_w/x_s
    
    x_w = Image.fromarray(x_w)
    x_w.save(output_filename)
    
    #scipy.misc.imsave(output_filename, x_w)
    
    RP_timerend(starttime)