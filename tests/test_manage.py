"""Test the manage action."""
from pytest_mock import MockFixture

from moka.actions import manage_jobs
from moka.input_validation import validate_input

from .utils_test import PATH_TEST


def test_manage_jobs(mocker: MockFixture):
    """Test the job creation"""
    path_input = PATH_TEST / "input_test_manage.yml"
    opts = validate_input(path_input, "manage")

    # Mock the server call
    mocker.patch("moka.actions.manage.query_server",
                 return_value={'jobs': []})

    manage_jobs(opts)