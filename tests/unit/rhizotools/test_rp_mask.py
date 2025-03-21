#!/usr/bin/env python
"""Tests for the RP_mask module."""

import os
from typing import Any, Dict

import numpy as np
import pytest
from PIL import Image

from rhizotools.RP_mask import RP_mask


def test_missing_input_file(temp_data_dir: str) -> None:
    """Test that RP_mask raises an error when the input file is missing."""
    # Setup parameters with a non-existent input file
    parameters: Dict[str, Any] = {
        "image_filename": os.path.join(temp_data_dir, "nonexistent.tiff"),
        "output_filename": os.path.join(temp_data_dir, "output_mask.tiff"),
        "windowsize": 101,
        "threshold": 0.05,
        "globthresh": 0.3,
    }

    # Check that it raises a ValueError
    with pytest.raises(ValueError, match="Crop file not found"):
        RP_mask(parameters)


def test_window_size_too_large(temp_data_dir: str) -> None:
    """Test that RP_mask raises an error when the window size is larger than the image."""
    # Create a small test image
    small_img = np.ones((50, 50), dtype=np.float32)
    img_path = os.path.join(temp_data_dir, "small_image.tiff")
    Image.fromarray(small_img).save(img_path)

    # Setup parameters with a window size larger than the image
    parameters: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": os.path.join(temp_data_dir, "output_mask.tiff"),
        "windowsize": 101,  # Larger than 50x50
        "threshold": 0.05,
        "globthresh": 0.3,
    }

    # Check that it raises a ValueError
    with pytest.raises(ValueError, match="Image is too small"):
        RP_mask(parameters)


def test_normal_mask_creation(temp_data_dir: str) -> None:
    """Test normal mask creation with default parameters."""
    # Create a test image with a dark center region
    img_size = 101
    test_img = np.ones((img_size, img_size), dtype=np.float32)
    # Create a dark region in the center (simulating a root)
    center = img_size // 2
    radius = 10
    for i in range(img_size):
        for j in range(img_size):
            if (i - center) ** 2 + (j - center) ** 2 < radius**2:
                test_img[i, j] = 0.1  # Dark pixel (root)

    img_path = os.path.join(temp_data_dir, "test_image.tiff")
    Image.fromarray(test_img).save(img_path)

    output_path = os.path.join(temp_data_dir, "output_mask.tiff")

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path,
        "windowsize": 21,  # Smaller window for faster test
        "threshold": 0.05,
        "globthresh": 0.3,
    }

    # Run the mask function
    RP_mask(parameters)

    # Check that the output file was created
    assert os.path.isfile(output_path), "Output mask file was not created"

    # Load and check the output mask
    mask = np.array(Image.open(output_path))

    # Verify that the dark center region was detected as a root (value = 1)
    # At least some pixels in the center should be marked as roots
    center_mask = mask[center - 5 : center + 5, center - 5 : center + 5]
    assert np.sum(center_mask) > 0, "No root pixels detected in the center"


def test_global_threshold(temp_data_dir: str) -> None:
    """Test that pixels below global threshold are automatically marked as roots."""
    # Create a test image with a very dark region
    img_size = 101
    test_img = np.ones((img_size, img_size), dtype=np.float32) * 0.8  # Light background

    # Create a very dark region in the center (below global threshold)
    center = img_size // 2
    radius = 10
    for i in range(img_size):
        for j in range(img_size):
            if (i - center) ** 2 + (j - center) ** 2 < radius**2:
                test_img[i, j] = 0.1  # Very dark pixel (well below globthresh)

    img_path = os.path.join(temp_data_dir, "global_thresh_test.tiff")
    Image.fromarray(test_img).save(img_path)

    output_path = os.path.join(temp_data_dir, "global_thresh_mask.tiff")

    # Setup parameters with high threshold but keeping globthresh
    parameters: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path,
        "windowsize": 21,
        "threshold": 0.2,  # Higher threshold makes it harder to detect roots
        "globthresh": 0.2,  # But dark regions below this are automatically roots
    }

    # Run the mask function
    RP_mask(parameters)

    # Load the output mask
    mask = np.array(Image.open(output_path))

    # Verify that the dark center region was detected due to global threshold
    center_mask = mask[center - 5 : center + 5, center - 5 : center + 5]
    assert np.sum(center_mask) > 0, "Global threshold did not detect dark pixels"
