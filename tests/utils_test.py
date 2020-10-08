"""Functions use for testing."""

from pathlib import Path

import pkg_resources as pkg

__all__ = ["PATH_MOKA", "PATH_TEST"]

# Environment data
PATH_MOKA = Path(pkg.resource_filename('moka', ''))
ROOT = PATH_MOKA.parent

PATH_TEST = ROOT / "tests" / "files"
