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


def RP_userconfiganalysis(wd, analysis_pos, analysis):
    IO_userconfig = os.path.isfile(wd+'/user_config.txt')
    if IO_userconfig is not True:
        raise ValueError('user_config.txt file not present in correct location.')
    f = open(wd+'/user_config.txt', 'r')
    parameters = {}
    counter = 1
    errorflag = 0
    for line in f:
        if counter == analysis_pos[0]-1:
            checkline = ''.join(line)
            if analysis == 'RP_stitch':
                if checkline != '1. STITCH\n':
                    errorflag = 1
            if analysis == 'RP_crop':
                if checkline != '2. CROP\n':
                    errorflag = 1
            if analysis == 'RP_wc':
                if checkline != '3. WC\n':
                    errorflag = 1
            if analysis == 'RP_mask':
                if checkline != '4. MASK\n':
                    errorflag = 1
            if analysis == 'RP_imagefilter':
                if checkline != '5. IMAGEFILTER\n':
                    errorflag = 1
            if analysis == 'RP_distmap':
                if checkline != '6. DISTMAP\n':
                    errorflag = 1
            if analysis == 'RP_radwc':
                if checkline != '7. RADWC\n':
                    errorflag = 1
            if analysis == 'RP_thickness':
                if checkline != '8. THICKNESS\n':
                    errorflag = 1
            if analysis == 'RP_rootimage':
                if checkline != '9. ROOTIMAGE\n':
                    errorflag = 1
            if errorflag == 1:
                raise ValueError('user_config.txt is in an incorrect format.  Check if additional lines or text were added or modified in the file.')
        if (counter > analysis_pos[0]-1) & (counter < analysis_pos[1]+1):
            splitline = line.split(':')
            parameters_ = {splitline[0]:splitline[1].strip()}
            for items in parameters_:
                parameters[items] = parameters_[items]
            #parameters = parameters_
            #parameters = {**parameters, **parameters_}
        counter += 1
        
    #1. STITCH
    if analysis == 'RP_stitch':
        try:
            parameters['dimh_horzoffset'] = np.int(parameters['dimh_horzoffset'])
            parameters['dimh_vertoffset'] = np.int(parameters['dimh_vertoffset'])
            parameters['dimv_horzoffset'] = np.int(parameters['dimv_horzoffset'])
            parameters['dimv_vertoffset'] = np.int(parameters['dimv_vertoffset'])
        except ValueError:
            raise ValueError('STITCH - Offset values are not in \'int\' format.')
        try:
            stitchval = parameters['stitch_order']
            stitchval = stitchval.split(',')
            counter = 0
            for val in stitchval:
                stitchval[counter] = np.int(val)
                counter += 1
            parameters['stitch_order'] = stitchval
        except ValueError:
            raise ValueError('\'stitch_order\' values are not in the correct format.')
        if stitchval[0]*stitchval[1] != np.shape(stitchval)[0]-2:
            raise ValueError('STITCH - \'stitch_order\' either has too many or too few numbers.')
            
    
    #2. CROP
    if analysis == 'RP_crop':
        try:
            cropmatval = parameters['cropmat']
            cropmatval = cropmatval.split(',')
            counter = 0
            for val in cropmatval:
                cropmatval[counter] = np.int(val)
                counter += 1
            parameters['cropmat'] = cropmatval
        except ValueError:
            raise ValueError('CROP - \'cropmat\' values are not in the correct format.  Please check documentation.')
    
    #3. WC
    if analysis == 'RP_wc':
        try:
            parameters['b_w'] = np.float(parameters['b_w'])
            parameters['s_w'] = np.float(parameters['s_w'])
            parameters['s_a'] = np.float(parameters['s_a'])
            parameters['s_s'] = np.float(parameters['s_s'])
            parameters['x_s'] = np.float(parameters['x_s'])
            parameters['x_a'] = np.float(parameters['x_a'])
        except ValueError:
            raise ValueError('\'wc\' values are not in the correct format.  Please check documentation.')
        if (parameters['s_w'] < 0) or (parameters['s_a'] < 0) or (parameters['s_s'] < 0) or (parameters['x_s'] < 0) or (parameters['x_a'] < 0):
            raise ValueError('WC - Invalid numbers: s_w, s_a, s_s, x_s, or x_a are less than 0.')  
    
    #4. MASK
    if analysis == 'RP_mask':
        try:
            parameters['windowsize'] = np.int(parameters['windowsize'])
            parameters['threshold'] = np.float(parameters['threshold'])
            parameters['globthresh'] = np.float(parameters['globthresh'])
        except ValueError:
            raise ValueError('\'mask\' values are not in the correct format.  Please check documentation.')
        if parameters['windowsize'] < 0:
            raise ValueError('windowsize must be greater than 0.  Please check documentation.')
        if (parameters['windowsize'] % 2 == 0):
            raise ValueError('MASK - windowsize must be an odd number.  Please check documentation.')
    
    #5. IMAGEFILTER
    if analysis == 'RP_imagefilter':
        try:
            parameters['bwareaval'] = np.int(parameters['bwareaval'])
            parameters['medfilterval'] = np.int(parameters['medfilterval'])
        except ValueError:
            raise ValueError('\'imagefilter\' values are not in the correct format.  Please check documentation.')
        if (parameters['medfilterval'] %2 == 0):
            raise ValueError('medfilterval must be an odd number.  Please check documentation.')
        if (parameters['medfilterval'] < 0) or (parameters['bwareaval'] < 0):
            raise ValueError('IMAGEFILTER - Invalid numbers: medfilterval and bwareaval must be greater than 0.')
        
    #6. DISTMAP
    if analysis == 'RP_distmap':
        try:
            parameters['maxval'] = np.int(parameters['maxval'])
        except ValueError:
            raise ValueError('\'distmap\' values are not in the correct format.  Please check documentation.')
        if parameters['maxval'] < 0:
            raise ValueError('DISTMAP - Invalid numbers: maxval must be greater than 0.')
        
    #7. RADWC
    if analysis == 'RP_radwc':
        try:
            parameters['pixelbin'] = np.int(parameters['pixelbin'])
        except ValueError:
            raise ValueError('\'radwc\' values are not in the correct format.  Please check documentation.')
        if parameters['pixelbin'] < 0:
            raise ValueError('RADWC - Invalid numbers: pixelbin must be greater than 0.')
    
    #8. THICKNESS
    
    #9. ROOTIMAGE
    
    return(parameters)