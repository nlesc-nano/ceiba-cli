"""Test the manage action."""
from datetime import datetime
from typing import Any, Dict, List

from pytest_mock import MockFixture

from ceibacli.actions import manage_jobs
from ceibacli.input_validation import validate_input

from .utils_test import PATH_TEST


def run_manage_job(mocker: MockFixture, jobs: Dict[str, List[Any]]):
    """Test the job creation"""
    path_input = PATH_TEST / "input_test_manage.yml"
    opts = validate_input(path_input, "manage")

    # Mock the authentication
    mocker.patch("ceibacli.actions.manage.fetch_cookie",
                 return_value="cookie_data")

    # Mock the server call
    mocker.patch("ceibacli.actions.manage.query_server",
                 return_value=jobs)
    # Mock the update call
    mocker.patch("ceibacli.actions.manage.update_job_status",
                 return_value=None)
    manage_jobs(opts)


def test_manage_no_expired_jobs(mocker: MockFixture):
    """Test the job creation"""
    jobs = {'jobs': []}  # type: Dict[str, List[Any]]
    run_manage_job(mocker, jobs)


def test_manage_single_expired_job(mocker: MockFixture):
    """Test that a single expired job."""
    jobs = {'jobs': [{"schedule_time": 100000000}]}  # datetime.datetime(1973, 3, 3, 10, 46, 40,..
    run_manage_job(mocker, jobs)
