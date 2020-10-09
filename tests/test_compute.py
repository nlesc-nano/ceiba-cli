"""Test the compute method."""

import pytest
from pytest_mock import MockFixture, mocker

from moka.actions.compute import compute_jobs, update_job_status
from moka.input_validation import validate_input
from moka.utils import Options

from .utils_test import PATH_TEST, read_mocked_reply


def test_compute(mocker: MockFixture):
    """Test the functionality to compute jobs."""
    path_input = PATH_TEST / "input_test_compute.yml"
    opts = validate_input(path_input, "compute")

    # Mock the server call
    mocker.patch("moka.actions.compute.query_server",
                 return_value=read_mocked_reply("compute_jobs_mocked.json"))

    mocker.patch("moka.actions.compute.update_job_status",
                 return_value=None)

    compute_jobs(opts)


def test_no_jobs_to_compute(mocker: MockFixture):
    """Test that the application exits without error if there are no jobs."""
    path_input = PATH_TEST / "input_test_compute.yml"
    opts = validate_input(path_input, "compute")

    # Mock the server call
    mocker.patch("moka.actions.compute.query_server",
                 return_value={"jobs": []})

    with pytest.raises(SystemExit):
        compute_jobs(opts)


def test_update_status(mocker: MockFixture):
    """Test the update update_job_status function."""
    mocker.patch("moka.actions.compute.query_server",
                 return_value=None)

    opts = Options({"collection_name": "something"})
    job = {"_id": 314159265}

    update_job_status(opts, job, 'FAILED')