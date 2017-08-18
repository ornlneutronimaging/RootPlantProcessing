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
from rootprocessing.RP_distwindowrange import RP_distwindowrange

def RP_thickness(parameters):
    '''
    SUMMARY:
    'RP_thickness': creates a half-thickness image from a binary segmented image of a root, 
    assuming a cylindrical shape.
    
    USING CODE:
    Using the binary image, a skeleton (i.e. medial axis transform) of the original image 
    is calculated.  A distance transform of the root is then calculated.  
    
    From here, for every pixel (x,y)_p, the following are calculated: (1) a minimum 
    distance from the pixel to a medial axis pixel (x, y)_m (i.e. skeleton), from which 
    the distance transform value (i.e. radius R) is extracted; and (2) a minimum distance 
    L_e from the pixel to the root edge (x,y)_e.  Then, assuming a cylindrical distribution, 
    and also assuming that the differences in slopes of lines ep and pm are negligible, 
    the half-dome height H of the pixel is calculated as follows: T^2 = R^2-(R-EP)^2.   
    
    PARAMETERS:
    1. image_filename: filename of evaluated image.  
    2. output_filename: filename where image is to be saved.
    
    SAMPLE INPUT: 
    ctype = 'Chamber10'
    
    wd_filename = '/Volumes/Untitled 2/rhizosphere'
    image_filename = wd_filename+'/morph_mask_crop/clean/'+ctype+'_clean.tif'
    output_filename = wd_filename+'/thickness/'+ctype+'_radmap.fits'
    
    '''
    
    starttime = time.time()
    scriptname = 'thickness map'
    
    image_filename = parameters['image_filename']
    output_filename = parameters['output_filename']
    
    IO_rootimage = os.path.isfile(image_filename)
    if IO_rootimage is not True:
        raise ValueError('Input files are not present in specified file location.  Please recheck input files.')
    

    RP_timerstart(scriptname)

    image = Image.open(image_filename)
    image = np.array(image)
    #image = fits.open(image_filename)[0].data

    image = medfilt(image, kernel_size = 7)
    imdim = np.shape(image)

    #image = np.asarray(image)
    #Skeletonization of root image
    skel = skeletonize(image > 0)

    #Distance transform from center of root to all other pixels
    #dist = ndimage.morphology.distance_transform_edt(~skel)

    #Distance from edge of root to center
    rootdist = ndimage.morphology.distance_transform_edt(image)

    checkwin = int(np.round(np.max(rootdist)*1.5))
    checkwindow = 11
    while checkwindow < checkwin:
        checkwindow += 2

    #Reference distance map for evaluated windows
    windist = np.ones([checkwindow*2+1,checkwindow*2+1])
    windist[checkwindow,checkwindow] = 0
    windist = ndimage.morphology.distance_transform_edt(windist)
    
    [pixelpos_y,pixelpos_x] = np.where(image > 0)

    T_map = np.zeros(imdim)
    counter = 0
    pctval = 0
    totalcount = np.shape(pixelpos_x)[0]

    for m in range(0,np.shape(pixelpos_x)[0]):
        [pctval,counter] = RP_timerprogress(counter,pctval,totalcount)

        i = pixelpos_y[m]
        j = pixelpos_x[m]

        [y1,y2,x1,x2] = RP_windowrange(i,j,np.shape(windist)[0],imdim)
        [y_1,y_2,x_1,x_2,y_c,x_c] = RP_distwindowrange(i,j,np.shape(windist)[0],imdim)

        windist_w = windist[y_1:y_2,x_1:x_2]
        image_w = image[y1:y2,x1:x2]
        #dist_w = dist[y1:y2,x1:x2]
        skel_w = skel[y1:y2,x1:x2]
        rootdist_w = rootdist[y1:y2,x1:x2]


        #Find minimum distance from pixel of interest to skeleton
        skelpos = np.where(skel_w)
        skelpos_y = skelpos[0]
        skelpos_x = skelpos[1]
        skeldist = np.zeros([np.shape(skelpos_y)[0]])
        for k in range(np.shape(skelpos_y)[0]):
            skeldist[k] = np.sqrt((y_c-skelpos_y[k])*(y_c-skelpos_y[k]) + (x_c-skelpos_x[k])*(x_c-skelpos_x[k]))
            minskelpos = np.where(skeldist == np.min(skeldist))
            minskelpos_y = skelpos_y[minskelpos[0][0]]
            minskelpos_x = skelpos_x[minskelpos[0][0]]
            dist_pixel_skel = skeldist[minskelpos[0][0]]

            #Find minimum distance from pixel of interest to edge
            dist_pixel_edge = rootdist_w[y_c,x_c]
            rad_val = rootdist_w[minskelpos_y,minskelpos_x]

            #Calculate thickness
            T_map[i,j] = np.sqrt(rad_val*rad_val-(rad_val-dist_pixel_edge)*(rad_val-dist_pixel_edge))

    #imghdu = fits.PrimaryHDU(T_map)
    #hdulist = fits.HDUList([imghdu])
    #hdulist.writeto(output_filename)
    T_map = Image.fromarray(T_map)
    T_map.save(output_filename)
    
    RP_timerend(starttime)
    