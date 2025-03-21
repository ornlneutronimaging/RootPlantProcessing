import os
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np
import pytest
from PIL import Image

from rhizotools.RP_crop import RP_crop


def test_missing_input_file(temp_data_dir: str) -> None:
    """Test that ValueError is raised when input file is missing."""
    # Setup directory structure
    stitched_dir: str = os.path.join(temp_data_dir, "stitched")
    crop_dir: str = os.path.join(temp_data_dir, "crop")
    os.makedirs(stitched_dir, exist_ok=True)
    os.makedirs(crop_dir, exist_ok=True)
    
    # Input file does not exist
    input_file: str = os.path.join(stitched_dir, "test_stitched.tiff")
    output_file: str = os.path.join(crop_dir, "test_crop.tiff")
    
    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": input_file,
        "output_filename": output_file,
        "cropmat": [10, 90, 10, 90]  # Crop values: start_row, end_row, start_col, end_col
    }
    
    # Test
    with pytest.raises(ValueError, match="mask file not found"):
        RP_crop(parameters)


def test_crop_values_exceed_image_size(temp_data_dir: str) -> None:
    """Test that ValueError is raised when crop values exceed image dimensions."""
    # Setup directory structure
    stitched_dir: str = os.path.join(temp_data_dir, "stitched")
    crop_dir: str = os.path.join(temp_data_dir, "crop")
    os.makedirs(stitched_dir, exist_ok=True)
    os.makedirs(crop_dir, exist_ok=True)
    
    # Create test image (100x100)
    input_file: str = os.path.join(stitched_dir, "test_stitched.tiff")
    output_file: str = os.path.join(crop_dir, "test_crop.tiff")
    
    test_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 200
    test: Image.Image = Image.fromarray(test_img)
    test.save(input_file)
    
    # Setup parameters with crop values exceeding image size
    parameters: Dict[str, Any] = {
        "image_filename": input_file,
        "output_filename": output_file,
        "cropmat": [10, 120, 10, 90]  # End row (120) exceeds image height (100)
    }
    
    # Test
    with pytest.raises(ValueError, match="Crop values exceed image size"):
        RP_crop(parameters)


def test_zero_cropmat_uses_full_image(temp_data_dir: str) -> None:
    """Test that when cropmat sums to zero, the entire image is used."""
    # Setup directory structure
    stitched_dir: str = os.path.join(temp_data_dir, "stitched")
    crop_dir: str = os.path.join(temp_data_dir, "crop")
    os.makedirs(stitched_dir, exist_ok=True)
    os.makedirs(crop_dir, exist_ok=True)
    
    # Create test image (100x100)
    input_file: str = os.path.join(stitched_dir, "test_stitched.tiff")
    output_file: str = os.path.join(crop_dir, "test_crop.tiff")
    
    test_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 200
    test: Image.Image = Image.fromarray(test_img)
    test.save(input_file)
    
    # Setup parameters with zero cropmat
    parameters: Dict[str, Any] = {
        "image_filename": input_file,
        "output_filename": output_file,
        "cropmat": [0, 0, 0, 0]  # Zero cropmat should use full image
    }
    
    # Run crop
    RP_crop(parameters)
    
    # Load and check output file
    assert os.path.isfile(output_file), "Output file was not created"
    
    output_img: Image.Image = Image.open(output_file)
    output_array: np.ndarray = np.array(output_img)
    
    # Verify dimensions are the same as input
    assert output_array.shape == (100, 100), "Output dimensions don't match original image"


def test_normal_crop(temp_data_dir: str) -> None:
    """Test that cropping works correctly with valid crop values."""
    # Setup directory structure
    stitched_dir: str = os.path.join(temp_data_dir, "stitched")
    crop_dir: str = os.path.join(temp_data_dir, "crop")
    os.makedirs(stitched_dir, exist_ok=True)
    os.makedirs(crop_dir, exist_ok=True)
    
    # Create test image (100x100) with recognizable pattern
    input_file: str = os.path.join(stitched_dir, "test_stitched.tiff")
    output_file: str = os.path.join(crop_dir, "test_crop.tiff")
    
    # Create a test image with different values in different regions for easy verification
    test_img: np.ndarray = np.zeros((100, 100), dtype=np.uint8)
    test_img[20:80, 20:80] = 100  # Center region = 100
    test_img[40:60, 40:60] = 200  # Inner region = 200
    test: Image.Image = Image.fromarray(test_img)
    test.save(input_file)
    
    # Setup parameters to crop to the center region
    parameters: Dict[str, Any] = {
        "image_filename": input_file,
        "output_filename": output_file,
        "cropmat": [20, 80, 20, 80]  # Crop to center region
    }
    
    # Run crop
    RP_crop(parameters)
    
    # Load and check output file
    assert os.path.isfile(output_file), "Output file was not created"
    
    output_img: Image.Image = Image.open(output_file)
    output_array: np.ndarray = np.array(output_img)
    
    # Verify dimensions
    assert output_array.shape == (60, 60), "Output dimensions incorrect after crop"
    
    # Verify content - center should be 100 and inner region should be 200
    assert np.all(output_array[0:20, 0:20] == 100), "Outer region values incorrect"
    assert np.all(output_array[20:40, 20:40] == 200), "Inner region values incorrect"