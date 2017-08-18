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


def sampledata(wd, unittest = 0):
    '''
    'sampleimages' generates a suite of images: a sample spiral image, a 'raw' version of the reference image divided into 6 individual images, and a sample dark field and open beam image.  This also creates a sample 'user_config' text file to analyze this dummy data.  Set 'unittest' to 1 if using this for a unit test.
    '''
        
    #Create the 'user_config' data file    
    if unittest == 1:
        unittest_str = 'Sample_Data_unittest'
    else:
        unittest_str = 'Sample_Data'
    if not os.path.isdir(wd+'/'+unittest_str+'/raw'):
        os.makedirs(wd+'/'+unittest_str+'/raw')
    f = open(wd+'/'+unittest_str+'/user_config.txt', 'w')
    
        
    f.write('1. STITCH\n')
    f.write('image_filename:'+wd+'/'+unittest_str+'/raw\n')
    f.write('output_filename:'+wd+'/'+unittest_str+'/stitched\n')
    f.write('output_fileformat:SampleImg\n')
    f.write('fileformat:19000101_Image_0060\n')
    f.write('dimv_horzoffset:20\n')
    f.write('dimv_vertoffset:10\n')
    f.write('dimh_horzoffset:5\n')
    f.write('dimh_vertoffset:7\n')
    f.write('stitch_order:2,3,3,2,1,6,5,4\n')
    f.write('\n')
    f.write('2. CROP\n')
    f.write('image_filename:'+wd+'/'+unittest_str+'/stitched/SampleImg_stitched.tiff\n')
    f.write('output_filename:'+wd+'/'+unittest_str+'/crop/SampleImg_crop.tiff\n')
    f.write('cropmat:21,472,183,633\n')
    f.write('\n')
    f.write('3. WC\n')
    f.write('image_filename:'+wd+'/'+unittest_str+'/crop/SampleImg_crop.tiff\n')
    f.write('output_filename:'+wd+'/'+unittest_str+'/wc/SampleImg_wc.tiff\n')
    f.write('b_w:-2.14\n')
    f.write('s_w:5.3\n')
    f.write('s_a:0.02015\n')
    f.write('s_s:0.006604\n')
    f.write('x_s:1\n')
    f.write('x_a:0.2\n')
    f.write('\n')
    f.write('4. MASK\n')
    f.write('image_filename:'+wd+'/'+unittest_str+'/crop/SampleImg_crop.tiff\n')
    f.write('output_filename:'+wd+'/'+unittest_str+'/mask/SampleImg_mask.tiff\n')
    f.write('windowsize:11\n')
    f.write('threshold:0.05\n')
    f.write('globthresh:0.3\n')
    f.write('\n')
    f.write('5. IMAGEFILTER\n')
    f.write('image_filename:'+wd+'/'+unittest_str+'/mask/SampleImg_mask.tiff\n')
    f.write('output_filename:'+wd+'/'+unittest_str+'/mask_filter/SampleImg_filter.tiff\n')
    f.write('bwareaval:800\n')
    f.write('medfilterval:5\n')
    f.write('\n')
    f.write('6. DISTMAP\n')
    f.write('image_filename:'+wd+'/'+unittest_str+'/mask_filter/SampleImg_filter.tiff\n')
    f.write('output_filename:'+wd+'/'+unittest_str+'/distmap/SampleImg_distmap.tiff\n')
    f.write('maxval:400\n')
    f.write('\n')
    f.write('7. RADWC\n')
    f.write('wc_filename:'+wd+'/'+unittest_str+'/wc/SampleImg_wc.tiff\n')
    f.write('distmap_filename:'+wd+'/'+unittest_str+'/distmap/SampleImg_distmap.tiff\n')
    f.write('mask_filename:'+wd+'/'+unittest_str+'/mask/SampleImg_mask.tiff\n')
    f.write('output_filename:'+wd+'/'+unittest_str+'/radwc/SampleImg\n')
    f.write('fileformat:SampleImg\n')
    f.write('pixelbin:1\n')
    f.write('\n')
    f.write('8. THICKNESS\n')
    f.write('image_filename:'+wd+'/'+unittest_str+'/mask_filter/SampleImg_filter.tiff\n')
    f.write('output_filename:'+wd+'/'+unittest_str+'/thickness/SampleImg_thickness.tiff\n')
    f.write('\n')
    f.write('9. ROOTIMAGE\n')
    f.write('wc_filename:'+wd+'/'+unittest_str+'/wc/SampleImg_wc.tiff\n')
    f.write('mask_filename:'+wd+'/'+unittest_str+'/mask_filter/SampleImg_filter.tiff\n')
    f.write('output_filename:'+wd+'/'+unittest_str+'/rootimage/SampleImg_rootimage.tiff\n')
    f.close()
  
    #Create the dummy data
    img = np.ones([500, 500])*200

    counter = 1
    for j in range(0, 6):
        for i in range(0, 360, 1):
            x = 250+np.int(np.cos(np.deg2rad(i))*counter)
            y = 250+np.int(np.sin(np.deg2rad(i))*counter)
            counter+= 0.1
            img[(x-6):(x+6), (y-6):(y+6)] = 50


        
    mu = 0
    sigma = 1
    noiseimg = np.random.normal(mu, sigma, [500, 500])*40
    noiseimg[noiseimg < -49] = 0
    noiseimg[noiseimg > 50] = 0
    if unittest != 1:
        img = noiseimg+img

    DF = np.zeros([250, 250])
    noiseimg_DF = np.random.normal(mu, sigma, [250, 250])*5
    noiseimg_DF[noiseimg_DF < 0] = 0
    noiseimg_DF[noiseimg_DF > 250] = 0
    if unittest != 1:
        DF = DF+noiseimg_DF

    OB = np.ones([250, 250])*240
    noiseimg_OB = np.random.normal(mu, sigma, [250, 250])
    noiseimg_OB[noiseimg_OB > 10] = 0
    noiseimg_OB[noiseimg_OB < 230] = 0
    if unittest != 1:
        OB = OB+noiseimg_OB

    img1 = np.ones([250, 250])*200
    img2 = np.ones([250, 250])*200
    img3 = np.ones([250, 250])*200
    img4 = np.ones([250, 250])*200
    img5 = np.ones([250, 250])*200
    img6 = np.ones([250, 250])*200

    noiseimg_indv = np.random.normal(mu, sigma, [250, 250])*40
    noiseimg_indv[noiseimg_indv < -49] = 0
    noiseimg_indv[noiseimg_indv > 50] = 0
    if unittest != 1:
        img1 = img1+noiseimg_indv
    noiseimg_indv = np.random.normal(mu, sigma, [250, 250])*40
    noiseimg_indv[noiseimg_indv < -49] = 0
    noiseimg_indv[noiseimg_indv > 50] = 0
    if unittest != 1:
        img2 = img2+noiseimg_indv
    noiseimg_indv = np.random.normal(mu, sigma, [250, 250])*40
    noiseimg_indv[noiseimg_indv < -49] = 0
    noiseimg_indv[noiseimg_indv > 50] = 0
    if unittest != 1:
        img3 = img3+noiseimg_indv
    noiseimg_indv = np.random.normal(mu, sigma, [250, 250])*40
    noiseimg_indv[noiseimg_indv < -49] = 0
    noiseimg_indv[noiseimg_indv > 50] = 0
    if unittest != 1:
        img4 = img4+noiseimg_indv
    noiseimg_indv = np.random.normal(mu, sigma, [250, 250])*40
    noiseimg_indv[noiseimg_indv < -49] = 0
    noiseimg_indv[noiseimg_indv > 50] = 0
    if unittest != 1:
        img5 = img5+noiseimg_indv
    noiseimg_indv = np.random.normal(mu, sigma, [250, 250])*40
    noiseimg_indv[noiseimg_indv < -49] = 0
    noiseimg_indv[noiseimg_indv > 50] = 0
    if unittest != 1:
        img6 = img6+noiseimg_indv

    v_v = 10
    v_h = 20
    h_v = 5
    h_h = 7

    img1[0:250, 0:190] = img[10:260, 310:500]
    img2[0:250, 0:250] = img[20:270, 80:330]
    img3[0:250, 150:250] = img[30:280, 0:100]

    img4[0:245, 0:190] = img[255:500, 303:493]
    img5[0:235, 0:250] = img[265:500, 73:323]
    img6[0:225, 157:250] = img[275:500, 0:93]



    img = Image.fromarray(img)

    img1 = Image.fromarray(img1)
    img2 = Image.fromarray(img2)
    img3 = Image.fromarray(img3)
    img4 = Image.fromarray(img4)
    img5 = Image.fromarray(img5)
    img6 = Image.fromarray(img6)

    OB = Image.fromarray(OB)
    DF = Image.fromarray(DF)


    img.save(wd+'/'+unittest_str+'/raw/19000101_Image_0060_reference.tiff')
    img1.save(wd+'/'+unittest_str+'/raw/19000101_Image_0060_0001.tiff')
    img2.save(wd+'/'+unittest_str+'/raw/19000101_Image_0060_0002.tiff')
    img3.save(wd+'/'+unittest_str+'/raw/19000101_Image_0060_0003.tiff')
    img4.save(wd+'/'+unittest_str+'/raw/19000101_Image_0060_0004.tiff')
    img5.save(wd+'/'+unittest_str+'/raw/19000101_Image_0060_0005.tiff')
    img6.save(wd+'/'+unittest_str+'/raw/19000101_Image_0060_0006.tiff')
    OB.save(wd+'/'+unittest_str+'/raw/OB.tiff')
    DF.save(wd+'/'+unittest_str+'/raw/DF.tiff')



    