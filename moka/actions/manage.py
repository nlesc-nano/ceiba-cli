"""Module to move the data back to the server.

API
---
.. autofunction:: report_properties

"""

import logging
import numpy as np
from datetime import datetime
from ..client import query_server
from ..client.queries import create_jobs_query
from ..utils import Options
from .compute import update_job_status

__all__ = ["manage_jobs"]

logger = logging.getLogger(__name__)


def is_job_time_expired(allow_time: int, schedule_time: float) -> bool:
    """Check if the allow time for a job in RUNNING or RESEVERED state has expired.

    Parameters
    ----------
    allow_time
        Maximum time allow in RESERVED/RUNNING state (in hours)
    schedule_time
        Timestamp when the job was reserved

    Returns
    -------
    Whether or not the job has expired.

    """
    # Current time
    now = datetime.timestamp(datetime.now())
    # Compute the amount of hours since the job was marked as RESERVED
    delta = (now - schedule_time) / 3600
    return np.ceil(delta) > allow_time


def manage_jobs(opts: Options) -> None:
    """Update jobs state."""
    action = opts.change_status
    # All sizes
    job_size = "null"
    max_jobs = "null"
    query = create_jobs_query(action.old_status, opts.collection_name, max_jobs, job_size)
    # Call the server
    jobs = query_server(opts.url, query)["jobs"]
    if not jobs:
        logger.info(f"No jobs in collection {opts.collection_name} with status {action.old_status}")

    # Maximum number of hours that the job can be RESERVED
    expiration_time = action.expiration_time

    target_jobs = filter(lambda j: is_job_time_expired(expiration_time, j["schedule_time"]), jobs)

    for job in target_jobs:
        update_job_status(opts, job, action.new_status)
