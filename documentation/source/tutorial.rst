.. tutorial:

****************
Getting Started
****************

**I. SETTING UP**

First, download the 'Root_Processing' library, available on the PyPi website, onto your computer::

    pip install rootprocessing

 

We will then create a fake dataset in order to run and test the analyses.  In your window, type the following::

    import rootprocessing
    wd = '/Users/johnsmith'  #Specify where your data files will be.
    from rootprocessing.sampledata import sampledata
    sampledata(wd)

This will create a 'Sample_Data' subdirectory in your library, which will contain a 'raw' subdirectory with a set of 6 images, as well as a dark field and open beam image.

You will also notice a 'user_config' file created in the 'Sample_Data' file - this contains all the necessary parameters for each of the analyses conducted by this library.  Please check the documentation within each module for details. 

Also, be sure to *only change the entries following the colon for each parameter!*  Do not add any extra lines or modify the headings for each section.  

**II. RUNNING ANALYSES WITH 'RP_RUN'**

From here, we will use the 'RP_run' module, which will act as the top-level program for running any analyses of interest::

    from rootprocessing.RP_run import RP_run

We will then specify the analyses of interest.  You can run these in any order, but make sure that you have the necessary images and analyses completed first.  Below is the suggested order of the analyses::

    analysis_list = ['RP_stitch', 'RP_crop', 'RP_wc', 'RP_mask', 'RP_imagefilter', 'RP_distmap', 'RP_radwc', 'RP_thickness', 'RP_rootimage']

We will also need to specify where the user_config.txt file will be.  In our case, this is the same location as where our data files are::

    wd_userconfig = wd+'/Sample_Data'

Once this is complete, then simply run the module, and the outputted subdirectories/data will automatically be placed in the 'Sample_Data' subdirectory::
	
    RP_run(wd, wd_userconfig, analysis_list)

Specific tutorials for each analysis will be outlined, using the sample dataset provided, so be sure to run that code when following through the guides.



