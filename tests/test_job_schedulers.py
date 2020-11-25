"""Module to test the job schedulers."""

from pathlib import Path
from moka.actions.compute import create_job_metadata
from moka.job_schedulers.slurm import create_slurm_script
from moka.utils import Options
from typing import Any, Dict


def check_script(tmp_path: Path, scheduler: Dict[str, Any]) -> None:
    """Check that the SLURM script is created."""
    opts = Options({
        "workdir": tmp_path,
        "command": "run_workflow",
        "scheduler": scheduler})

    jobs = [{'_id': 1000, "settings": '{"input": {"prop1": "compute"}}',
             'property': {
                 '_id': 42, 'smile': 'CCCCCCCCC=CCCCCCCCC(=O)O',
                 'collection_name': "test_collection"}}]
    jobs_metadata = [create_job_metadata(opts, j) for j in jobs]
    command = create_slurm_script(opts, jobs, jobs_metadata)
    script = command.split()[1]

    assert Path(script).exists()


def test_slurm_script_generation(tmp_path: Path):
    """Check that the slurm script is correctly generated."""
    scheduler = {
        "name": "slurm", "nodes": 2, "cpus-per-task": 24, "wall_time": "01:12:00",
        "partition": "saturn"}

    check_script(tmp_path, scheduler)


def test_slurm_free_format(tmp_path: Path):
    """Test the slurm script generation with the user passes its own script."""
    free_format = """#!/bin/bash

#SBATCH -N 1
#SBATCH -t 00:05:00
#SBATCH -p godzilla

module load awesome-package/3.14.15
"""
    scheduler = {"name": "slurm", "free_format": free_format}

    check_script(tmp_path, scheduler)
