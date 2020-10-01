"""Module to move the data back to the server.

API
---
.. autofunction:: report_properties

"""

import getpass
import platform
from datetime import datetime
from pathlib import Path

import pandas as pd

from ..client import query_server
from ..utils import Options


def read_properties_from_csv(path_results: Path) -> pd.DataFrame:
    """From a csv file to a pandas DataFrame."""
    if not path_results.exists():
        raise RuntimeError(f"{path_results} doesn't exists!")
    df = pd.read_csv(path_results).reset_index(drop=True)
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]


def report_properties(opts: Options) -> None:
    """Send computed properties to the server."""
    # Read the data
    df = read_properties_from_csv(Path(opts.path_results))
    meta_data = {"user": getpass.getuser(),
                 "platform": platform.platform(),
                 "completion_time": datetime.timestamp()
                 }

    print(df, meta_data)
    # for _, row in df.iterrows():
    #     query_server.

