import os
import sys
from pathlib import Path
from typing import List, Any, Union

import pytest
from rhizotools.RP_run import RP_run


def test_incorrect_input_analysis_list(temp_data_dir: str) -> None:
    """Test that ValueError is raised when analysis_list contains invalid modules."""
    # Setup
    proj_root: str = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "../"))
    bad_analysis_list: List[str] = ["sitch"]  # Misspelled analysis name
    
    # Test
    with pytest.raises(ValueError):
        RP_run(proj_root, temp_data_dir, bad_analysis_list, 0, 1)


def test_string_analysis_list(temp_data_dir: str) -> None:
    """Test that ValueError is raised when analysis_list is a string instead of a list."""
    # Setup
    proj_root: str = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "../"))
    bad_analysis_list: str = "RP_stitch"  # String instead of list
    
    # Test
    with pytest.raises(ValueError):
        # Type ignore because we're intentionally passing the wrong type for testing
        RP_run(proj_root, temp_data_dir, bad_analysis_list, 0, 1)  # type: ignore


def test_integer_analysis_list(temp_data_dir: str) -> None:
    """Test that ValueError is raised when analysis_list is an integer instead of a list."""
    # Setup
    proj_root: str = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "../"))
    bad_analysis_list: int = 4  # Integer instead of list
    
    # Test
    with pytest.raises(ValueError):
        # Type ignore because we're intentionally passing the wrong type for testing
        RP_run(proj_root, temp_data_dir, bad_analysis_list, 0, 1)  # type: ignore


def test_bad_override(temp_data_dir: str) -> None:
    """Test that ValueError is raised when override is not a valid value."""
    # Setup
    proj_root: str = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "../"))
    analysis_list: List[str] = ["RP_stitch"]
    
    # Test with string override
    with pytest.raises(ValueError):
        # Type ignore because we're intentionally passing the wrong type for testing
        RP_run(proj_root, temp_data_dir, analysis_list, 0, "override")  # type: ignore
    
    # Test with invalid integer
    with pytest.raises(ValueError):
        RP_run(proj_root, temp_data_dir, analysis_list, 0, 4)