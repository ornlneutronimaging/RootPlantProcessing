[![Build Status](https://travis-ci.org/kdecarlo/CG1D_rhizotools.svg?branch=master)](https://travis-ci.org/kdecarlo/CG1D_rootprocessing)
[![codecov](https://codecov.io/gh/kdecarlo/Root_Processing/branch/master/graph/badge.svg)](https://codecov.io/gh/kdecarlo/Root_Processing)
[![Documentation Status](https://readthedocs.org/projects/rootplotprocessing/badge/?version=latest)](http://rootplotprocessing.readthedocs.io/en/latest/?badge=latest)

# Root Processing**

This is the root processing suite, rhizotools (`rhizo` means "root related"), for images at the ORNL MARS (formerly CG-1D) beamline.
<!-- Please visit [https://kdecarlo.github.io/Root_Processing/](https://kdecarlo.github.io/Root_Processing/) for full documentation. -->

## Quick Start

## Development Guide

## How to Use

<!-- Running the suite on the sample data provided::

	#Importing sample dataset
	wd = '/Users/...'  #Specify where you saved your sample data
	from rhizotools.sampledata import sampledata
	sampledata(wd)

	#Running Code - Default Settings
	from rhizotools.RP_run import RP_run
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
	RP_run(wd, wd_userconfig, analysis_list) -->

## Known issue

1. When using `pixi install` for the first time, you might see the following error messages. The solutions is to increase your file limit with `ulimit -n 65535` and then run `pixi install` again.

```bash
Too many open files (os error 24) at path
```
