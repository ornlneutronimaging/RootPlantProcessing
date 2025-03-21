import os
from typing import Any, Dict

import numpy as np
import pytest
from PIL import Image

from rhizotools.RP_stitch import RP_stitch


def test_missing_dark_field(temp_data_dir: str) -> None:
    """Test that ValueError is raised when dark field image is missing."""
    # Setup directory structure
    raw_dir: str = os.path.join(temp_data_dir, "raw")
    output_dir: str = os.path.join(temp_data_dir, "stitched")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Create OB image only (no DF)
    ob_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 255
    ob: Image.Image = Image.fromarray(ob_img)
    ob.save(os.path.join(raw_dir, "OB.tiff"))

    # Create test image
    test_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 200
    test: Image.Image = Image.fromarray(test_img)
    test.save(os.path.join(raw_dir, "test_0001.tiff"))

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": raw_dir,
        "output_filename": output_dir,
        "stitch_order": [1, 1, 1],  # 1x1 grid with image index 1
        "fileformat": "test",
        "dimh_horzoffset": 0,
        "dimh_vertoffset": 0,
        "dimv_horzoffset": 0,
        "dimv_vertoffset": 0,
        "output_fileformat": 0,
    }

    # Test
    with pytest.raises(ValueError, match="Dark field image not present in file"):
        RP_stitch(parameters)


def test_missing_open_beam(temp_data_dir: str) -> None:
    """Test that ValueError is raised when open beam image is missing."""
    # Setup directory structure
    raw_dir: str = os.path.join(temp_data_dir, "raw")
    output_dir: str = os.path.join(temp_data_dir, "stitched")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Create DF image only (no OB)
    df_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 50
    df: Image.Image = Image.fromarray(df_img)
    df.save(os.path.join(raw_dir, "DF.tiff"))

    # Create test image
    test_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 200
    test: Image.Image = Image.fromarray(test_img)
    test.save(os.path.join(raw_dir, "test_0001.tiff"))

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": raw_dir,
        "output_filename": output_dir,
        "stitch_order": [1, 1, 1],  # 1x1 grid with image index 1
        "fileformat": "test",
        "dimh_horzoffset": 0,
        "dimh_vertoffset": 0,
        "dimv_horzoffset": 0,
        "dimv_vertoffset": 0,
        "output_fileformat": 0,
    }

    # Test
    with pytest.raises(ValueError, match="Open beam image not present in file"):
        RP_stitch(parameters)


def test_size_mismatch_ob_df(temp_data_dir: str) -> None:
    """Test that ValueError is raised when OB and DF images have different sizes."""
    # Setup directory structure
    raw_dir: str = os.path.join(temp_data_dir, "raw")
    output_dir: str = os.path.join(temp_data_dir, "stitched")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Create OB and DF images with different sizes
    ob_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 255
    ob: Image.Image = Image.fromarray(ob_img)
    ob.save(os.path.join(raw_dir, "OB.tiff"))

    df_img: np.ndarray = np.ones((90, 90), dtype=np.uint8) * 50  # Different size
    df: Image.Image = Image.fromarray(df_img)
    df.save(os.path.join(raw_dir, "DF.tiff"))

    # Create test image
    test_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 200
    test: Image.Image = Image.fromarray(test_img)
    test.save(os.path.join(raw_dir, "test_0001.tiff"))

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": raw_dir,
        "output_filename": output_dir,
        "stitch_order": [1, 1, 1],  # 1x1 grid with image index 1
        "fileformat": "test",
        "dimh_horzoffset": 0,
        "dimh_vertoffset": 0,
        "dimv_horzoffset": 0,
        "dimv_vertoffset": 0,
        "output_fileformat": 0,
    }

    # Test
    with pytest.raises(ValueError, match="Open beam and dark field images are not the same size"):
        RP_stitch(parameters)


