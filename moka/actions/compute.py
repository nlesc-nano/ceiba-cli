"""Module to compute some jobs from the server."""

import logging
from ..client import query_server
from ..client.queries import create_jobs_query
from ..utils import Options

logger = logging.getLogger(__name__)


def compute_jobs(opts: Options) -> None:
    """Compute some jobs using the configuration."""
    query = create_jobs_query(opts.job_status)
    jobs = query_server(opts.url, query)
    print(jobs["data"]["jobs"])
    # for j in jobs:
    #     succeeded = schedule_job(j)
    #     if not succeeded:
    #         logger.warn(f"Job {jobs['id']} fails to be scheduled!")
    #     update_job_status(jobs, status="RUNNING")