""""Test the report functionality."""

from pathlib import Path

from pytest_mock import MockFixture

from moka.actions import report_properties
from moka.input_validation import validate_input
from moka.swift_interface import SwiftAction

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
    run_report(mocker, "input_test_report_standalone.yml")


def test_report_large_objects(mocker: MockFixture):
    """Checkt that a file is saved on the large objects storage."""
    run_report(mocker, "input_test_report_large_objects.yml")

    # Check that the large object is in the storage
    container = "awesome_collection"
    swift = SwiftAction("https://awesome_scientific_storage.pi")
    reply = next(swift.list_container(container))
    listing = reply["listing"][0]
    # Extract the file name
    name = listing["name"]
    assert Path(name).name == "data.npy"

    # Remove the data from the storage
    swift.delete(container, objects=[name])
    # Check that there are no objects in the container
    data = list(swift.list_container(container))
    assert not data
