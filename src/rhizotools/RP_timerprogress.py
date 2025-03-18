from __future__ import print_function
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


def RP_timerprogress(counter, pctval, totalcount):
    '''
    SUMMARY: 
    'timer' outputs script progress time.
    
    USING CODE:
    Depending on 'flag', code will operate under 'start', 'progress', or 'end' conditions.  
    'start' will output the 'scriptname' and '% complete' string, while 'progress' will output 
    the percentage and counter specified by 'counter', 'totalcount', and 'pctval', and 'end' 
    will output elapsed time.  

    NOTE: this is written specifically for the current processing routine, and is written with 
    an imaging context in mind.
    
    PARAMETERS:
    A. INPUTS -
    1. scriptname: the name of the script that the timer is being used for.
    2. counter: the number of counts at the current moment.  
    3. totalcount: the total number of counts to be measured.
    4. pctval: the current percentage value evaluated.
    5. starttime: the starting time of the code.
    6. flag: specifies which phase of the timer should be outputted.  Options are 'start', 
    'progress', and 'end'.
    
    B. OUTPUTS (only for 'progress') -
    1. pctval: the current percentage value, with progress added.
    2. counter: the current counter number, with progress added.
    '''
    
    if totalcount < 100:
        if counter/totalcount >= pctval:
            print(round(100*pctval), end=' ')
            pctval += round(100/totalcount)/100
            counter += 1
            return (pctval, counter)
    
    if counter/totalcount >= pctval:
        print(round(100*pctval), end=' ')
        pctval += 0.01
        counter += 1
        return (pctval, counter)
    else:
        counter += 1
        return (pctval, counter)