"""Module to the client actions."""

from pathlib import Path

from pytest_mock import MockFixture, mocker

from moka.actions import add_jobs, query_properties
from moka.input_validation import validate_input

from .utils_test import PATH_TEST, read_mocked_reply


def test_add_jobs(mocker: MockFixture):
    """Test the job creation"""
    path_input = PATH_TEST / "input_test_add.yml"
    opts = validate_input(path_input, "add")

    # Mock the server call
    mocker.patch("moka.actions.add.query_server",
                 return_value=read_mocked_reply("add_jobs_mocked.json"))

    add_jobs(opts)
