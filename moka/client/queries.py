"""Module to create all the available queries."""

from typing import Union

__all__ = ["create_jobs_query"]


def create_properties_query(collection_name: str) -> str:
    """Create a query for the properties in a collection."""
    return f"""query{{
    properties (collection_name: "{collection_name}") {{
        _id
        smile
        geometry
        data
    }}
}}
"""


def create_jobs_query(
        status: str, collection_name: str, max_jobs: Union[str, int], job_size: str) -> str:
    """Create a query a list of jobs by status.

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
    jobs (status: {status}, collection_name: "{collection_name}", max_jobs: {max_jobs}, job_size: {job_size}) {{
        _id
        property {{
            _id
            collection_name
            smile
            data
            geometry
        }}
        settings
        status
        user
        schedule_time
        report_time
        platform
    }}
}}
"""
