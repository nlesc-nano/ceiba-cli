""""Test the report functionality."""


from pytest_mock import MockFixture

from moka.actions import report_properties
from moka.input_validation import validate_input

from .utils_test import PATH_TEST


def run_report(mocker: MockFixture, file_name: str):
    """Test the functionality to report the data to the server."""
    path_input = PATH_TEST / file_name
    opts = validate_input(path_input, "report")

    # Mock the server call
    mocker.patch("moka.actions.report.query_server", return_value={
        "updateJob": {"text": "job has been updated"}})

    report_properties(opts)


def test_report(mocker: MockFixture):
    """Test the functionality to report the data to the server."""
    run_report(mocker, "input_test_report.yml")


def test_report_standalone(mocker: MockFixture):
    """Check that the standalone data is properly report."""
    run_report(mocker, "input_test_standalone_report.yml")
