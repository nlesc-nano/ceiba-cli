"""Test the command line interface."""

import argparse

from pathlib import Path
from pytest_mock import MockFixture, mocker

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


def test_cli(mocker: MockFixture):
    """Test the command line interface."""
    actions = ("compute", "query", "report", "add")

    for action in actions:
        path_input = PATH_TEST / f"input_test_{action}.yml"
        run_workflow_mock(mocker, action, path_input)
