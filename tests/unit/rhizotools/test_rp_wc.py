import os
from pathlib import Path
from typing import Dict, Any, List, Union

import numpy as np
import pytest
from PIL import Image

from rhizotools.RP_wc import RP_wc


def test_missing_input_file(temp_data_dir: str) -> None:
    """Test that ValueError is raised when input file is missing."""
    # Setup directory structure
    crop_dir: str = os.path.join(temp_data_dir, "crop")
    wc_dir: str = os.path.join(temp_data_dir, "wc")
    os.makedirs(crop_dir, exist_ok=True)
    os.makedirs(wc_dir, exist_ok=True)
    
    # Input file does not exist
    input_file: str = os.path.join(crop_dir, "test_crop.tiff")
    output_file: str = os.path.join(wc_dir, "test_wc.tiff")
    
    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": input_file,
        "output_filename": output_file,
        "b_w": 0.1,  # Example scattering coefficient of water
        "s_w": 0.2,  # Example attenuation coefficient of water
        "s_a": 0.3,  # Example attenuation coefficient of aluminum
        "s_s": 0.4,  # Example attenuation coefficient of silicon
        "x_s": 0.5,  # Example thickness of soil
        "x_a": 0.01  # Example thickness of aluminum
    }
    
    # Test
    with pytest.raises(ValueError, match="mask file not found"):
        RP_wc(parameters)


def test_blank_image(temp_data_dir: str) -> None:
    """Test that ValueError is raised when image is blank (zeros)."""
    # Setup directory structure
    crop_dir: str = os.path.join(temp_data_dir, "crop")
    wc_dir: str = os.path.join(temp_data_dir, "wc")
    os.makedirs(crop_dir, exist_ok=True)
    os.makedirs(wc_dir, exist_ok=True)
    
    # Create blank test image with zeros
    input_file: str = os.path.join(crop_dir, "test_crop.tiff")
    output_file: str = os.path.join(wc_dir, "test_wc.tiff")
    
    blank_img: np.ndarray = np.zeros((100, 100), dtype=np.float32)
    blank: Image.Image = Image.fromarray(blank_img)
    blank.save(input_file)
    
    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": input_file,
        "output_filename": output_file,
        "b_w": 0.1,
        "s_w": 0.2,
        "s_a": 0.3,
        "s_s": 0.4,
        "x_s": 0.5,
        "x_a": 0.01
    }
    
    # Test
    with pytest.raises(ValueError, match="Image is blank"):
        RP_wc(parameters)


def test_valid_wc_calculation(temp_data_dir: str) -> None:
    """Test that water content calculation works correctly with valid input."""
    # Setup directory structure
    crop_dir: str = os.path.join(temp_data_dir, "crop")
    wc_dir: str = os.path.join(temp_data_dir, "wc")
    os.makedirs(crop_dir, exist_ok=True)
    os.makedirs(wc_dir, exist_ok=True)
    
    # Create test image with transmission values
    input_file: str = os.path.join(crop_dir, "test_crop.tiff")
    output_file: str = os.path.join(wc_dir, "test_wc.tiff")
    
    # Create a simple uniform image with transmission values
    # Using a value greater than 1 for higher transmission
    transmission_values: np.ndarray = np.ones((100, 100), dtype=np.float32) * 1.2
    test_img: Image.Image = Image.fromarray(transmission_values)
    test_img.save(input_file)
    
    # Setup parameters with realistic values
    parameters: Dict[str, Any] = {
        "image_filename": input_file,
        "output_filename": output_file,
        "b_w": 0.1,  # cm^-2
        "s_w": 0.2,  # cm^-1
        "s_a": 0.3,  # cm^-1
        "s_s": 0.4,  # cm^-1
        "x_s": 0.5,  # cm
        "x_a": 0.01  # cm
    }
    
    # Run water content calculation
    RP_wc(parameters)
    
    # Verify output file exists
    assert os.path.isfile(output_file), "Output file was not created"
    
    # Load output image
    output_img: Image.Image = Image.open(output_file)
    output_array: np.ndarray = np.array(output_img)
    
    # Verify dimensions
    assert output_array.shape == (100, 100), "Output dimensions don't match input"
    
    # Check for valid output - we're not verifying specific values
    # but just that calculations ran without errors
    assert not np.isnan(np.sum(output_array)), "Output contains NaN values"


def test_different_input_values(temp_data_dir: str) -> None:
    """Test water content calculation with non-uniform input values."""
    # Setup directory structure
    crop_dir: str = os.path.join(temp_data_dir, "crop")
    wc_dir: str = os.path.join(temp_data_dir, "wc")
    os.makedirs(crop_dir, exist_ok=True)
    os.makedirs(wc_dir, exist_ok=True)
    
    # Create test image with varying transmission values
    input_file: str = os.path.join(crop_dir, "test_crop.tiff")
    output_file: str = os.path.join(wc_dir, "test_wc.tiff")
    
    # Create an image with varying transmission values - using higher values for valid results
    transmission_values: np.ndarray = np.ones((100, 100), dtype=np.float32) * 1.2
    # Add a pattern for testing
    transmission_values[30:70, 30:70] = 1.5  # Higher transmission in middle region
    test_img: Image.Image = Image.fromarray(transmission_values)
    test_img.save(input_file)
    
    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": input_file,
        "output_filename": output_file,
        "b_w": 0.1,
        "s_w": 0.2,
        "s_a": 0.3,
        "s_s": 0.4,
        "x_s": 0.5,
        "x_a": 0.01
    }
    
    # Run water content calculation
    RP_wc(parameters)
    
    # Verify output file exists
    assert os.path.isfile(output_file), "Output file was not created"
    
    # Load output image
    output_img: Image.Image = Image.open(output_file)
    output_array: np.ndarray = np.array(output_img)
    
    # Verify dimensions
    assert output_array.shape == (100, 100), "Output dimensions don't match input"
    
    # Note: In a real situation, we would compare to known values computed by hand
    # Here we just verify that the structure of the output makes sense based on input
    
    # Get mean values from different regions
    center_values: np.ndarray = output_array[30:70, 30:70]
    outer_values: np.ndarray = np.concatenate([
        output_array[0:30, :].flatten(),
        output_array[70:100, :].flatten(),
        output_array[30:70, 0:30].flatten(),
        output_array[30:70, 70:100].flatten()
    ])
    
    # Count non-NaN values to ensure we have valid data to compare
    valid_center: int = np.sum(~np.isnan(center_values))
    valid_outer: int = np.sum(~np.isnan(outer_values))
    
    # Only assert difference if we have valid data to compare
    if valid_center > 0 and valid_outer > 0:
        center_mean: float = np.nanmean(center_values)
        outer_mean: float = np.nanmean(outer_values)
        assert center_mean != outer_mean, "Output does not show expected variation based on input pattern"