"""Module to compute some jobs from the server.

API
---
.. compute_jobs:: compute_jobs

"""

import logging
import sys
from pathlib import Path
from subprocess import DEVNULL, check_call
from typing import Any, Dict

import yaml

from ..client import query_server
from ..client.queries import create_jobs_query
from ..job_schedulers import create_pbs_script, create_slurm_script
from ..utils import Options

logger = logging.getLogger(__name__)


def compute_jobs(opts: Options) -> None:
    """Compute some jobs using the configuration."""
    query = create_jobs_query(opts.job_status)
    jobs = query_server(opts.url, query)
    logger.info(f"Job scheduler: {opts.scheduler}")
    
    print(jobs["data"]["jobs"])
    for j in jobs:
        succeeded = schedule_job(opts, j)
        if not succeeded:
            logger.warn(f"Job {jobs['id']} fails to be scheduled!")
    #     update_job_status(jobs, status="RUNNING")


def schedule_job(opts: Options, job: Dict[str, Any]) -> bool:
    """Schedule a job to run locally or using job scheduler."""
    job_id = job['id']
    # Folder where the job data is going to be stored
    job_workdir = Path(opts.workdir) / f"job_{job_id}"

    # input used by the workflow runner
    input_file = write_input_file(opts, job, job_workdir)

    # Generate the script to submit the job using the
    # user provide scheduler
    scheduler = opts.scheduler.lower()
    script_generator = {"slurm": create_slurm_script, "pbs": create_slurm_script}
    if scheduler == "none":
        cmd = f"{opts.command} {input_file} &"
    else:
        cmd = script_generator[scheduler](opts, job, job_workdir)
    try:
        run_command(cmd, job_workdir)
        return True
    except:
        msg = f"Job {job_id} failed with error:\n{sys.exc_info()[0]}"
        logger.warning(msg)
        return False


def write_input_file(opts: Options, job: Dict[str, Any], job_workdir: Path) -> str:
    """Write input to run the workflow in YAML format."""
    input_file = job_workdir / f"input_file_job_{job['id']}.yml"

    with open(input_file, 'w') as handler:
        yaml.dump(opts.settings, handler, indent=4)

    return input_file.absolute().as_posix()


def run_command(cmd: str, workdir: str) -> bool:
    """Run ``cmd`` as subprocess."""
    result = check_call(cmd, shell=True, stdout=DEVNULL, cwd=workdir)
    return result == 0
