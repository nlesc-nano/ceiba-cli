"""API to create an interface to job schedulers."""

from .pbs import create_pbs_script
from .slurm import create_slurm_script


__all__ = ["create_pbs_script", "create_slurm_script"]
