"""Mock a workflow runner."""

import argparse
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import yaml

from .cli import exists


def validate_input(file_input: Path) -> Dict[str, Any]:
    """Check that the input is in yaml format."""
    with open(file_input, 'r') as handler:
        dict_input = yaml.load(handler.read(), Loader=yaml.FullLoader)

    return dict_input


def main():
    """Read command line arguments."""
    parser = argparse.ArgumentParser("mock_runner")
    parser.add_argument("input", type=exists, help="YAML input file")
    args = parser.parse_args()
    opts = validate_input(args.input)
    print(f"Running with options:\n", yaml.dump(opts))

    data = pd.DataFrame.from_records({
        "prop1": [3.1415926535897932], "prop2": [42], "prop3": [1.618]})
    data.to_csv("result.csv")

    print("data store at result.csv")
