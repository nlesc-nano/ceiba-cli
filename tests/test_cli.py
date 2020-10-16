"""Test the command line interface."""

import argparse
from pathlib import Path

import pytest
import schema
from pytest_mock import MockFixture

from moka.cli import main

from .utils_test import PATH_TEST


def run_workflow_mock(mocker: MockFixture, action: str, path_input: Path) -> None:
    """Run mocked action."""
    functions = {"add": "add_jobs",
                 "compute": "compute_jobs",
                 "query": "query_properties",
                 "report": "report_properties"}

    # Mock argparse
    mocker.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(
        command=action, input=path_input))

    # Mock the action
    mocker.patch(f"moka.cli.{functions[action]}", return_value=None)

    main()


def call_wrong_input(mocker: MockFixture, action: str, message: str, excp: BaseException) -> None:
    """Call CLI with incorrect arguments."""
    path_input = PATH_TEST / "wrong_input.yml"

    mocker.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(
        command=action, input=path_input))

    with pytest.raises(excp) as info:
        main()

    error = info.value.args[0]
    assert message in error

def test_cli(mocker: MockFixture):
    """Test the command line interface."""
    actions = ("compute", "query", "report", "add")

    for action in actions:
        path_input = PATH_TEST / f"input_test_{action}.yml"
        run_workflow_mock(mocker, action, path_input)


def test_wrong_action(mocker: MockFixture):
    """Check that the validation fails if a wrong action is provided."""
    call_wrong_input(mocker, "tessellate", "unknown action:", RuntimeError)


def test_wrong_input(mocker: MockFixture):
    """Check that the validation fails if call with invalid arguments."""
    call_wrong_input(mocker, "compute", "Missing keys", schema.SchemaMissingKeyError)
