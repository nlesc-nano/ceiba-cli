"""Functions use for testing."""

import json
from pathlib import Path
from typing import Any, Dict

import pkg_resources as pkg

__all__ = ["PATH_MOKA", "PATH_TEST"]

# Environment data
PATH_MOKA = Path(pkg.resource_filename('moka', ''))
ROOT = PATH_MOKA.parent

PATH_TEST = ROOT / "tests" / "files"


def read_mocked_reply(file_name: str) -> Dict[str, Any]:
    """Read a mocked JSON reply from ``file_name``."""
    path_reply = PATH_TEST / "mocked_replies" / file_name
    with open(path_reply, 'r') as handler:
        reply = json.load(handler)

    return reply
