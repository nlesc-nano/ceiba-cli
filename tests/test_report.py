""""Test the report functionality."""


from pytest_mock import MockFixture, mocker

from moka.actions import report_properties
from moka.input_validation import validate_input

from .utils_test import PATH_TEST


def test_report(mocker: MockFixture):
    """Test the functionality to report the data to the server."""
    path_input = PATH_TEST / "input_test_report.yml"
    opts = validate_input(path_input, "report")

    # Mock the server call
    mocker.patch("moka.actions.report.query_server", return_value=None)

    report_properties(opts)
