"""Module to create all the available queries."""

__all__ = ["create_jobs_query"]


def create_properties_query(collection_name: str) -> str:
    """Create a query for the properties in a collection."""
    return f"""query{{
    properties (collection_name: "{collection_name}") {{
        id
        smile
        geometry
        data
    }}
}}
"""


def create_jobs_query(status: str, kind="jobs") -> str:
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
