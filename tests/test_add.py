"""Module to the client actions."""

import json
from pathlib import Path

import pytest
import yaml
from pytest_mock import MockFixture

from ceibacli.actions import add_jobs
from ceibacli.input_validation import validate_input

from .utils_test import PATH_TEST, read_mocked_reply


def test_add_jobs(mocker: MockFixture):
    """Test the job creation."""
    path_input = PATH_TEST / "input_test_add.yml"
    opts = validate_input(path_input, "add")

    # Mock the authentication
    mocker.patch("ceibacli.actions.add.fetch_cookie",
                 return_value="cookie_data")

    # Mock the server call
    mocker.patch("ceibacli.actions.add.query_server",
                 return_value=read_mocked_reply("add_jobs_mocked.json"))

    add_jobs(opts)


def test_wrong_jobs_argument(mocker: MockFixture, tmp_path: Path):
    """Check that an exception is raised if the wrong job arguments is passed."""
    path_jobs = tmp_path / "jobs.json"
    with open(path_jobs, 'w') as handler:
        json.dump({"parameter": 42}, handler)

    arguments = {
        "web": "http://localhost:8080/graphql", "collection_name": "some/collection",
        "jobs": path_jobs.absolute().as_posix(),
    }
    path_input = tmp_path / "wrong_jobs.yml"

    with open(path_input, 'w') as handler:
        yaml.dump(arguments, handler)

    opts = validate_input(path_input, "add")
    # Mock the authentication
    mocker.patch("ceibacli.actions.add.fetch_cookie",
                 return_value="cookie_data")

    with pytest.raises(RuntimeError) as excinfo:
        add_jobs(opts)

    assert "Jobs must be a list of JSON objects" in str(excinfo.value)
