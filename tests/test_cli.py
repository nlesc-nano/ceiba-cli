"""Test the command line interface."""

import argparse
import sys
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
                 "report": "report_properties",
                 "manage": "manage_jobs"
                 }

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
    actions = ("compute", "query", "report", "add", "manage")

    for action in actions:
        path_input = PATH_TEST / f"input_test_{action}.yml"
        run_workflow_mock(mocker, action, path_input)


def test_wrong_action(mocker: MockFixture):
    """Check that the validation fails if a wrong action is provided."""
    call_wrong_input(mocker, "tessellate", "unknown action:", RuntimeError)


def test_wrong_input(mocker: MockFixture):
    """Check that the validation fails if call with invalid arguments."""
    call_wrong_input(mocker, "compute", "Missing key", schema.SchemaMissingKeyError)


def test_non_existing_file(capsys):
    """Check that an error is raised if the input file doesn't exist."""
    path_input = "Nonexistingfile.yml"

    with pytest.raises(SystemExit):
        sys.argv = ['compute', path_input]
        main()

    captured = capsys.readouterr()
    assert "error: argument command: invalid choice" in captured.err


def test_no_command_argument(mocker: MockFixture, capsys):
    """Check that the program exit if there is no command."""
    mocker.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(
        command=None, input=PATH_TEST / "wrong_input.yml"))

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()

    assert "usage: moka [-h] [--version] {login,compute,report,query,add,manage} ..." in captured.out


def test_no_input_file(mocker: MockFixture):
    """Check that defaults are correctly applied when no input file is provided."""
    # Mock command line user input
    mocker.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(
        command="report", web="localhost:8080/graphql"))

    # Mock action
    mocker.patch("moka.cli.report_properties", return_value=None)

    main()


def test_login():
    """Check the login functionality."""
    pass
