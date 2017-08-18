[![Build Status](https://travis-ci.org/kdecarlo/CG1D_rootprocessing.svg?branch=master)](https://travis-ci.org/kdecarlo/CG1D_rootprocessing)
[![codecov](https://codecov.io/gh/kdecarlo/Root_Processing/branch/master/graph/badge.svg)](https://codecov.io/gh/kdecarlo/Root_Processing)

********************
**Root Processing**
********************

This is the root processing suite for images at the ORNL CG-1D beamline.  Please visit [https://kdecarlo.github.io/Root_Processing/](https://kdecarlo.github.io/Root_Processing/) for full documentation.

**Example**

Running the suite on the sample data provided::

	#Importing sample dataset
	wd = '/Users/...'  #Specify where you saved your sample data
	from rootprocessing.sampledata import sampledata
	sampledata(wd)

	#Running Code - Default Settings
	from rootprocessing.RP_run import RP_run
	analysis_list = [
		'RP_stitch',
		'RP_crop',
		'RP_wc',
		'RP_mask',
		'RP_imagefilter',
		'RP_distmap',
		'RP_radwc',
		'RP_thickness',
		'RP_rootimage',
		]
	wd_userconfig = wd+'/Sample_Data'	#Specify where you saved your user_config file - in case of sample dataset, it is saved together with the data directory
	RP_run(wd, wd_userconfig, analysis_list)

