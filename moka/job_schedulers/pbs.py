"""Interface to the `PBS job scheduler <https://en.wikipedia.org/wiki/Portable_Batch_System>`_

.. autofunction:: create_pbs_script

"""

from pathlib import Path
from typing import Any, Dict

from ..utils import Options


def create_pbs_script(opts: Options, job: Dict[str, Any], job_workdir: Path) -> str:
    """Create a script to run the workflow using the PBS job schedule."""
    pass
