"""Module to compute some jobs from the server.

API
---
.. compute_jobs:: compute_jobs

"""

import getpass
import json
import logging
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from subprocess import CalledProcessError, check_output
from typing import Any, DefaultDict, Dict, List

import yaml

from ..authentication import fetch_cookie
from ..client import query_server
from ..client.mutations import create_job_status_mutation
from ..client.queries import create_jobs_query
from ..job_schedulers import create_slurm_script
from ..utils import Options

logger = logging.getLogger(__name__)


def compute_jobs(opts: Options) -> None:
    """Compute some jobs using the configuration."""
    opts.cookie = fetch_cookie()
    # Generate jobs
    job_size = "null" if opts.job_size is None else opts.job_size.upper()
    query = create_jobs_query(opts.job_status, opts.collection_name, opts.max_jobs, job_size)
    jobs = query_server(opts.web, query)["jobs"]
    check_jobs(jobs)
    # Mark  jobs as  RESERVED so no other repeat the calculation
    mark_jobs_as_reseved(opts, jobs)

    logger.info(f"Using scheduler: {opts.scheduler.name}")
    for j in jobs:
        succeeded = schedule_job(opts, j)
        if not succeeded:
            logger.warn(f"Job {j['_id']} fails to be scheduled!")
            update_job_status(opts, j, "FAILED")
        else:
            update_job_status(opts, j, "RUNNING")


def check_jobs(jobs: List[Dict[str, Any]]) -> None:
    """Check that there are jobs to run."""
    if not jobs:
        print("There are no jobs to run!!")
        sys.exit()


def schedule_job(opts: Options, job: Dict[str, Any]) -> bool:
    """Schedule a job to run locally or using job scheduler."""
    job_id = job['_id']
    # Folder where the job data is going to be stored
    job_workdir = Path(opts.workdir) / f"job_{job_id}"
    if not job_workdir.exists():
        os.makedirs(job_workdir, exist_ok=True)

    # input used by the workflow runner
    input_file = write_input_file(job, job_workdir)

    # Write job metadata in the folder to read when reporting
    write_metadata(job, job_workdir)

    # Generate the script to submit the job using the
    # user provide scheduler
    scheduler = opts.scheduler.name

    # Command to run the workflow
    smile = job["property"]["smile"]
    if scheduler == "none":
        # Run locally
        cmd = f'{opts.command} -s "{smile}" -i {input_file.absolute().as_posix()} &'
    else:
        # Schedule the job
        cmd = create_slurm_script(opts, smile, input_file)

    logger.info(f"Running workflow:\n{cmd}")
    return run_command(cmd, job_workdir)


def write_input_file(job: Dict[str, Any], job_workdir: Path) -> Path:
    """Write input to run the workflow in YAML format."""
    input_file = job_workdir / f"input_file_job_{job['_id']}.yml"

    with open(input_file, 'w') as handler:
        settings = json.loads(job['settings'])
        yaml.dump(settings, handler, indent=4)

    return input_file.absolute()


def write_metadata(job: Dict[str, Any], job_workdir: Path):
    """Write the job's metadata that is going to be read in the report step."""
    input_file = job_workdir / "metadata.yml"

    prop = job["property"]
    metadata = {"job_id": job["_id"],
                "property": {
                    "smile_id": prop["_id"], "smile": prop["smile"],
                    "collection_name": prop["collection_name"]}}

    with open(input_file, 'w') as handler:
        yaml.dump(metadata, handler, indent=4)


def run_command(cmd: str, workdir: Path) -> bool:
    """Run ``cmd`` as subprocess."""
    try:
        result = check_output(cmd, shell=True, cwd=workdir)
        logger.info(f"workflow output:\n{result.decode()}")
        return True
    except CalledProcessError as err:
        logger.error(f"Workflow runner failed with error:\n{err}")
        return False


def update_job_status(opts: Options, job: Dict[str, Any], status: str) -> None:
    """Update status of `job`."""
    now = datetime.timestamp(datetime.now())
    report_time = now if status == "FAILED" else "null"

    # Change job metadata
    info = {
        "job_id": job["_id"],
        "status": status,
        "collection_name": opts.collection_name,
        "user": getpass.getuser(),
        "schedule_time": now,
        "report_time": report_time
    }

    query = create_job_status_mutation(opts.cookie, info)
    query_server(opts.web, query)
    logger.info(f"job {job['_id']} has been marked as {status}!")


def mark_jobs_as_reseved(opts: Options, jobs: List[Dict[str, Any]]) -> None:
    """Mark requested jobs as reseved to avoid recomputation of the same job."""
    for job in jobs:
        job_info = defaultdict(lambda: "null")  # type: DefaultDict[str, Any]
        job_info["job_id"] = job["_id"]
        job_info["status"] = "RESERVED"
        job_info["collection_name"] = opts.collection_name
        job_info["schedule_time"] = datetime.timestamp(datetime.now())
        query = create_job_status_mutation(opts.cookie, job_info)
        query_server(opts.web, query)
        logger.info(f"job {job['_id']} has been marked as RESERVED!")
