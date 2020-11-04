"""Module to test the job schedulers."""

from pathlib import Path
from moka.job_schedulers.slurm import create_slurm_script
from moka.utils import Options


def check_script(opts: Options, tmp_path: Path) -> None:
    """Check that the SLURM script is created."""
    input_file = tmp_path / "job_input.yml"
    smile = "CCO"
    command = create_slurm_script(opts, smile, input_file)
    script = command.split()[1]

    assert Path(script).exists()


def test_slurm_script_generation(tmp_path: Path):
    """Check that the slurm script is correctly generated."""
    opts = Options({
        "command": "run_workflow",
        "scheduler":
        {"name": "slurm", "nodes": 2, "cpus-per-task": 24, "wall_time": "01:12:00",
         "partition": "saturn"}})

    check_script(opts, tmp_path)


def test_slurm_free_format(tmp_path: Path):
    """Test the slurm script generation with the user passes its own script."""
    free_format = """#!/bin/bash

#SBATCH -N 1
#SBATCH -t 00:05:00
#SBATCH -p godzilla

module load awesome-package/3.14.15
"""

    opts = Options({
        "command": "run_workflow",
        "scheduler":
        {"name": "slurm", "free_format": free_format}})

    check_script(opts, tmp_path)
