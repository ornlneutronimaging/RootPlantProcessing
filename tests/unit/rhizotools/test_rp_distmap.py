#!/usr/bin/env python
"""Tests for the RP_distmap module."""

import os
from typing import Any, Dict

import numpy as np
import pytest
from PIL import Image

from rhizotools.RP_distmap import RP_distmap


def test_missing_input_file(temp_data_dir: str) -> None:
    """Test that RP_distmap raises an error when the input file is missing."""
    # Setup parameters with a non-existent input file
    parameters: Dict[str, Any] = {
        "image_filename": os.path.join(temp_data_dir, "nonexistent.tiff"),
        "output_filename": os.path.join(temp_data_dir, "output_distmap.tiff"),
        "maxval": 100,
    }

    # Check that it raises a ValueError
    with pytest.raises(ValueError, match="Binary root image not present"):
        RP_distmap(parameters)


def test_empty_image(temp_data_dir: str) -> None:
    """Test that RP_distmap raises an error when the input image is empty (no masked objects)."""
    # Create an empty test image
    empty_img = np.zeros((100, 100), dtype=np.uint8)
    img_path = os.path.join(temp_data_dir, "empty_image.tiff")
    Image.fromarray(empty_img).save(img_path)

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": os.path.join(temp_data_dir, "output_distmap.tiff"),
        "maxval": 100,
    }

    # Check that it raises a ValueError
    with pytest.raises(ValueError, match="No masked objects present"):
        RP_distmap(parameters)


def test_simple_distmap(temp_data_dir: str) -> None:
    """Test distance map calculation with a simple root-like structure."""
    # Create a test image with a simple root structure
    img_size = 100
    test_img = np.zeros((img_size, img_size), dtype=np.uint8)

    # Create a vertical line (simulating a simple root)
    center_x = img_size // 2
    line_width = 10
    for i in range(img_size):
        for j in range(center_x - line_width // 2, center_x + line_width // 2):
            if 0 <= j < img_size:  # Ensure we stay within bounds
                test_img[i, j] = 1

    img_path = os.path.join(temp_data_dir, "simple_root.tiff")
    Image.fromarray(test_img).save(img_path)

    output_path = os.path.join(temp_data_dir, "simple_distmap.tiff")

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path,
        "maxval": 20,  # Limit distance calculation to nearby soil pixels
    }

    # Run the distance map calculation
    RP_distmap(parameters)

    # Check that the output file was created
    assert os.path.isfile(output_path), "Output distance map file was not created"

    # Load the output distance map
    distmap = np.array(Image.open(output_path))

    # Basic verification:
    # 1. The distance map should have the same dimensions as the input
    assert distmap.shape == test_img.shape, "Distance map has incorrect dimensions"

    # 2. Root pixels should have zero values in the soil contour map
    root_pixels = np.where(test_img > 0)
    assert np.sum(distmap[root_pixels]) == 0, "Root pixels should have zero values in distance map"

    # 3. Non-zero values should exist in the result (soil pixels)
    soil_pixels = np.where((test_img == 0) & (distmap > 0))
    assert len(soil_pixels[0]) > 0, "No soil pixels found in distance map"


def test_complex_root_structure(temp_data_dir: str) -> None:
    """Test distance map calculation with a more complex root structure."""
    # Create a test image with a more complex root structure
    img_size = 100
    test_img = np.zeros((img_size, img_size), dtype=np.uint8)

    # Create a cross-shaped root structure
    center = img_size // 2
    thickness = 6

    # Horizontal line
    for i in range(center - thickness // 2, center + thickness // 2):
        for j in range(img_size):
            test_img[i, j] = 1

    # Vertical line
    for i in range(img_size):
        for j in range(center - thickness // 2, center + thickness // 2):
            test_img[i, j] = 1

    img_path = os.path.join(temp_data_dir, "complex_root.tiff")
    Image.fromarray(test_img).save(img_path)

    output_path = os.path.join(temp_data_dir, "complex_distmap.tiff")

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path,
        "maxval": 30,  # Longer distance to capture more soil pixels
    }

    # Run the distance map calculation
    RP_distmap(parameters)

    # Load the output distance map
    distmap = np.array(Image.open(output_path))

    # Check for expected properties of a cross-shaped root structure:

    # 1. The highest values should be in the corners (furthest from the root)
    # Quadrant 1 (top-right)
    q1 = distmap[5 : center - thickness // 2 - 5, center + thickness // 2 + 5 : img_size - 5]
    # Quadrant 2 (top-left)
    q2 = distmap[5 : center - thickness // 2 - 5, 5 : center - thickness // 2 - 5]
    # Quadrant 3 (bottom-left)
    q3 = distmap[center + thickness // 2 + 5 : img_size - 5, 5 : center - thickness // 2 - 5]
    # Quadrant 4 (bottom-right)
    q4 = distmap[center + thickness // 2 + 5 : img_size - 5, center + thickness // 2 + 5 : img_size - 5]

    # All quadrants should have non-zero values (soil pixels)
    assert np.max(q1) > 0, "No soil pixels found in top-right quadrant"
    assert np.max(q2) > 0, "No soil pixels found in top-left quadrant"
    assert np.max(q3) > 0, "No soil pixels found in bottom-left quadrant"
    assert np.max(q4) > 0, "No soil pixels found in bottom-right quadrant"


def test_maxval_limits_calculation(temp_data_dir: str) -> None:
    """Test that the maxval parameter properly limits distance calculations."""
    # Create a test image with a single root in the center
    img_size = 100
    test_img = np.zeros((img_size, img_size), dtype=np.uint8)

    # Create a small circle in the center
    center = img_size // 2
    radius = 5
    for i in range(img_size):
        for j in range(img_size):
            if (i - center) ** 2 + (j - center) ** 2 < radius**2:
                test_img[i, j] = 1

    img_path = os.path.join(temp_data_dir, "center_root.tiff")
    Image.fromarray(test_img).save(img_path)

    # Create two different output files with different maxval settings
    output_path1 = os.path.join(temp_data_dir, "small_maxval_distmap.tiff")
    output_path2 = os.path.join(temp_data_dir, "large_maxval_distmap.tiff")

    # Setup parameters with a small maxval
    parameters1: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path1,
        "maxval": 10,  # Small distance limit
    }

    # Setup parameters with a larger maxval
    parameters2: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path2,
        "maxval": 40,  # Larger distance limit
    }

    # Run the distance map calculations
    RP_distmap(parameters1)
    RP_distmap(parameters2)

    # Load the output distance maps
    distmap1 = np.array(Image.open(output_path1))
    distmap2 = np.array(Image.open(output_path2))

    # The number of non-zero pixels in distmap2 should be greater than in distmap1
    # due to the larger maxval allowing more soil pixels to be calculated
    nonzero_pixels1 = np.count_nonzero(distmap1)
    nonzero_pixels2 = np.count_nonzero(distmap2)

    assert nonzero_pixels2 > nonzero_pixels1, "Larger maxval did not result in more calculated soil pixels"

    # Calculate the maximum distance value in each distmap
    max_dist1 = np.max(distmap1)
    max_dist2 = np.max(distmap2)

    # The maximum radius value should be about the same (since it depends on root thickness)
    # but the maximum distance from root should be limited by maxval
    assert max_dist1 <= parameters1["maxval"], f"Distance values exceed maxval: {max_dist1} > {parameters1['maxval']}"
    assert max_dist2 <= parameters2["maxval"], f"Distance values exceed maxval: {max_dist2} > {parameters2['maxval']}"
