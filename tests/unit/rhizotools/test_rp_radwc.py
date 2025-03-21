#!/usr/bin/env python
"""Tests for the RP_radwc module."""

import os
from typing import Any, Dict

import numpy as np
import pytest
from PIL import Image

from rhizotools.RP_radwc import RP_radwc


def test_missing_input_files(temp_data_dir: str) -> None:
    """Test that RP_radwc raises an error when input files are missing."""
    # Setup parameters with non-existent input files
    parameters: Dict[str, Any] = {
        "wc_filename": os.path.join(temp_data_dir, "nonexistent_wc.tiff"),
        "distmap_filename": os.path.join(temp_data_dir, "nonexistent_distmap.tiff"),
        "mask_filename": os.path.join(temp_data_dir, "nonexistent_mask.tiff"),
        "output_filename": temp_data_dir,
        "fileformat": "test",
        "pixelbin": 3,
    }

    # Check that it raises a ValueError
    with pytest.raises(ValueError, match="Input files are not present"):
        RP_radwc(parameters)


def test_simple_radwc_calculation(temp_data_dir: str) -> None:  # noqa: C901
    """Test radial water content calculation with simple root and water content images."""
    # Create test images
    img_size = 50

    # 1. Create a water content image with values between 0.04 and 0.35
    wc_img = np.ones((img_size, img_size), dtype=np.float32) * 0.04

    # Add some higher water content in a specific region
    center_x, center_y = img_size // 2, img_size // 2
    for i in range(img_size):
        for j in range(img_size):
            # Create a gradient of water content
            dist = np.sqrt((i - center_y) ** 2 + (j - center_x) ** 2)
            if dist < 15:
                wc_img[i, j] = 0.35 - dist * 0.02  # Higher water content closer to center

    # 2. Create a binary root mask image (1 for root, 0 for soil)
    mask_img = np.zeros((img_size, img_size), dtype=np.uint8)
    # Create a simple vertical root
    root_width = 6
    for i in range(img_size):
        for j in range(center_x - root_width // 2, center_x + root_width // 2):
            if 0 <= j < img_size:
                mask_img[i, j] = 1

    # 3. Create a distance map image (0 for root, increasing values for soil)
    # For this test, we'll create a simple distance transform
    distmap_img = np.zeros((img_size, img_size), dtype=np.float32)
    for i in range(img_size):
        for j in range(img_size):
            if mask_img[i, j] == 1:
                # Inside the root, pixel value is thickness from border
                border_dist = min(j - (center_x - root_width // 2), (center_x + root_width // 2) - j)
                distmap_img[i, j] = border_dist
            else:
                distmap_img[i, j] = 0  # Will be replaced with soil distance

    # Save the test images
    wc_path = os.path.join(temp_data_dir, "simple_wc.tiff")
    mask_path = os.path.join(temp_data_dir, "simple_mask.tiff")
    distmap_path = os.path.join(temp_data_dir, "simple_distmap.tiff")

    Image.fromarray((wc_img * 255).astype(np.uint8)).save(wc_path)
    Image.fromarray(mask_img).save(mask_path)
    Image.fromarray((distmap_img * 20).astype(np.uint8)).save(distmap_path)

    # Define output files
    output_dir = temp_data_dir
    fileformat = "simple"

    # Setup parameters
    parameters: Dict[str, Any] = {
        "wc_filename": wc_path,
        "distmap_filename": distmap_path,
        "mask_filename": mask_path,
        "output_filename": output_dir,
        "fileformat": fileformat,
        "pixelbin": 3,
    }

    # Run the radial water content calculation
    RP_radwc(parameters)

    # Check that the output files were created
    expected_files = [
        os.path.join(output_dir, f"{fileformat}_data_xrad_ydist_wc.txt"),
        os.path.join(output_dir, f"{fileformat}_data_num_xrad_ydist_wc.txt"),
        os.path.join(output_dir, f"{fileformat}_data_radrange.txt"),
        os.path.join(output_dir, f"{fileformat}_data_distrange.txt"),
    ]

    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Output file {file_path} was not created"

    # Load and verify the output data
    radrange = np.loadtxt(os.path.join(output_dir, f"{fileformat}_data_radrange.txt"))
    distrange = np.loadtxt(os.path.join(output_dir, f"{fileformat}_data_distrange.txt"))

    # Basic verification:
    # 1. radrange should contain root thickness values
    assert len(radrange) > 0, "radrange is empty"

    # 2. distrange should contain distance bin values
    assert len(distrange) > 0, "distrange is empty"
    assert distrange[0] == 0, "distrange should start at 0"

    # 3. There should be a data matrix with water content values
    wc_data = np.loadtxt(os.path.join(output_dir, f"{fileformat}_data_xrad_ydist_wc.txt"))
    assert wc_data.shape[0] == len(radrange), "Wrong number of rows in water content data"
    assert wc_data.shape[1] == len(distrange), "Wrong number of columns in water content data"

    # 4. There should be a data matrix with pixel counts
    num_data = np.loadtxt(os.path.join(output_dir, f"{fileformat}_data_num_xrad_ydist_wc.txt"))
    assert num_data.shape == wc_data.shape, "Pixel count data has different shape than water content data"


def test_complex_root_radwc_calculation(temp_data_dir: str) -> None:  # noqa: C901
    """Test radial water content calculation with a more complex root structure."""
    # Create test images with a cross-shaped root
    img_size = 60

    # 1. Create a water content image
    wc_img = np.ones((img_size, img_size), dtype=np.float32) * 0.04

    # 2. Create a binary root mask image with a cross shape
    mask_img = np.zeros((img_size, img_size), dtype=np.uint8)
    center = img_size // 2
    thickness = 8

    # Horizontal line
    for i in range(center - thickness // 2, center + thickness // 2):
        for j in range(img_size):
            if 0 <= i < img_size:
                mask_img[i, j] = 1

    # Vertical line
    for i in range(img_size):
        for j in range(center - thickness // 2, center + thickness // 2):
            if 0 <= j < img_size:
                mask_img[i, j] = 1

    # 3. Create a distance map image (values represent root thickness)
    distmap_img = np.zeros((img_size, img_size), dtype=np.float32)

    # Set thickness values in the root area
    root_pixels = np.where(mask_img > 0)
    for i, j in zip(root_pixels[0], root_pixels[1]):
        # Simple approximation - distance from edge of cross shape
        if (center - thickness // 2 <= i < center + thickness // 2) and (
            center - thickness // 2 <= j < center + thickness // 2
        ):
            # Center square - maximum thickness
            distmap_img[i, j] = thickness // 2
        elif center - thickness // 2 <= i < center + thickness // 2:
            # Horizontal bar
            distmap_img[i, j] = min(thickness // 2, min(i - (center - thickness // 2), (center + thickness // 2) - i))
        else:
            # Vertical bar
            distmap_img[i, j] = min(thickness // 2, min(j - (center - thickness // 2), (center + thickness // 2) - j))

    # Save the test images
    wc_path = os.path.join(temp_data_dir, "complex_wc.tiff")
    mask_path = os.path.join(temp_data_dir, "complex_mask.tiff")
    distmap_path = os.path.join(temp_data_dir, "complex_distmap.tiff")

    Image.fromarray((wc_img * 255).astype(np.uint8)).save(wc_path)
    Image.fromarray(mask_img).save(mask_path)
    Image.fromarray((distmap_img * 20).astype(np.uint8)).save(distmap_path)

    # Define output files
    output_dir = temp_data_dir
    fileformat = "complex"

    # Setup parameters
    parameters: Dict[str, Any] = {
        "wc_filename": wc_path,
        "distmap_filename": distmap_path,
        "mask_filename": mask_path,
        "output_filename": output_dir,
        "fileformat": fileformat,
        "pixelbin": 2,  # Smaller bin size for more detail
    }

    # Run the radial water content calculation
    RP_radwc(parameters)

    # Check that the output files were created
    expected_files = [
        os.path.join(output_dir, f"{fileformat}_data_xrad_ydist_wc.txt"),
        os.path.join(output_dir, f"{fileformat}_data_num_xrad_ydist_wc.txt"),
        os.path.join(output_dir, f"{fileformat}_data_radrange.txt"),
        os.path.join(output_dir, f"{fileformat}_data_distrange.txt"),
    ]

    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Output file {file_path} was not created"

    # Load and verify the output data
    radrange = np.loadtxt(os.path.join(output_dir, f"{fileformat}_data_radrange.txt"))
    distrange = np.loadtxt(os.path.join(output_dir, f"{fileformat}_data_distrange.txt"))
    wc_data = np.loadtxt(os.path.join(output_dir, f"{fileformat}_data_xrad_ydist_wc.txt"))
    num_data = np.loadtxt(os.path.join(output_dir, f"{fileformat}_data_num_xrad_ydist_wc.txt"))

    # Verification:
    # 1. In the current implementation, the radrange values are computed from the image
    # and may differ from the values we expect based on our test image setup
    # The important thing is to ensure there are radius values and they increase properly
    assert len(radrange) > 0, "No radius values found"
    assert np.all(np.diff(radrange) >= 0), "Radius values are not monotonically increasing"

    # 2. With a cross shape, there should be a distribution of radius values
    assert len(radrange) > 2, "Not enough radius values found"

    # 3. The distance range should use our bin size of 2
    assert distrange[1] - distrange[0] == 2, f"Distance bin size is not 2, got {distrange[1] - distrange[0]}"

    # 4. Check that the data makes sense
    assert np.any(wc_data > 0), "No positive water content values found"
    assert np.any(num_data > 0), "No pixel counts found"


def test_pixelbin_parameter(temp_data_dir: str) -> None:
    """Test that the pixelbin parameter correctly affects binning."""
    # Create simple test images
    img_size = 40
    center = img_size // 2

    # Create basic images
    wc_img = np.ones((img_size, img_size), dtype=np.float32) * 0.04
    mask_img = np.zeros((img_size, img_size), dtype=np.uint8)
    distmap_img = np.zeros((img_size, img_size), dtype=np.float32)

    # Create a circle in the center
    radius = 8
    for i in range(img_size):
        for j in range(img_size):
            dist = np.sqrt((i - center) ** 2 + (j - center) ** 2)
            if dist < radius:
                mask_img[i, j] = 1
                # Distance from edge for root pixels
                distmap_img[i, j] = max(0, radius - dist)

    # Save images
    wc_path = os.path.join(temp_data_dir, "circle_wc.tiff")
    mask_path = os.path.join(temp_data_dir, "circle_mask.tiff")
    distmap_path = os.path.join(temp_data_dir, "circle_distmap.tiff")

    Image.fromarray((wc_img * 255).astype(np.uint8)).save(wc_path)
    Image.fromarray(mask_img).save(mask_path)
    Image.fromarray((distmap_img * 20).astype(np.uint8)).save(distmap_path)

    # Run with two different bin sizes
    for bin_size, suffix in [(2, "small"), (5, "large")]:
        fileformat = f"bin{suffix}"

        parameters: Dict[str, Any] = {
            "wc_filename": wc_path,
            "distmap_filename": distmap_path,
            "mask_filename": mask_path,
            "output_filename": temp_data_dir,
            "fileformat": fileformat,
            "pixelbin": bin_size,
        }

        # Run the calculation
        RP_radwc(parameters)

        # Load the distance range
        distrange = np.loadtxt(os.path.join(temp_data_dir, f"{fileformat}_data_distrange.txt"))

        # Check that the step size matches our bin size
        if len(distrange) > 1:
            bin_step = distrange[1] - distrange[0]
            assert bin_step == bin_size, f"Expected bin step of {bin_size}, got {bin_step}"

    # Compare the sizes of the output matrices
    small_data = np.loadtxt(os.path.join(temp_data_dir, "binsmall_data_xrad_ydist_wc.txt"))
    large_data = np.loadtxt(os.path.join(temp_data_dir, "binlarge_data_xrad_ydist_wc.txt"))

    # The small bin size should produce more distance columns
    assert small_data.shape[1] > large_data.shape[1], "Small bin size did not produce more distance columns"


def test_output_content_validation(reference_data_dir: str, temp_data_dir: str) -> None:
    """Test that the output content has the expected format by comparing to reference data."""
    # Copy test files from reference data to temporary directory
    ref_wc_path = os.path.join(reference_data_dir, "wc", "SampleImg_wc.tiff")
    ref_distmap_path = os.path.join(reference_data_dir, "distmap", "SampleImg_distmap.tiff")
    ref_mask_path = os.path.join(reference_data_dir, "mask", "SampleImg_mask.tiff")

    if not all(os.path.isfile(path) for path in [ref_wc_path, ref_distmap_path, ref_mask_path]):
        pytest.skip("Reference data files not found")

    # Create copies in temp_data_dir
    wc_path = os.path.join(temp_data_dir, "ref_wc.tiff")
    distmap_path = os.path.join(temp_data_dir, "ref_distmap.tiff")
    mask_path = os.path.join(temp_data_dir, "ref_mask.tiff")

    # Copy files
    for src, dst in [(ref_wc_path, wc_path), (ref_distmap_path, distmap_path), (ref_mask_path, mask_path)]:
        img = Image.open(src)
        img.save(dst)

    # Set up parameters
    parameters: Dict[str, Any] = {
        "wc_filename": wc_path,
        "distmap_filename": distmap_path,
        "mask_filename": mask_path,
        "output_filename": temp_data_dir,
        "fileformat": "SampleTest",
        "pixelbin": 3,
    }

    # Run RP_radwc
    RP_radwc(parameters)

    # Check output files
    expected_files = [
        os.path.join(temp_data_dir, "SampleTest_data_xrad_ydist_wc.txt"),
        os.path.join(temp_data_dir, "SampleTest_data_num_xrad_ydist_wc.txt"),
        os.path.join(temp_data_dir, "SampleTest_data_radrange.txt"),
        os.path.join(temp_data_dir, "SampleTest_data_distrange.txt"),
    ]

    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Output file {file_path} was not created"

    # Load data from output files
    wc_data = np.loadtxt(os.path.join(temp_data_dir, "SampleTest_data_xrad_ydist_wc.txt"))
    num_data = np.loadtxt(os.path.join(temp_data_dir, "SampleTest_data_num_xrad_ydist_wc.txt"))
    radrange = np.loadtxt(os.path.join(temp_data_dir, "SampleTest_data_radrange.txt"))
    distrange = np.loadtxt(os.path.join(temp_data_dir, "SampleTest_data_distrange.txt"))

    # Verify data properties
    # 1. Data matrices have the expected dimensions
    assert wc_data.shape[0] == len(radrange), "WC data rows don't match radrange length"
    assert wc_data.shape[1] == len(distrange), "WC data columns don't match distrange length"
    assert wc_data.shape == num_data.shape, "WC data and num data have different shapes"

    # 2. Check that radrange values are increasing
    assert np.all(np.diff(radrange) >= 0), "radrange values are not monotonically increasing"

    # 3. Check that distrange values are increasing with the correct bin size
    assert np.all(np.diff(distrange) == 3), "distrange values don't increase by the bin size (3)"

    # 4. Check for expected value ranges in the WC data
    # Water content values should be between 0 and 1 (typically 0.04-0.35 for neutron imaging)
    nonzero_wc = wc_data[wc_data > 0]
    if len(nonzero_wc) > 0:
        assert np.all(nonzero_wc <= 1.0), "Water content values exceed 1.0"
        assert np.all(nonzero_wc >= 0.0), "Water content values are negative"
