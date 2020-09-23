"""Module to compute some jobs from the server."""

from ..client import query_server
from ..utils import Options


def create_jobs_query(status: str, kind="jobs") -> str:
    """Query a list of jobs by status.

    Parameters
    ----------
    status
        Current job status: AVAILABLE, DONE, FAILED or RUNNING
    kind
        Either `job` or `jobs`

    Returns
    -------
    string to query the server

    """
    return f"""query{{
    {kind} (status: {status}) {{
        id
        property {{
            id
            collection_name
            smile
            data
            geometry
        }}
        settings
        status
        user
        schedule_time
        completion_time
        platform
    }}
}}
"""


def compute_jobs(opts: Options) -> None:
    """Compute some jobs using the configuration."""
    query = create_jobs_query(opts.job_status)
    jobs = query_server(opts.url, query)
    print(jobs["data"]["jobs"])
