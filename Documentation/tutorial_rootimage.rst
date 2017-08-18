.. tutorial_rootimage:

***************************
Getting Started: rootimage
***************************

**I. OVERVIEW**

The 'RP_rootimage' analysis creates an image of only root values using the mask and water content images.

**II. HOW TO USE**

First, open the 'user_config' text file in your 'Root_Processing' directory.  The parameters used in 'RP_radwc' are in the 9th section, and there will be three parameters.  In order, they are:

1. wc_filename: this is the full image filename (including directory) where the water content image is to be found.  

2. mask_filename: this is the full image filename (including directory) where the mask image is to be found.

3. output_filename: this is the directory where the outputted files will be saved.

**III. RUNNING THE CODE**

This analysis can be conducted using the ['RP_rootimage'] string in the 'RP_run' module.  