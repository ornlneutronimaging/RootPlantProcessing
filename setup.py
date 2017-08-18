#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
	name = 'rootprocessing',
	version = '1.0.6', 
	author = 'Keita DeCarlo', 
	author_email = 'decarlokd@ornl.gov', 
	packages = find_packages(exclude=['test', 'Notebook_Code']),
	include_package_data = True, 
	test_suite = 'test', 
	install_requires = [
		'numpy', 
		'astropy',
		'scipy',
		'pillow',
		],
		dependency_links = [
		],
		description = 'Root Processing suite for images at the ORNL CG-1D beamline',
		license = 'BSD',
		keywords = 'tiff tif root processing',
		url = 'https://github.com/kdecarlo/CG1D_rootprocessing',
		classifiers = ['Development Status :: 3 - Alpha', 
						'Topic :: Scientific/Engineering :: Physics',
						'Intended Audience :: Developers',
						'Programming Language :: Python :: 2.7',
						'Programming Language :: Python :: 3.4',
						'Programming Language :: Python :: 3.5'],
)
