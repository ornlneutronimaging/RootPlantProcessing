import unittest
import unittest
import numpy as np
import os
from PIL import Image

import sys
import shutil
import filecmp
#sys.path.append(wd+'/Analyses')
#sys.path.append(wd+'/Misc')

#Potential issues: mostly tests if files are not present - would this be sufficient?

class TestClass(unittest.TestCase):
    
    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../../rootprocessing/'))
        self.data_path2 = os.path.abspath(os.path.join(_file_path, '../../'))

        if os.path.isdir(self.data_path+'/Sample_Data_unittest'):
            shutil.rmtree(self.data_path+'/Sample_Data_unittest')
        #print('Hello')
    
    def tearDown(self):
        wd = self.data_path
        if os.path.isdir(wd+'/Sample_Data_unittest'):
            shutil.rmtree(wd+'/Sample_Data_unittest')
        #print('Bye')
        
    
    def test_incorrect_input(self):
                                         
                                         
        '''assert error when processing option not listed in code is given'''
        analysis_list = ['RP_stitch']
        override = 1
        
        bad_analysis_list_sp = ['sitch']
        bad_analysis_list_str = 'RP_stitch'
        bad_analysis_list_int = 4
        
        bad_override_str = 'override'
        bad_override_int = 4
                                         
        wd = self.data_path
        sys.path.append(wd)
        #sys.path.append(wd+'/Analyses')    #Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
                                                                                  
        from RP_run import RP_run                                  
        
        #With override option
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', bad_analysis_list_sp, 0, 1)
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', bad_analysis_list_str, 0, 1)
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', bad_analysis_list_int, 0, 1)
        
        #Without override option
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', bad_analysis_list_sp, 0, 0)
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', bad_analysis_list_str, 0, 0)
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', bad_analysis_list_int, 0, 0)
        
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, bad_override_str)
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, bad_override_int)                                         

    def test_stitch(self):
        wd = self.data_path
        sys.path.append(wd)
        #sys.path.append(wd+'/Analyses')    #Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
        
        from sampledata import sampledata
        from RP_run import RP_run                                  

        sampledata(wd, 1)
        analysis_list = ['RP_stitch']
        
        #user_config-specified image/actual image mismatch - due to number, incorrect file format, etc.
        os.remove(wd+'/Sample_Data_unittest/raw/19000101_Image_0060_0006.tiff')
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
        
        #image sizes are not consistent
        bad_image = np.zeros([100, 100])
        bad_image = Image.fromarray(bad_image)
        bad_image.save(wd+'/Sample_Data_unittest/raw/19000101_Image_0060_0006.tiff')
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1) 
        #print(wd+'/Sample_Data_unittest')
        shutil.rmtree(wd+'/Sample_Data_unittest') 

           
    def test_crop(self):
        wd = self.data_path
        sys.path.append(wd)
        #sys.path.append(wd+'/Analyses')    #Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
        
        from sampledata import sampledata
        from RP_run import RP_run 
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/stitched')
        analysis_list = ['RP_crop']
        
        #Stitched image not found
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
        
        #Cropmat values are greater/larger than the inputted image
        bad_image = np.zeros([20, 20])
        bad_image = Image.fromarray(bad_image)
        bad_image.save(wd+'/Sample_Data_unittest/stitched/SampleImg_stitched.tiff')
        
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
        
        shutil.rmtree(wd+'/Sample_Data_unittest') 
        

        
    def test_wc(self):
        wd = self.data_path
        sys.path.append(wd)
        #sys.path.append(wd+'/Analyses')    #Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/crop')
        analysis_list = ['RP_wc']
        
        #Cropped image not found
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
                
        shutil.rmtree(wd+'/Sample_Data_unittest') 
        


    def test_mask(self):
        wd = self.data_path
        sys.path.append(wd)
        #sys.path.append(wd+'/Analyses')    #Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/crop')
        analysis_list = ['RP_mask']
        
        #Cropped image not found
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
        
        #Image is too small - windowsize is larger than image
        bad_image = np.zeros([5, 5])
        bad_image = Image.fromarray(bad_image)
        bad_image.save(wd+'/Sample_Data_unittest/crop/SampleImg_crop.tiff')
        
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
        
        shutil.rmtree(wd+'/Sample_Data_unittest')
        

    
    def test_imagefilter(self):
        wd = self.data_path
        sys.path.append(wd)
        #sys.path.append(wd+'/Analyses')    #Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/mask')
        analysis_list = ['RP_imagefilter']
        
        #mask image not found
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
        
        shutil.rmtree(wd+'/Sample_Data_unittest')
        
    def test_distmap(self):
        wd = self.data_path
        sys.path.append(wd)
        #sys.path.append(wd+'/Analyses')    #Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/mask_filter')
        analysis_list = ['RP_distmap']
        
        #mask image not found
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
        
        #Mask image has no object to analyze
        bad_image = np.zeros([5, 5])
        bad_image = Image.fromarray(bad_image)
        bad_image.save(wd+'/Sample_Data_unittest/mask_filter/SampleImg_filter.tiff')
        
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
        
        shutil.rmtree(wd+'/Sample_Data_unittest') 
        


    def test_radwc(self):
        wd = self.data_path
        sys.path.append(wd)
        #sys.path.append(wd+'/Analyses')    #Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/wc')
        os.makedirs(wd+'/Sample_Data_unittest/distmap')
        os.makedirs(wd+'/Sample_Data_unittest/mask')
        analysis_list = ['RP_radwc']
        
        #wc, distmap, mask images not found
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
        
        shutil.rmtree(wd+'/Sample_Data_unittest')   
        

    
    def test_thickness(self):
        wd = self.data_path
        sys.path.append(wd)
        #sys.path.append(wd+'/Analyses')    #Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/mask_filter')
        analysis_list = ['RP_thickness']
        
        #mask image not found
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)

        shutil.rmtree(wd+'/Sample_Data_unittest') 
        
    def test_rootimage(self):
        
        wd = self.data_path
        sys.path.append(wd)
        #sys.path.append(wd+'/Analyses')    #Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
        
        from sampledata import sampledata
        from RP_run import RP_run
        
        sampledata(wd, 1)
        os.makedirs(wd+'/Sample_Data_unittest/mask_filter')
        os.makedirs(wd+'/Sample_Data_unittest/wc')
        analysis_list = ['RP_rootimage']
        
        #wc, mask images not found
        self.assertRaises(ValueError, RP_run, wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
                
        shutil.rmtree(wd+'/Sample_Data_unittest')

    def test_allimagesequal(self):
        wd = self.data_path
        sys.path.append(wd)
        #sys.path.append(wd+'/Analyses')    #Not necessary anymore due to __init__.py - test later
        #sys.path.append(wd+'/Misc')
        wd_ = self.data_path2
      
        from sampledata import sampledata
        from RP_run import RP_run
    
        sampledata(wd, 1)
        
        analysis_list = ['RP_stitch', 'RP_crop', 'RP_wc', 'RP_mask', 'RP_imagefilter','RP_distmap', 'RP_radwc', 'RP_thickness', 'RP_rootimage']
        RP_run(wd, wd+'/Sample_Data_unittest', analysis_list, 0, 1)
        
        stitch_image = Image.open(wd+'/Sample_Data_unittest/stitched/SampleImg_stitched.tiff')
        stitch_image_ideal = Image.open(wd_+'/test/Sample_Data_ideal/stitched/SampleImg_stitched.tiff')
        self.assertTrue(np.array_equal(stitch_image, stitch_image_ideal))

        crop_image = Image.open(wd+'/Sample_Data_unittest/crop/SampleImg_crop.tiff')
        crop_image_ideal = Image.open(wd_+'/test/Sample_Data_ideal/crop/SampleImg_crop.tiff')
        self.assertTrue(np.array_equal(crop_image, crop_image_ideal))
        
        
        wc_image = Image.open(wd+'/Sample_Data_unittest/wc/SampleImg_wc.tiff')
        wc_image_ideal = Image.open(wd_+'/test/Sample_Data_ideal/wc/SampleImg_wc.tiff')
        self.assertTrue(np.array_equal(wc_image, wc_image_ideal))
        
        mask_image = Image.open(wd+'/Sample_Data_unittest/mask/SampleImg_mask.tiff')
        mask_image_ideal = Image.open(wd_+'/test/Sample_Data_ideal/mask/SampleImg_mask.tiff')
        self.assertTrue(np.array_equal(mask_image, mask_image_ideal))
            
        filter_image = Image.open(wd+'/Sample_Data_unittest/mask_filter/SampleImg_filter.tiff')
        filter_image_ideal = Image.open(wd_+'/test/Sample_Data_ideal/mask_filter/SampleImg_filter.tiff')
        self.assertTrue(np.array_equal(filter_image, filter_image_ideal))
    
        distmap_image = Image.open(wd+'/Sample_Data_unittest/distmap/SampleImg_distmap.tiff')
        distmap_image_ideal = Image.open(wd_+'/test/Sample_Data_ideal/distmap/SampleImg_distmap.tiff')
        self.assertTrue(np.array_equal(distmap_image, distmap_image_ideal))
    
    
        self.assertTrue(filecmp.cmp(wd+'/Sample_Data_unittest/radwc/SampleImg/SampleImg_data_distrange.txt', wd_+'/test/Sample_Data_ideal/radwc/SampleImg/SampleImg_data_distrange.txt'))
        self.assertTrue(filecmp.cmp(wd+'/Sample_Data_unittest/radwc/SampleImg/SampleImg_data_num_xrad_ydist_wc.txt', wd_+'/test/Sample_Data_ideal/radwc/SampleImg/SampleImg_data_num_xrad_ydist_wc.txt'))
        self.assertTrue(filecmp.cmp(wd+'/Sample_Data_unittest/radwc/SampleImg/SampleImg_data_radrange.txt', wd_+'/test/Sample_Data_ideal/radwc/SampleImg/SampleImg_data_radrange.txt'))
        self.assertTrue(filecmp.cmp(wd+'/Sample_Data_unittest/radwc/SampleImg/SampleImg_data_xrad_ydist_wc.txt', wd_+'/test/Sample_Data_ideal/radwc/SampleImg/SampleImg_data_xrad_ydist_wc.txt'))
            
    
        thickness_image = Image.open(wd+'/Sample_Data_unittest/thickness/SampleImg_thickness.tiff')
        thickness_image_ideal = Image.open(wd_+'/test/Sample_Data_ideal/thickness/SampleImg_thickness.tiff')
        self.assertTrue(np.array_equal(thickness_image, thickness_image_ideal))
                
        ri_image = Image.open(wd+'/Sample_Data_unittest/rootimage/SampleImg_rootimage.tiff')
        ri_image_ideal = Image.open(wd_+'/test/Sample_Data_ideal/rootimage/SampleImg_rootimage.tiff')
        self.assertTrue(np.array_equal(ri_image, ri_image_ideal))
    
        shutil.rmtree(wd+'/Sample_Data_unittest')

    
 
    
        