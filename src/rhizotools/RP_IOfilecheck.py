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

def RP_IOfilecheck(input_filename, output_filename):
    '''
    SUMMARY: 
    'RP_IOfilecheck' confirms whether input and output file locations are prepared for processing.
    
    USING CODE:
    'RP_IOfilecheck' is used to confirm whether there are files to be processed in the input file
    (specified by 'input_filename') and whether there are no files in the output file (specified by
    'output_filename'), and relayed back via 'IOcheck'.  If there is data in the input file but 
    none in the output file, then 'IOcheck' = 10, if there is data in both files, 'IOcheck' = 11, if
    there is data in the output but none in the input, 'IOcheck' = 1, and if there is no data in either,
    'IOcheck' = 0.
    
    PARAMETERS:
    A. INPUTS - 
    1. image_filename: filename where images are to be found.  
    2. output_filename: filename where image is to be saved.   
    3. filedirectoryflag: flag whether missing file should be made if not present.  0 means no, 1 means yes.
    
    B. OUTPUTS -
    1. IOcheck: flag indicating data presence in input/output file.
    '''
    
    Icheck = 0
    Ocheck = 0
    if not os.path.isdir(input_filename):
        os.makedirs(input_filename)
    if not os.path.isdir(output_filename):
        os.makedirs(output_filename)
    
    if any(File.endswith('.fits') for File in os.listdir(input_filename)):
        Icheck = 1
    if any(File.endswith('.tiff') for File in os.listdir(input_filename)):
        Icheck = 1
    if any(File.endswith('.txt') for File in os.listdir(input_filename)):
        Icheck = 1
    
    if any(File.endswith('.fits') for File in os.listdir(output_filename)):
        Ocheck = 1
    if any(File.endswith('.tiff') for File in os.listdir(output_filename)):
        Ocheck = 1
    if any(File.endswith('.txt') for File in os.listdir(output_filename)):
        Ocheck = 1
    
    IOcheck = 10*Icheck + Ocheck
    
    return IOcheck