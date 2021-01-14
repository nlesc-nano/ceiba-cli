"""API to create an interface to job schedulers."""

from .slurm import create_slurm_script


__all__ = ["create_slurm_script"]
