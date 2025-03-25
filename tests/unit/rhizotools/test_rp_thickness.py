#!/usr/bin/env python
"""Tests for the RP_thickness module."""

import os
from typing import Any, Dict

import numpy as np
import pytest
from PIL import Image

from rhizotools.RP_thickness import RP_thickness


def test_missing_input_file(temp_data_dir: str) -> None:
    """Test that RP_thickness raises an error when the input file is missing."""
    # Setup parameters with a non-existent input file
    parameters: Dict[str, Any] = {
        "image_filename": os.path.join(temp_data_dir, "nonexistent.tiff"),
        "output_filename": os.path.join(temp_data_dir, "output_thickness.tiff"),
    }

    # Check that it raises a ValueError
    with pytest.raises(ValueError, match="Input files are not present"):
        RP_thickness(parameters)


def test_simple_thickness_calculation(temp_data_dir: str) -> None:
    """Test thickness calculation with a simple cylindrical root."""
    # Create a test image with a simple root structure (a circle)
    img_size = 100
    test_img = np.zeros((img_size, img_size), dtype=np.uint8)

    # Create a circular root
    center_x, center_y = img_size // 2, img_size // 2
    radius = 20
    for i in range(img_size):
        for j in range(img_size):
            if (i - center_y) ** 2 + (j - center_x) ** 2 < radius**2:
                test_img[i, j] = 1

    img_path = os.path.join(temp_data_dir, "circular_root.tiff")
    Image.fromarray(test_img).save(img_path)

    output_path = os.path.join(temp_data_dir, "thickness_map.tiff")

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path,
    }

    # Run the thickness calculation
    RP_thickness(parameters)

    # Check that the output file was created
    assert os.path.isfile(output_path), "Output thickness map file was not created"

    # Load the output thickness map
    thickness_map = np.array(Image.open(output_path))

    # Basic verification:
    # 1. The thickness map should have the same dimensions as the input
    assert thickness_map.shape == test_img.shape, "Thickness map has incorrect dimensions"

    # 2. For a circle, the maximum thickness should be approximately the radius
    # Allow some tolerance due to discretization and pixel-based calculations
    max_thickness = np.max(thickness_map)
    assert radius * 0.8 <= max_thickness <= radius * 1.2, (
        f"Expected max thickness close to {radius}, got {max_thickness}"
    )

    # 3. Check that the thickness decreases from the center to the edges
    # Get a horizontal slice through the center

    # Verify that the thickness generally decreases from center to edges
    center_value = thickness_map[center_y, center_x]
    edge_values = thickness_map[center_y, [center_x - radius + 2, center_x + radius - 2]]

    assert center_value > np.mean(edge_values), "Thickness does not decrease from center to edges"


def test_rectangular_root_thickness(temp_data_dir: str) -> None:
    """Test thickness calculation with a rectangular root."""
    # Create a test image with a rectangular root
    img_size = 100
    test_img = np.zeros((img_size, img_size), dtype=np.uint8)

    # Create a rectangular root
    rect_width = 10
    rect_height = 50
    start_x = (img_size - rect_width) // 2
    start_y = (img_size - rect_height) // 2

    test_img[start_y : start_y + rect_height, start_x : start_x + rect_width] = 1

    img_path = os.path.join(temp_data_dir, "rectangular_root.tiff")
    Image.fromarray(test_img).save(img_path)

    output_path = os.path.join(temp_data_dir, "rectangular_thickness.tiff")

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path,
    }

    # Run the thickness calculation
    RP_thickness(parameters)

    # Load the output thickness map
    thickness_map = np.array(Image.open(output_path))

    # Basic verification:
    # 1. For a rectangle, the maximum thickness should be close to half the width
    max_thickness = np.max(thickness_map)
    expected_max = rect_width / 2
    assert expected_max * 0.8 <= max_thickness <= expected_max * 1.2, (
        f"Expected max thickness close to {expected_max}, got {max_thickness}"
    )

    # 2. Check the center of the rectangle
    center_y, center_x = img_size // 2, img_size // 2
    center_thickness = thickness_map[center_y, center_x]
    assert center_thickness > 0, "Center of rectangle has zero thickness"


def test_complex_root_structure(temp_data_dir: str) -> None:
    """Test thickness calculation with a more complex root structure (cross-shaped)."""
    # Create a test image with a cross-shaped root
    img_size = 100
    test_img = np.zeros((img_size, img_size), dtype=np.uint8)

    # Create a cross-shaped root
    center = img_size // 2
    thickness = 10

    # Horizontal line
    for i in range(center - thickness // 2, center + thickness // 2):
        for j in range(img_size):
            test_img[i, j] = 1

    # Vertical line
    for i in range(img_size):
        for j in range(center - thickness // 2, center + thickness // 2):
            test_img[i, j] = 1

    img_path = os.path.join(temp_data_dir, "cross_root.tiff")
    Image.fromarray(test_img).save(img_path)

    output_path = os.path.join(temp_data_dir, "cross_thickness.tiff")

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": img_path,
        "output_filename": output_path,
    }

    # Run the thickness calculation
    RP_thickness(parameters)

    # Load the output thickness map
    thickness_map = np.array(Image.open(output_path))

    # Basic verification:
    # 1. The center of the cross should have higher thickness value due to the intersection
    center_thickness = thickness_map[center, center]
    assert center_thickness > 0, "Center of cross has zero thickness"

    # 2. Check points along the arms of the cross
    # Take points 20 pixels away from the center along each arm
    arm_points = [
        (center, center + 20),  # right arm
        (center, center - 20),  # left arm
        (center + 20, center),  # bottom arm
        (center - 20, center),  # top arm
    ]

    for point in arm_points:
        assert thickness_map[point] > 0, f"Arm point {point} has zero thickness"
