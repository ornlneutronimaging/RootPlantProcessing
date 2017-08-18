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
import sys






def RP_run(wd, wd_userconfig = '', analysis_list = [], parameters_ = 0, override = 0):
    '''
    SUMMARY: 
    'RP_run' takes in as input the image processing steps that the user is interested in and runs them.
    
    USING CODE:
    'RP_run' is where the image processing algorithms (whose code and library are all located in the file 
    specified by 'wd') of interest are specified by the user in the list 'analysis_list', and run.  If the
    user is interested in specifying individual parameters for each algorithm, the 'parameters_' variable
    allows the user to specify in dictionary format the specific parameters that the user would like to change
    without manually changing them in the 'user_config.txt' file, whose file location is specified by 
    'wd_userconfig' (if left unspecified, the code assumes it to be in 'wd').  'override' is set to 1 if 
    already existing outputted files can be overwritten with the new run.
    
    
    PARAMETERS:
    1. wd: the working directory where the 'Root_Processing' algorithm is stored.
    2. wd_userconfig: the working directory where the 'user_config.txt' file is located.
    3. analysis_list: a string list of the algorithms that the user wants to run, in order.
    4. parameters_: specific parameters that the user may wish to modify outside of the 'user_config.txt' file.
    5. override: flag for whether the user wants to override previously written files normally outputted by the
    algorithm.
    
    '''
    
    
    
    #if type(wd) is int or type(wd) is float:
    #    raise ValueError('Working directory (wd) is inputted with a numerical value.  Please enter a valid directory.')

    #if type(wd) is str:
    #    if not os.path.isdir(wd):
    #        raise ValueError('Working directory (wd) does not exist.  Please enter a valid directory.')
    
    
    #sys.path.append(wd+'/Analyses')
    #sys.path.append(wd+'/Misc')
    
    from rootprocessing.RP_IOfilecheck import RP_IOfilecheck
    from rootprocessing.RP_timerstart import RP_timerstart
    from rootprocessing.RP_timerprogress import RP_timerprogress
    from rootprocessing.RP_timerend import RP_timerend
    from rootprocessing.RP_stitch import RP_stitch
    from rootprocessing.RP_crop import RP_crop
    from rootprocessing.RP_wc import RP_wc
    from rootprocessing.RP_mask import RP_mask
    from rootprocessing.RP_imagefilter import RP_imagefilter
    from rootprocessing.RP_distmap import RP_distmap
    from rootprocessing.RP_radwc import RP_radwc
    from rootprocessing.RP_thickness import RP_thickness
    from rootprocessing.RP_userconfiganalysis import RP_userconfiganalysis
    from rootprocessing.RP_windowrange import RP_windowrange
    from rootprocessing.RP_distwindowrange import RP_distwindowrange
    from rootprocessing.RP_remove import RP_remove
    from rootprocessing.RP_rootimage import RP_rootimage
    
    '''
    Definitions that can be run for analysis (see below for details):
    1. wc:
    - REQUIRES: neutron transmission image (fits format, range from 0-1)
    - PRODUCES: water content image (fits format)

    2. mask:
    - REQUIRES: neutron transmission image (fits format, range from 0-1)
    - PRODUCES: binary mask image (fits format, range 0, 1)

    3. thickness:
    - REQUIRES: binary mask image (fits format, range 0, 1)
    - PRODUCES: root thickness map (fits format)

    4. distmap:
    - REQUIRES: binary mask image (fits format, range 0, 1)
    - PRODUCES: soil distance map (fits format)

    5. radwc:
    - REQUIRES: water content image, soil distance map, and mask image (all fits format)
    NOTE: if run separately, user must specify all inputs
    - PRODUCES: water content-radius text, wc-rad count, radius and distance values (text files) 

    Miscellaneous processing:
    1. stitch:
    - REQUIRES: original radiographs, open beam (labeled 'OB'), and dark field 
    (labeled 'DF') images (fits format)
    - PRODUCES: stitched neutron transmission image (fits format, range from 0-1)

    2. crop:
    - REQUIRES: any image (fits format)
    - PRODUCES: cropped version of image (fits format)

    3. imagefilter:
    - REQUIRES: original binary mask image (fits format, range 0, 1)
    - PRODUCES: filtered mask image (fits format, range 0, 1)

    Full list of definitions:

    IOfilecheck
    timer
    windowrange
    distwindowrange
    stitch
    crop
    wc
    mask
    thickness
    remove
    distmap
    radwc

    '''
    
    
    #User config analysis positions:
    analysis_pos_list = {
        'RP_stitch':[2,10],
        'RP_crop':[13,15],
        'RP_wc':[18,25], 
        'RP_mask':[28,32],
        'RP_imagefilter':[35,38],
        'RP_distmap':[41,43],
        'RP_radwc':[46,51],
        'RP_thickness':[54,55],
        'RP_rootimage':[58,60]
    }
    
    
    
    #Dispatch
    dispatch = {
        'RP_IOfilecheck':RP_IOfilecheck,
        'RP_timerstart':RP_timerstart,
        'RP_timerprogress':RP_timerprogress,
        'RP_timerend':RP_timerend,
        'RP_windowrange':RP_windowrange,
        'RP_distwindowrange':RP_distwindowrange,
        'RP_stitch':RP_stitch,
        'RP_crop':RP_crop,
        'RP_wc':RP_wc,
        'RP_mask':RP_mask,
        'RP_imagefilter':RP_imagefilter,
        'RP_thickness':RP_thickness,
        'RP_remove':RP_remove,
        'RP_distmap':RP_distmap,
        'RP_radwc':RP_radwc,
        'RP_rootimage':RP_rootimage
    }    
    alist = ['RP_stitch', 'RP_crop', 'RP_wc', 'RP_mask', 'RP_imagefilter', 'RP_thickness', 'RP_remove', 
            'RP_distmap', 'RP_radwc', 'RP_rootimage']
    
    if type(analysis_list) is not list:
        raise ValueError('Analysis list must be in \'list\' format, not as a string.  Please put [] around the analysis terms.')
    
    
    if type(override) is int or type(override) is float:
        if override is not 1 and override is not 0:
            raise ValueError('Override term is not given a valid value.  Please enter either 0 (no override) or 1 (override).')

    if type(override) is str:
        raise ValueError('Override term is not given a valid value.  Please enter either 0 (no override) or 1 (override).')
    
    if type(analysis_list) is int or type(analysis_list) is float:
        #print('Analysis list is inputted with a numerical value.  Please enter a valid processing choice.')
        raise ValueError('Analysis list is inputted with a numerical value.  Please enter a valid processing choice.')
        
    if type(analysis_list) is list:
        counter = 0
        for analysis in analysis_list:
            if analysis in alist:
                counter += 1
        if counter == 0:
            raise ValueError('Analysis list does not have a valid processing choice.  Please enter a correct processing choice.')
    

    
    for analysis in analysis_list:
        analysis_pos = analysis_pos_list[analysis]
        if wd_userconfig == '':
            parameters = RP_userconfiganalysis(wd, analysis_pos, analysis)
        else:
            parameters = RP_userconfiganalysis(wd_userconfig, analysis_pos, analysis)
        if not parameters_ == 0:
            for key in parameters_:
                parameters[key] = parameters_[key]
            
        if analysis == 'RP_stitch':
            I = parameters['image_filename']
            O = parameters['output_filename']
        elif analysis == 'RP_radwc':
            I = parameters['wc_filename'].rsplit('/',1)[0]
            O = parameters['output_filename']
        elif analysis == 'RP_rootimage':
            I = parameters['wc_filename'].rsplit('/',1)[0]
            O = parameters['output_filename'].rsplit('/',1)[0]
        else:
            I = parameters['image_filename'].rsplit('/',1)[0]
            O = parameters['output_filename'].rsplit('/',1)[0]
            
        IOcheck = dispatch['RP_IOfilecheck'](I, O)
                
        if not IOcheck == 10:
            if IOcheck == 0:
                raise ValueError('No input file is present.  Please ensure that either you have your input files, or the user_config.txt file specified the correct input file directory locations.')
            print(analysis+' already has output files.  Skipping...')
            if override == 1:
                override_val = override*100+IOcheck
                print('overriding skip...')
                dispatch[analysis](parameters)
        else:
            dispatch[analysis](parameters)
    
    if __name__ == "__main__":
        import doctest
        doctest.testmod()