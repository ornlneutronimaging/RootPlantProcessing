.. tutorial_radwc:

************************
Getting Started: radwc
************************

**I. OVERVIEW**

The 'RP_radwc' analysis creates two size NxM text files: (1) the water content of a given root radius (row) at a given distance from the root (column), and (2) the number of pixels analyzed for each entry.  The analysis also outputs a size 1xN and 1xM text file of the root radius values and distance from the root, respectively.  All distance and radius values are outputted in terms of pixels.

In calculating the water content, for each entry of radius i and distance j, this analysis takes the mean value of all pixels that fit these criteria.  

**II. HOW TO USE**

First, open the 'user_config' text file in your 'Root_Processing' directory.  The parameters used in 'RP_radwc' are in the 7th section, and there will be six parameters.  In order, they are:

1. wc_filename: this is the full image filename (including directory) where the water content image is to be found.  

2. distmap_filename: this is the full image filename (including directory) where the image outputted from 'RP_distmap' is to be found.

3. mask_filename: this is the full image filename (including directory) where the mask image is to be found.

4. output_filename: this is the directory where the outputted files will be saved.

5. fileformat: this is the file prefix that will be attached to the four files outputted by this analysis.  So, for example, if 'fileformat' is set as 'SampleImg', then the 4 files outputted will be:

    - 'SampleImg_data_distrange.txt': 1xM text file of distance from the root
    - 'SampleImg_data_num_xrad_ydist_wc.txt': NxM text file of number of pixels analyzed
    - 'SampleImg_data_radrange.txt':1xN text file of root radii analyzed
    - 'SampleImg_data_xrad_ydist_wc.txt': NxM text file of mean water content for each root radius at a given distance

6. pixelbin: the number of pixels to be binned along the 'distance from root' axis when determining water content

**III. RUNNING THE CODE**

This analysis can be conducted using the ['RP_radwc'] string in the 'RP_run' module.  