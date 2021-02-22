"""Check that the mocked computing workflow works."""

import sys
from numbers import Real
from pathlib import Path

import pandas as pd

from ceibacli.mock_workflow import main

from .utils_test import PATH_TEST


def test_mock_workflow(tmp_path: Path):
    """"Check mock workflow script."""
    path_input = PATH_TEST / "input_test_compute.yml"

    # Inyect command line arguments
    sys.argv = ['mock_runner', path_input.as_posix()]
    main()
    # Show that the results file exists
    output_file = Path("result.csv")
    assert output_file.exists()

    # Checkt that the results can be read
    frame = pd.read_csv(output_file)
    assert isinstance(frame.prop1[0], Real)

    if output_file.exists:
        output_file.unlink()