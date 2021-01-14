"""Module to the client actions."""

from pytest_mock import MockFixture

from ceibacli.actions import add_jobs
from ceibacli.input_validation import validate_input

from .utils_test import PATH_TEST, read_mocked_reply


def test_add_jobs(mocker: MockFixture):
    """Test the job creation"""
    path_input = PATH_TEST / "input_test_add.yml"
    opts = validate_input(path_input, "add")

    # Mock the authentication
    mocker.patch("ceibacli.actions.add.fetch_cookie",
                 return_value="cookie_data")

    # Mock the server call
    mocker.patch("ceibacli.actions.add.query_server",
                 return_value=read_mocked_reply("add_jobs_mocked.json"))

    add_jobs(opts)
