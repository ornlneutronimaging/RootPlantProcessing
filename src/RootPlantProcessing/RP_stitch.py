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
from rootprocessing.RP_IOfilecheck import RP_IOfilecheck

def RP_stitch(parameters):
    '''
    SUMMARY: 
    'RP_stitch': creates combined image from specified multiple images.
    
    USING CODE: 
    'stitch_order' will specify the number of images, numbering scheme, and image position. 
    From the specified parameters, images located in 'image_filename' and labeled under the 
    general filename format 'fileformat' will be read in and positioned using the offset 
    variables specified in 'dimv_horzoffset', 'dimv_vertoffset', 'dimh_horzoffset', and 
    'dimh_vertoffset'.  The stitched image will then be outputted to 'output_filename' under
    the filename 'fileformat_stitched.fits'.  
    
    NOTE: Dark field and open beam images must be located in the same file, named 'DF.fits',
    and 'OB.fits', respectively.  Filenames will assume '%04d' format for numbering.  
    
    PARAMETERS:
    1. image_filename: filename where images are to be found.  
    2. output_filename: filename where image is to be saved.
    3. fileformat: filename format of the images.  Eg. For images labeled 'Scan_0001.fits',
    'Scan_0002.fits', etc., filename = 'Scan'.  
    4. stitch_order: array whose first two values indicate row and column number, and then
    following values specify what each column, by row, each image fits into.  
    example: img0-7 in a 2x4 r/c matrix format
           [4,5,6,7]
           [3,2,1,0]
     ---> stitch_order = [2,4,4,5,6,7,3,2,1,0]
    5. imdim: dimensions of the images to be stitched.  
    6-9. Offset values: 'dim_v' for images in vertical direction
    
    NOTE: all images in the row will be considered to have an equivalent offset, and all
    images in the column will be considered to have an equivalent offset.  

    img1: col B, row A
    img2: col A, row A
            __________
    _______|__       |
    |      | |       |
    |  img2| |  img1 |
    |      |_|_______|        
    |________|           |   <---- dimv_vertoffset

            _  <---- dimv_horzoffset



    img2: col A, row A
    img3: col A, row B

       ________
       |      |
       | img2 |
     __|_____ |
     | |____|_|    |   <---- dimh_horzoffset
     |      |
     | img3 |
     |______|


             _   <----- dimh_vertoffset


    SAMPLE INPUT:
    #Chamber 2_8: 8, post H2O w/ lamp

    image_filename = '/Volumes/Untitled 2/IPTS-14336/imgs/radiograph'
    output_filename = '/Volumes/Untitled 2/IPTS-14336/imgs/stitched'
    fileformat = 'Chamber2_8_'


    stitch_order = [4,4,63,62,61,60,70,69,68,67,77,76,75,74,84,83,82,81]

    dimv_horzoffset = 95
    dimv_vertoffset = 25
    dimh_horzoffset = 7
    dimh_vertoffset = 161


    '''
    starttime = time.time()
    scriptname = 'stitch'
    
    image_filename = parameters['image_filename']
    output_filename = parameters['output_filename']
    stitch_order = parameters['stitch_order']
    fileformat = parameters['fileformat']
    dimh_horzoffset = parameters['dimh_horzoffset']
    dimh_vertoffset = parameters['dimh_vertoffset']
    dimv_horzoffset = parameters['dimv_horzoffset']
    dimv_vertoffset = parameters['dimv_vertoffset']
    output_fileformat = parameters['output_fileformat']
    
    imformat = 'tiff'
    
    RP_timerstart(scriptname)
    
    image_fn = image_filename+'/'+fileformat+'_'
    if output_fileformat == 0:   
        output_fn = output_filename+'/'+fileformat+'_stitched.'+imformat
    else:
        output_fn = output_filename+'/'+output_fileformat+'_stitched.'+imformat

    so = stitch_order
    stitch_order = np.zeros([int(so[0]),int(so[1])])
    

    counter = 2
    for i in range(0,so[0]):
        for j in range(0,so[1]):
            stitch_order[i,j] = so[counter]
            counter += 1
    #Read in OB/DF images
    OB_filename = image_filename+'/OB.'+imformat
    DF_filename = image_filename+'/DF.'+imformat
    IO_DF = os.path.isfile(DF_filename)
    IO_OB = os.path.isfile(OB_filename)
    if IO_DF is not True:
        raise ValueError('Dark field image not present in file.')
    if IO_OB is not True:
        raise ValueError('Open beam image not present in file.')

    if imformat == 'fits':
        ##DF
        DF = fits.open(DF_filename)[0].data
        ##OB
        OB = fits.open(OB_filename)[0].data-DF
    elif imformat == 'tiff':
        DF = Image.open(DF_filename)
        OB = Image.open(OB_filename)
        DF = np.flipud(DF)
        OB = np.flipud(OB)


        
    imdim = np.shape(OB)
    imdim_OB = imdim
    imdim_DF = np.shape(DF)
    if imdim_OB != imdim_DF:
        raise ValueError('Open beam and dark field images are not the same size.  Please re-check files.')
    #[2048, 2048]
    #Read in images and stitch them into master image
    dimval = np.shape(stitch_order)

    ##Define row and col positions for each image
    dimval = np.shape(stitch_order)
    rowvals = np.zeros([dimval[0]*dimval[1]])
    colvals = np.zeros([dimval[0]*dimval[1]])
    rowvals[0] = int(np.round(((dimval[0]-1)+0.25)*imdim[0]))
    colvals[0] = int(np.round(0.25*imdim[1]))

    stitch_list = np.zeros([dimval[0]*dimval[1]])

    
    counter = 0
    for i in range(0,dimval[0]):
        for j in range(0,dimval[1]):
            stitch_list[counter] = stitch_order[i,j]
            if i+j==0:
                counter += 1
                continue
            rowvals[counter] = rowvals[0]-i*(imdim[0]-dimh_horzoffset)+j*dimv_vertoffset
            colvals[counter] = colvals[0]+j*(imdim[0]-dimv_horzoffset)-i*dimh_vertoffset
            counter += 1

    image = np.zeros([int(np.round((dimval[0]+0.5)*imdim[0])), int(np.round(((dimval[1]+0.5)*imdim[1])))])
    counter = 1
            
    for i in range(0,dimval[0]*dimval[1]):
        so = int(stitch_list[i])
        
        #print(so, end = ' ')
        #print(type(so), end = ' ')
        
        filename = image_fn+'%04d' %so
        filename = filename+'.'+imformat
        IO_img = os.path.isfile(filename)
        if IO_img is not True:
            raise ValueError('One or more of the raw images specified in \'stitch_order\' is not present.  Please re-check raw images.')
        counter += 1
        
        
        #print(filename)
        if imformat == 'fits':
            img = fits.open(filename)[0].data-DF
        elif imformat == 'tiff':
            img = Image.open(filename)
            img = np.flipud(img)
            imdim_indcheck = np.shape(img)
            if imdim_indcheck != imdim_OB:
                raise ValueError('Raw image size is inconsistent.  Please re-check individual files.')
            img = img - DF    
        img = np.divide(img, OB)
        image[int(rowvals[i]):int(rowvals[i]+imdim[0]),int(colvals[i]):int(colvals[i]+imdim[1])] = img

    #row cutting
    img_row = np.zeros([np.shape(image)[0]])
    img_col = np.zeros([np.shape(image)[1]])
    for i in range(0,np.shape(image)[0]):
        img_row[i] = np.sum(image[i,0:np.shape(image)[1]])

    #column cutting    
    for i in range(0,np.shape(image)[1]):
        img_col[i] = np.sum(image[0:np.shape(image)[0],i])

    row_first = np.nonzero(img_row)[0][0]
    row_last = np.nonzero(img_row)[0][np.shape(np.nonzero(img_row)[0])[0]-1]
    col_first = np.nonzero(img_col)[0][0]
    col_last = np.nonzero(img_col)[0][np.shape(np.nonzero(img_col)[0])[0]-1]

    if imformat == 'fits':
        img = image[row_first:row_last,col_first:col_last]
        imghdu = fits.PrimaryHDU(img)
        hdulist = fits.HDUList([imghdu])
        hdulist.writeto(output_fn)
    elif imformat == 'tiff':
        img = image[row_first:row_last,col_first:col_last]
        img = np.flipud(img)
        img = Image.fromarray(img)
        img.save(output_fn)

        #scipy.misc.imsave(output_fn, img)
    
    RP_timerend(starttime)