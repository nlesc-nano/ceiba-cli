"""Module to the client actions."""

import json

from pathlib import Path
from pytest_mock import MockFixture, mocker

from moka.actions import query_properties, report_properties
from moka.input_validation import validate_input

from .utils_test import PATH_TEST


def test_add_jobs():
    """Test the job creation"""
    pass


def test_compute(mocker: MockFixture):
    """Test the functionality to compute jobs."""
    pass


def test_report(mocker: MockFixture):
    """Test the functionality to report the data to the server."""
    path_input = PATH_TEST / "input_test_report.yml"
    opts = validate_input(path_input, "report")

    # Mock the server call
    mocker.patch("moka.actions.report.query_server", return_value=None)

    report_properties(opts)


def test_query(mocker: MockFixture, tmp_path: Path):
    """Test the functionality to update jobs."""
    # Read and Validate user input
    path_input = PATH_TEST / "input_test_query.yml"
    opts = validate_input(path_input, "query")
    opts.output_file = (tmp_path / "output.csv").absolute().as_posix()

    # Read mock reply
    path_reply = PATH_TEST / "reply_mock.json"
    with open(path_reply, 'r') as handler:
        reply = json.load(handler)

    # Mock the server interface
    mocker.patch("moka.actions.query.query_server", return_value=reply)

    df = query_properties(opts)
    assert len(df) == 10
