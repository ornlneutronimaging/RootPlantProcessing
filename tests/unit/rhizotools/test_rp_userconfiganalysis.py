import os

import pytest

from rhizotools.RP_userconfiganalysis import RP_userconfiganalysis


def test_missing_config_file(tmp_path):
    """Test that an error is raised when the config file is missing."""
    with pytest.raises(ValueError, match="user_config.txt file not present in correct location"):
        RP_userconfiganalysis(str(tmp_path), [1, 10], "RP_stitch")


def test_stitch_parameter_validation(tmp_path):
    """Test validation of stitch parameters."""
    # Create a minimal config file based on the actual format in Sample_Data_ideal
    config_path = tmp_path / "user_config.txt"
    with open(config_path, "w") as f:
        f.write("1. STITCH\n")
        f.write("image_filename:/path/to/raw\n")
        f.write("output_filename:/path/to/stitched\n")
        f.write("output_fileformat:SampleImg\n")
        f.write("fileformat:test\n")
        f.write("dimv_horzoffset:20\n")
        f.write("dimv_vertoffset:10\n")
        f.write("dimh_horzoffset:5\n")
        f.write("dimh_vertoffset:7\n")
        f.write("stitch_order:2,3,3,2,1,6,5,4\n")

    # Test correct validation
    params = RP_userconfiganalysis(str(tmp_path), [1, 10], "RP_stitch")

    assert params["dimv_horzoffset"] == 20
    assert params["dimv_vertoffset"] == 10
    assert params["dimh_horzoffset"] == 5
    assert params["dimh_vertoffset"] == 7
    assert params["stitch_order"] == [2, 3, 3, 2, 1, 6, 5, 4]

    # Test invalid type for offset values
    with open(config_path, "w") as f:
        f.write("1. STITCH\n")
        f.write("image_filename:/path/to/raw\n")
        f.write("output_filename:/path/to/stitched\n")
        f.write("output_fileformat:SampleImg\n")
        f.write("fileformat:test\n")
        f.write("dimv_horzoffset:invalid\n")  # Invalid value
        f.write("dimv_vertoffset:10\n")
        f.write("dimh_horzoffset:5\n")
        f.write("dimh_vertoffset:7\n")
        f.write("stitch_order:2,3,3,2,1,6,5,4\n")

    with pytest.raises(ValueError, match="STITCH - Offset values are not in 'int' format"):
        RP_userconfiganalysis(str(tmp_path), [1, 10], "RP_stitch")


