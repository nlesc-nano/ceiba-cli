"""Test the compute method."""


from pytest_mock import MockFixture, mocker

from moka.actions import compute_jobs
from moka.input_validation import validate_input

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
