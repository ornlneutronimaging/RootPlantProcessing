# Root Processing

This is the root processing suite, rhizotools (`rhizo` means "root related"), for images at the ORNL MARS (formerly CG-1D) beamline.
<!-- Please visit [https://kdecarlo.github.io/Root_Processing/](https://kdecarlo.github.io/Root_Processing/) for full documentation. -->

## Quick Start

### Installation

#### Using Pip

```bash
pip install rhizotools
```

#### Using Pixi (Recommended)

```bash
# Install pixi if you don't have it already
curl -fsSL https://pixi.sh/install.sh | bash

# Create a new environment with rhizotools
pixi init --name my-rhizo-project
cd my-rhizo-project
pixi add rhizotools

# Activate the environment
pixi shell
```

#### Using Conda

```bash
conda install -c conda-forge rhizotools
```

## Development Guide

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/ornlneutronimaging/RootPlantProcessing.git
cd RootPlantProcessing

# Set up development environment with pixi
pixi install

# Activate the environment
pixi shell
```

### Development Workflow

```bash
# Run tests
pixi run test

# Run linting checks
pixi run ruff check .

# Format code
pixi run ruff format .

# Build the package
pixi run build-pypi

# Build documentation
pixi run build-docs
```

### Adding Dependencies

To add new dependencies:

1. Add Python dependencies to `[project.dependencies]` in `pyproject.toml`
1. Add pixi/conda dependencies to `[tool.pixi.dependencies]` in `pyproject.toml` 
1. Run `pixi install` to update your environment

## How to Use

```python
# Importing sample dataset
wd = '/Users/...'  # Specify where you saved your sample data
from rhizotools.sampledata import sampledata
sampledata(wd)

# Running Code - Default Settings
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
wd_userconfig = wd+'/Sample_Data'  # Specify where you saved your user_config file
RP_run(wd, wd_userconfig, analysis_list)
```

## Known issue

1. When using `pixi install` for the first time, you might see the following error messages. The solutions is to increase your file limit with `ulimit -n 65535` and then run `pixi install` again.

```bash
Too many open files (os error 24) at path
```