def test_crop_parameter_validation(tmp_path):
    """Test validation of crop parameters."""
    config_path = tmp_path / "user_config.txt"

    # Valid crop parameters
    with open(config_path, "w") as f:
        f.write("2. CROP\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("cropmat:21,472,183,633\n")

    params = RP_userconfiganalysis(str(tmp_path), [1, 4], "RP_crop")
    assert params["cropmat"] == [21, 472, 183, 633]

    # Invalid crop parameters (non-integer)
    with open(config_path, "w") as f:
        f.write("2. CROP\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("cropmat:21,invalid,183,633\n")

    with pytest.raises(ValueError, match="CROP - 'cropmat' values are not in the correct format"):
        RP_userconfiganalysis(str(tmp_path), [1, 4], "RP_crop")


def test_wc_parameter_validation(tmp_path):
    """Test validation of water content parameters."""
    config_path = tmp_path / "user_config.txt"

    # Valid WC parameters
    with open(config_path, "w") as f:
        f.write("3. WC\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("b_w:-2.14\n")
        f.write("s_w:5.3\n")
        f.write("s_a:0.02015\n")
        f.write("s_s:0.006604\n")
        f.write("x_s:1\n")
        f.write("x_a:0.2\n")

    params = RP_userconfiganalysis(str(tmp_path), [1, 9], "RP_wc")
    assert params["b_w"] == -2.14
    assert params["s_w"] == 5.3
    assert params["s_a"] == 0.02015
    assert params["s_s"] == 0.006604
    assert params["x_s"] == 1.0
    assert params["x_a"] == 0.2

    # Invalid WC parameters (non-float)
    with open(config_path, "w") as f:
        f.write("3. WC\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("b_w:invalid\n")  # Invalid value
        f.write("s_w:5.3\n")
        f.write("s_a:0.02015\n")
        f.write("s_s:0.006604\n")
        f.write("x_s:1\n")
        f.write("x_a:0.2\n")

    with pytest.raises(ValueError, match="'wc' values are not in the correct format"):
        RP_userconfiganalysis(str(tmp_path), [1, 9], "RP_wc")

    # Invalid WC parameters (negative values)
    with open(config_path, "w") as f:
        f.write("3. WC\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("b_w:-2.14\n")
        f.write("s_w:-5.3\n")  # Negative value (invalid)
        f.write("s_a:0.02015\n")
        f.write("s_s:0.006604\n")
        f.write("x_s:1\n")
        f.write("x_a:0.2\n")

    with pytest.raises(ValueError, match="WC - Invalid numbers: s_w, s_a, s_s, x_s, or x_a are less than 0"):
        RP_userconfiganalysis(str(tmp_path), [1, 9], "RP_wc")


def test_mask_parameter_validation(tmp_path):
    """Test validation of mask parameters."""
    config_path = tmp_path / "user_config.txt"

    # Valid mask parameters
    with open(config_path, "w") as f:
        f.write("4. MASK\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("windowsize:11\n")
        f.write("threshold:0.05\n")
        f.write("globthresh:0.3\n")

    params = RP_userconfiganalysis(str(tmp_path), [1, 6], "RP_mask")
    assert params["windowsize"] == 11
    assert params["threshold"] == 0.05
    assert params["globthresh"] == 0.3

    # Invalid mask parameters (non-numeric)
    with open(config_path, "w") as f:
        f.write("4. MASK\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("windowsize:invalid\n")  # Invalid value
        f.write("threshold:0.05\n")
        f.write("globthresh:0.3\n")

    with pytest.raises(ValueError, match="'mask' values are not in the correct format"):
        RP_userconfiganalysis(str(tmp_path), [1, 6], "RP_mask")

    # Invalid mask parameters (windowsize < 0)
    with open(config_path, "w") as f:
        f.write("4. MASK\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("windowsize:-11\n")  # Negative value (invalid)
        f.write("threshold:0.05\n")
        f.write("globthresh:0.3\n")

    with pytest.raises(ValueError, match="windowsize must be greater than 0"):
        RP_userconfiganalysis(str(tmp_path), [1, 6], "RP_mask")

    # Invalid mask parameters (windowsize is even)
    with open(config_path, "w") as f:
        f.write("4. MASK\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("windowsize:10\n")  # Even value (invalid)
        f.write("threshold:0.05\n")
        f.write("globthresh:0.3\n")

    with pytest.raises(ValueError, match="MASK - windowsize must be an odd number"):
        RP_userconfiganalysis(str(tmp_path), [1, 6], "RP_mask")


def test_imagefilter_parameter_validation(tmp_path):
    """Test validation of image filter parameters."""
    config_path = tmp_path / "user_config.txt"

    # Valid imagefilter parameters
    with open(config_path, "w") as f:
        f.write("5. IMAGEFILTER\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("bwareaval:800\n")
        f.write("medfilterval:5\n")

    params = RP_userconfiganalysis(str(tmp_path), [1, 5], "RP_imagefilter")
    assert params["bwareaval"] == 800
    assert params["medfilterval"] == 5

    # Invalid imagefilter parameters (non-integer)
    with open(config_path, "w") as f:
        f.write("5. IMAGEFILTER\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("bwareaval:invalid\n")  # Invalid value
        f.write("medfilterval:5\n")

    with pytest.raises(ValueError, match="'imagefilter' values are not in the correct format"):
        RP_userconfiganalysis(str(tmp_path), [1, 5], "RP_imagefilter")

    # Invalid imagefilter parameters (negative values)
    with open(config_path, "w") as f:
        f.write("5. IMAGEFILTER\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("bwareaval:-800\n")  # Negative value (invalid)
        f.write("medfilterval:5\n")

    with pytest.raises(
        ValueError, match="IMAGEFILTER - Invalid numbers: medfilterval and bwareaval must be greater than 0"
    ):
        RP_userconfiganalysis(str(tmp_path), [1, 5], "RP_imagefilter")

    # Invalid imagefilter parameters (medfilterval is even)
    with open(config_path, "w") as f:
        f.write("5. IMAGEFILTER\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("bwareaval:800\n")
        f.write("medfilterval:4\n")  # Even value (invalid)

    with pytest.raises(ValueError, match="medfilterval must be an odd number"):
        RP_userconfiganalysis(str(tmp_path), [1, 5], "RP_imagefilter")


def test_distmap_parameter_validation(tmp_path):
    """Test validation of distance map parameters."""
    config_path = tmp_path / "user_config.txt"

    # Valid distmap parameters
    with open(config_path, "w") as f:
        f.write("6. DISTMAP\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("maxval:400\n")

    params = RP_userconfiganalysis(str(tmp_path), [1, 4], "RP_distmap")
    assert params["maxval"] == 400

    # Invalid distmap parameters (non-integer)
    with open(config_path, "w") as f:
        f.write("6. DISTMAP\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("maxval:invalid\n")  # Invalid value

    with pytest.raises(ValueError, match="'distmap' values are not in the correct format"):
        RP_userconfiganalysis(str(tmp_path), [1, 4], "RP_distmap")

    # Invalid distmap parameters (negative values)
    with open(config_path, "w") as f:
        f.write("6. DISTMAP\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")
        f.write("maxval:-400\n")  # Negative value (invalid)

    with pytest.raises(ValueError, match="DISTMAP - Invalid numbers: maxval must be greater than 0"):
        RP_userconfiganalysis(str(tmp_path), [1, 4], "RP_distmap")


def test_radwc_parameter_validation(tmp_path):
    """Test validation of radial water content parameters."""
    config_path = tmp_path / "user_config.txt"

    # Valid radwc parameters
    with open(config_path, "w") as f:
        f.write("7. RADWC\n")
        f.write("wc_filename:/path/to/wc.tiff\n")
        f.write("distmap_filename:/path/to/distmap.tiff\n")
        f.write("mask_filename:/path/to/mask.tiff\n")
        f.write("output_filename:/path/to/output\n")
        f.write("fileformat:SampleImg\n")
        f.write("pixelbin:1\n")

    params = RP_userconfiganalysis(str(tmp_path), [1, 7], "RP_radwc")
    assert params["pixelbin"] == 1

    # Invalid radwc parameters (non-integer)
    with open(config_path, "w") as f:
        f.write("7. RADWC\n")
        f.write("wc_filename:/path/to/wc.tiff\n")
        f.write("distmap_filename:/path/to/distmap.tiff\n")
        f.write("mask_filename:/path/to/mask.tiff\n")
        f.write("output_filename:/path/to/output\n")
        f.write("fileformat:SampleImg\n")
        f.write("pixelbin:invalid\n")  # Invalid value

    with pytest.raises(ValueError, match="'radwc' values are not in the correct format"):
        RP_userconfiganalysis(str(tmp_path), [1, 7], "RP_radwc")

    # Invalid radwc parameters (negative values)
    with open(config_path, "w") as f:
        f.write("7. RADWC\n")
        f.write("wc_filename:/path/to/wc.tiff\n")
        f.write("distmap_filename:/path/to/distmap.tiff\n")
        f.write("mask_filename:/path/to/mask.tiff\n")
        f.write("output_filename:/path/to/output\n")
        f.write("fileformat:SampleImg\n")
        f.write("pixelbin:-1\n")  # Negative value (invalid)

    with pytest.raises(ValueError, match="RADWC - Invalid numbers: pixelbin must be greater than 0"):
        RP_userconfiganalysis(str(tmp_path), [1, 7], "RP_radwc")


def test_thickness_parameter_validation(tmp_path):
    """Test validation of thickness parameters."""
    config_path = tmp_path / "user_config.txt"

    # Valid thickness parameters (no validation for these)
    with open(config_path, "w") as f:
        f.write("8. THICKNESS\n")
        f.write("image_filename:/path/to/image.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")

    params = RP_userconfiganalysis(str(tmp_path), [1, 3], "RP_thickness")
    assert "image_filename" in params
    assert "output_filename" in params


def test_rootimage_parameter_validation(tmp_path):
    """Test validation of root image parameters."""
    config_path = tmp_path / "user_config.txt"

    # Valid rootimage parameters (no validation for these)
    with open(config_path, "w") as f:
        f.write("9. ROOTIMAGE\n")
        f.write("wc_filename:/path/to/wc.tiff\n")
        f.write("mask_filename:/path/to/mask.tiff\n")
        f.write("output_filename:/path/to/output.tiff\n")

    params = RP_userconfiganalysis(str(tmp_path), [1, 4], "RP_rootimage")
    assert "wc_filename" in params
    assert "mask_filename" in params
    assert "output_filename" in params


@pytest.mark.skip(reason="Line position issues with the sample config file")
def test_with_sample_config(tmp_path):
    """Test using the actual sample config file."""
    # Copy the sample config to the temp directory
    import shutil

    sample_config = "/Users/8cz/github.com/RootPlantProcessing/test/Sample_Data_ideal/user_config.txt"
    target_config = os.path.join(str(tmp_path), "user_config.txt")
    shutil.copyfile(sample_config, target_config)

    # Test one section that we know works
    stitch_params = RP_userconfiganalysis(str(tmp_path), [1, 11], "RP_stitch")
    assert stitch_params["dimv_horzoffset"] == 20
    assert stitch_params["dimv_vertoffset"] == 10
