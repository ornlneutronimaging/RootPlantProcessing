#!/usr/bin/env python
"""Tests for the RP_imagefilter module."""

import os
from typing import Any, Dict

import numpy as np
import pytest
from PIL import Image

from rhizotools.RP_imagefilter import RP_imagefilter


def test_missing_input_file(temp_data_dir: str) -> None:
    """Test that RP_imagefilter raises an error when the input file is missing."""
    # Setup parameters with a non-existent input file
    parameters: Dict[str, Any] = {
        "image_filename": os.path.join(temp_data_dir, "nonexistent.tiff"),
        "output_filename": os.path.join(temp_data_dir, "output_filtered.tiff"),
        "bwareaval": 800,
        "medfilterval": 5,
    }

    # Check that it raises a ValueError
    with pytest.raises(ValueError, match="mask file not found"):
        RP_imagefilter(parameters)


def test_normal_filtering(temp_data_dir: str) -> None:
    """Test normal image filtering with default parameters."""
    # Create a test binary mask with different sized objects
    img_size = 100
    test_img = np.zeros((img_size, img_size), dtype=np.uint8)

    # Create a large object (should be kept)
    center_large = img_size // 2
    radius_large = 20
    for i in range(img_size):
        for j in range(img_size):
            if (i - center_large) ** 2 + (j - center_large) ** 2 < radius_large**2:
                test_img[i, j] = 1

    # Create a small object (should be removed)
    center_small_x, center_small_y = img_size // 4, img_size // 4
    radius_small = 5
    for i in range(img_size):
        for j in range(img_size):
            if (i - center_small_x) ** 2 + (j - center_small_y) ** 2 < radius_small**2:
                test_img[i, j] = 1

    img_path = os.path.join(temp_data_dir, "test_mask.tiff")
    Image.fromarray(test_img).save(img_path)

    output_path = os.path.join(temp_data_dir, "output_filtered.tiff")

    # Setup parameters - bwareaval set to remove the small object
    parameters: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path,
        "bwareaval": 200,  # Small object should be below this threshold
        "medfilterval": 3,
    }

    # Run the filter function
    RP_imagefilter(parameters)

    # Check that the output file was created
    assert os.path.isfile(output_path), "Output filtered file was not created"

    # Load and check the output filtered image
    filtered_img = np.array(Image.open(output_path))

    # Verify that the large object was kept
    center_region = filtered_img[center_large - 10 : center_large + 10, center_large - 10 : center_large + 10]
    assert np.sum(center_region) > 0, "Large object was incorrectly removed"

    # Verify that the small object was removed
    small_region = filtered_img[center_small_x - 6 : center_small_x + 6, center_small_y - 6 : center_small_y + 6]
    assert np.sum(small_region) == 0, "Small object was not removed"


def test_keep_all_objects(temp_data_dir: str) -> None:
    """Test that setting bwareaval to 0 keeps all objects."""
    # Create a test binary mask with different sized objects
    img_size = 100
    test_img = np.zeros((img_size, img_size), dtype=np.uint8)

    # Create a large object
    center_large = img_size // 2
    radius_large = 20
    for i in range(img_size):
        for j in range(img_size):
            if (i - center_large) ** 2 + (j - center_large) ** 2 < radius_large**2:
                test_img[i, j] = 1

    # Create a small object
    center_small_x, center_small_y = img_size // 4, img_size // 4
    radius_small = 5
    for i in range(img_size):
        for j in range(img_size):
            if (i - center_small_x) ** 2 + (j - center_small_y) ** 2 < radius_small**2:
                test_img[i, j] = 1

    img_path = os.path.join(temp_data_dir, "test_mask_all.tiff")
    Image.fromarray(test_img).save(img_path)

    output_path = os.path.join(temp_data_dir, "output_filtered_all.tiff")

    # Setup parameters - bwareaval set to 0 to keep all objects
    parameters: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path,
        "bwareaval": 0,  # Should keep all objects
        "medfilterval": 3,
    }

    # Run the filter function
    RP_imagefilter(parameters)

    # Load and check the output filtered image
    filtered_img = np.array(Image.open(output_path))

    # Verify that the large object was kept
    center_region = filtered_img[center_large - 10 : center_large + 10, center_large - 10 : center_large + 10]
    assert np.sum(center_region) > 0, "Large object was incorrectly removed"

    # Verify that the small object was also kept
    small_region = filtered_img[center_small_x - 6 : center_small_x + 6, center_small_y - 6 : center_small_y + 6]
    assert np.sum(small_region) > 0, "Small object was incorrectly removed"


def test_median_filter_effect(temp_data_dir: str) -> None:
    """Test the effect of different median filter values."""
    # Create a test binary mask with noise
    img_size = 100
    test_img = np.zeros((img_size, img_size), dtype=np.uint8)

    # Create a simple object with salt and pepper noise
    center = img_size // 2
    radius = 20
    np.random.seed(42)  # For reproducibility

    for i in range(img_size):
        for j in range(img_size):
            if (i - center) ** 2 + (j - center) ** 2 < radius**2:
                test_img[i, j] = 1

    # Add noise inside and outside the object
    noise_mask = np.random.random(test_img.shape) > 0.9  # 10% noise
    test_img = np.logical_xor(test_img, noise_mask).astype(np.uint8)

    img_path = os.path.join(temp_data_dir, "test_noisy_mask.tiff")
    Image.fromarray(test_img).save(img_path)

    output_path1 = os.path.join(temp_data_dir, "output_filtered_small_kernel.tiff")
    output_path2 = os.path.join(temp_data_dir, "output_filtered_large_kernel.tiff")

    # Setup parameters with small median filter
    parameters1: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path1,
        "bwareaval": 10,  # Remove very small noise
        "medfilterval": 3,  # Small median filter
    }

    # Setup parameters with large median filter
    parameters2: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path2,
        "bwareaval": 10,  # Same as above
        "medfilterval": 7,  # Larger median filter
    }

    # Run the filter function for both parameter sets
    RP_imagefilter(parameters1)
    RP_imagefilter(parameters2)

    # Load filtered images
    filtered_img1 = np.array(Image.open(output_path1))
    filtered_img2 = np.array(Image.open(output_path2))

    # Verify that the larger median filter removes more noise
    # Total count in original noisy image should be higher than filtered images
    assert np.sum(test_img) > np.sum(filtered_img1), "Small median filter didn't reduce noise"
    assert np.sum(filtered_img1) > np.sum(filtered_img2), "Larger median filter didn't reduce more noise"
