#!/usr/bin/env python
"""Fixtures for the test suite."""

import os
import shutil
from typing import Generator

import pytest
from rhizotools.sampledata import sampledata


@pytest.fixture(scope="function")
def temp_data_dir(request: pytest.FixtureRequest) -> Generator[str, None, None]:
    """Creates a temporary directory for test data and cleans it up after the test."""
    # Current file path to get to project root
    file_path: str = os.path.dirname(__file__)
    proj_root: str = os.path.abspath(os.path.join(file_path, "../"))

    # Create a unique temp directory for each test
    test_dir: str = os.path.join(proj_root, "test_data_temp")

    # Clean up any existing test data directory
    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)

    # Create the test directory
    os.makedirs(test_dir)

    # Return path to the test directory
    yield test_dir

    # Clean up after test
    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)


@pytest.fixture(scope="function")
def sample_data(temp_data_dir: str) -> Generator[str, None, None]:
    """Creates sample data in the temporary directory."""
    # Get absolute path to the project root
    file_path: str = os.path.dirname(__file__)
    proj_root: str = os.path.abspath(os.path.join(file_path, "../"))

    # Generate sample data using the package's sampledata function
    sampledata(proj_root, 1)

    # Yield the path to the sample data directory
    yield os.path.join(proj_root, "Sample_Data_unittest")


@pytest.fixture(scope="session")
def reference_data_dir() -> str:
    """Returns the path to the reference data directory with ideal outputs."""
    file_path: str = os.path.dirname(__file__)
    ref_data_path: str = os.path.abspath(os.path.join(file_path, "../test/Sample_Data_ideal"))

    if not os.path.isdir(ref_data_path):
        pytest.skip(f"Reference data directory not found: {ref_data_path}")

    return ref_data_path
