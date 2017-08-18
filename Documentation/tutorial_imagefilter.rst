.. tutorial_imagefilter:

*****************************
Getting Started: imagefilter
*****************************

**I. OVERVIEW**

The 'RP_imagefilter' analysis conducts a simple filtering process of an image for later processing.  This is primarily used to 'clean up' the output image from the 'RP_mask' analysis, and as such should be used in parallel.

Two main filters are applied: the first is an area-based filter, where all mask-labeled objects with a connected pixel count smaller than 'bwareaval' will be removed.  The second filter is a simple median filter.  

**II. HOW TO USE**

First, open the 'user_config' text file in your 'Root_Processing' directory.  The parameters used in 'RP_imagefilter' are in the 5th section, and there will be four parameters.  In order, they are:

1. image_filename: this is the full image filename (including directory) where the image is to be found.  

2. output_filename: this is the full image filename (including directory) where the image is to be saved.  If the directory is not present, the analysis will automatically make the directory.  

3. bwareaval: this is the scalar value of the minimum pixel count (i.e. pixel area) to be removed.  

4. medfilterval: this is the window size to be used for the median filter.

**III. RUNNING THE CODE**

This analysis can be conducted using the ['RP_imagefilter'] string in the 'RP_run' module.  