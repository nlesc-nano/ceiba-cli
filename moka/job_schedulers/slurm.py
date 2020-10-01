"""Interface to the `SLURM job scheduler <https://slurm.schedmd.com/documentation.html>`_

.. autofunction:: create_slurm_script
"""

from pathlib import Path
from typing import Any, Dict
from ..utils import Options


def create_slurm_script(opts: Options, job: Dict[str, Any], job_workdir: Path) -> str:
    """Create a script to run the workflow using the SLURM job schedule."""
    pass