def test_missing_input_image(temp_data_dir: str) -> None:
    """Test that ValueError is raised when a referenced input image is missing."""
    # Setup directory structure
    raw_dir: str = os.path.join(temp_data_dir, "raw")
    output_dir: str = os.path.join(temp_data_dir, "stitched")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Create OB and DF images
    ob_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 255
    ob: Image.Image = Image.fromarray(ob_img)
    ob.save(os.path.join(raw_dir, "OB.tiff"))

    df_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 50
    df: Image.Image = Image.fromarray(df_img)
    df.save(os.path.join(raw_dir, "DF.tiff"))

    # Don't create the referenced test image

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": raw_dir,
        "output_filename": output_dir,
        "stitch_order": [1, 1, 1],  # 1x1 grid with image index 1
        "fileformat": "test",
        "dimh_horzoffset": 0,
        "dimh_vertoffset": 0,
        "dimv_horzoffset": 0,
        "dimv_vertoffset": 0,
        "output_fileformat": 0,
    }

    # Test
    with pytest.raises(ValueError, match="One or more of the raw images specified in 'stitch_order' is not present"):
        RP_stitch(parameters)


def test_inconsistent_image_size(temp_data_dir: str) -> None:
    """Test that ValueError is raised when input images have inconsistent sizes."""
    # Setup directory structure
    raw_dir: str = os.path.join(temp_data_dir, "raw")
    output_dir: str = os.path.join(temp_data_dir, "stitched")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Create OB and DF images
    ob_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 255
    ob: Image.Image = Image.fromarray(ob_img)
    ob.save(os.path.join(raw_dir, "OB.tiff"))

    df_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 50
    df: Image.Image = Image.fromarray(df_img)
    df.save(os.path.join(raw_dir, "DF.tiff"))

    # Create test image with different size
    test_img: np.ndarray = np.ones((90, 90), dtype=np.uint8) * 200  # Different size
    test: Image.Image = Image.fromarray(test_img)
    test.save(os.path.join(raw_dir, "test_0001.tiff"))

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": raw_dir,
        "output_filename": output_dir,
        "stitch_order": [1, 1, 1],  # 1x1 grid with image index 1
        "fileformat": "test",
        "dimh_horzoffset": 0,
        "dimh_vertoffset": 0,
        "dimv_horzoffset": 0,
        "dimv_vertoffset": 0,
        "output_fileformat": 0,
    }

    # Test
    with pytest.raises(ValueError, match="Raw image size is inconsistent"):
        RP_stitch(parameters)


# Add a positive test case to verify successful stitching
def test_successful_stitching(temp_data_dir: str) -> None:
    """Test that stitching works correctly for a simple 1x1 grid."""
    # Setup directory structure
    raw_dir: str = os.path.join(temp_data_dir, "raw")
    output_dir: str = os.path.join(temp_data_dir, "stitched")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Create OB and DF images
    ob_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 255
    ob: Image.Image = Image.fromarray(ob_img)
    ob.save(os.path.join(raw_dir, "OB.tiff"))

    df_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 50
    df: Image.Image = Image.fromarray(df_img)
    df.save(os.path.join(raw_dir, "DF.tiff"))

    # Create test image
    test_img: np.ndarray = np.ones((100, 100), dtype=np.uint8) * 200
    test: Image.Image = Image.fromarray(test_img)
    test.save(os.path.join(raw_dir, "test_0001.tiff"))

    # Setup parameters
    parameters: Dict[str, Any] = {
        "image_filename": raw_dir,
        "output_filename": output_dir,
        "stitch_order": [1, 1, 1],  # 1x1 grid with image index 1
        "fileformat": "test",
        "dimh_horzoffset": 0,
        "dimh_vertoffset": 0,
        "dimv_horzoffset": 0,
        "dimv_vertoffset": 0,
        "output_fileformat": 0,
    }

    # Run stitching
    RP_stitch(parameters)

    # Verify output file exists
    output_file: str = os.path.join(output_dir, "test_stitched.tiff")
    assert os.path.isfile(output_file), "Output file was not created"

    # Could also verify image content if needed
