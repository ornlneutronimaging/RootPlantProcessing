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
from rootprocessing.RP_remove import RP_remove

def RP_radwc(parameters):
    '''
    SUMMARY:
    'RP_radwc': creates two NxM text files of the water content of a given root radius (row) at a given distance
    from the root (column), and the number of pixels for each entry, as well as a 1xN and 1xM text file of 
    the root radius values and distance from the root, respectively.  All distance and radius values are 
    outputted in terms of pixels.
    
    USING CODE:
    Necessary images are the water content image (located in 'wc_filename'), the soil-distance map
    created by 'RootProcess.distmap' (located in 'distmap_filename'), and the binary root mask 
    (located in 'mask_filename').  'output_filename' specifies the folder where all files will be placed.
    'fileformat' specifies the name of the file.  The water content for each root radius at a given distance
    will be labeled "fileformat+'_data_xrad_ydist_wc.txt'", the numerical counts as "fileformat+'data_num_xrad'
    +'_ydist_wc.txt'", the y axis (i.e. root radius values) will be labeled "fileformat"+'_data_radrange.txt'", 
    and the x axis (i.e. distance values) will be labeled "fileformat+'_data_distrange.txt'".  So, for example,
    if 'fileformat' = 'Test', then the water content data will be labeled 'Test_data_xrad_ydist_wc.txt'.  
    
    'pixelbin' specifies the number of pixels to be binned on the distance axis, with a default of 3 pixels
    per bin.  
    
    PARAMETERS:
    1. wc_filename: filename of the water content image.  
    2. distmap_filename: filename of the distance map image.
    3. mask_filename: filename of the root mask image.
    4. output_filename: filename where the text files are to be saved.
    5. fileformat: the filename prefix to be attached to the data.
    6. pixelbin: the number of pixels to be binned when determining water contents by distance.
    
    SAMPLE:
    cmat = ['Chamber1', 'Chamber2', 'Chamber3']
    wc_filename = wd_filename+'/wc/'+cmat[0]+'_wc.fits'
    distmap_filename = wd_filename+'/distmap/'+cmat[0]+'_distmap.fits'
    mask_filename = wd_filename+'/filter/'+cmat[0]+'_filter.fits'
    output_filename = wd_filename+'/rhizosphere_data/'+cmat[0]
    fileformat = cmat[0]
    pixelbin = 3

    '''

    starttime = time.time()
    scriptname = 'radwc'
    
    RP_timerstart(scriptname)
    
    wc_filename = parameters['wc_filename']
    distmap_filename = parameters['distmap_filename']
    mask_filename = parameters['mask_filename']
    output_filename = parameters['output_filename']
    fileformat = parameters['fileformat']
    pixelbin = parameters['pixelbin']
    
    IO_rootimage_wc = os.path.isfile(wc_filename)
    IO_rootimage_distmap = os.path.isfile(distmap_filename)
    IO_rootimage_mask = os.path.isfile(mask_filename)
    if (IO_rootimage_wc is not True) or (IO_rootimage_distmap is not True) or (IO_rootimage_mask is not True):
        raise ValueError('Input files are not present in specified file location.  Please recheck input files.')
    
    
    #image_wc = fits.open(wc_filename)[0].data
    #image_distmap = fits.open(distmap_filename)[0].data
    #image_mask = fits.open(mask_filename)[0].data
    image_wc = Image.open(wc_filename)
    image_wc = np.array(image_wc)
    image_distmap = Image.open(distmap_filename)
    image_distmap = np.array(image_distmap)
    image_mask = Image.open(mask_filename)
    image_mask = np.array(image_mask)
    
    
    image_mask = image_mask > 0
    image_rootdist = ndimage.morphology.distance_transform_edt(~image_mask)

    soilmap = image_mask < 1

    pixelpos = np.where(soilmap)
    pixelpos_y = pixelpos[0]
    pixelpos_x = pixelpos[1]

    data = np.zeros([np.shape(pixelpos_y)[0], 3])

    radrange = np.unique(image_distmap)
    distrange = np.unique(image_rootdist)
    maxdistval = np.max(distrange)
    maxradval = np.max(radrange)
    newdistrange = np.array(range(0, int(np.floor(maxdistval)), pixelbin))

    data = np.zeros([int(np.shape(radrange)[0])-1, np.shape(range(0,int(np.floor(maxdistval)), pixelbin))[0]])
    data_num = np.zeros([int(np.shape(radrange)[0])-1, int(np.shape(range(0,int(np.floor(maxdistval)), pixelbin))[0])])
    
    counter = 0
    pctval = 0

    outline_img = RP_remove(image_mask)
    image_mask_wooutline = image_mask > 0
    image_mask_wooutline[outline_img > 0] = False

    image_rootdist[image_mask_wooutline] = -1
    

    totalcount = (np.shape(newdistrange)[0]-1)*(np.shape(radrange)[0]-1)
    for i in range(0,np.shape(newdistrange)[0]-1):
        for j in range(1,np.shape(radrange)[0]):
            [pctval,counter] = RP_timerprogress(counter,pctval,totalcount)
            
            image_pos = (image_rootdist >= newdistrange[i]) & (image_rootdist < newdistrange[i+1]) & (image_distmap == radrange[j])
            if np.sum(image_pos) > 0:
                data[j-1,i] = np.mean(image_wc[image_pos])
                data_num[j-1,i] = np.sum(image_pos)
            
            
    np.savetxt(output_filename+'/'+fileformat+'_data_xrad_ydist_wc.txt', data)
    np.savetxt(output_filename+'/'+fileformat+'_data_num_xrad_ydist_wc.txt', data_num)
    np.savetxt(output_filename+'/'+fileformat+'_data_radrange.txt', radrange[1:np.shape(radrange)[0]])
    np.savetxt(output_filename+'/'+fileformat+'_data_distrange.txt', newdistrange)
    
    RP_timerend(starttime)