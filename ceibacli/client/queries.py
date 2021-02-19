"""Module to create all the available queries."""

from typing import Union

__all__ = ["create_jobs_query", "create_properties_query"]


def create_properties_query(collection_name: str) -> str:
    """Create a query for the properties in a collection."""
    return f"""query{{
    properties (collection_name: "{collection_name}") {{
        _id
        metadata
        data
    }}
}}
"""


def create_collections_query() -> str:
    """Create query for available collections."""
    return """query {
       collections {
           name
           size
       }
   }
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
    jobs (status: {status}, collection_name: "{collection_name}", max_jobs: {max_jobs}) {{
        _id
        property {{
            _id
            collection_name
            metadata
            data
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


def query_introspection() -> str:
    """Retrieve available queries."""
    return """query {
    __type(name: "Query") {
        kind
        name
        fields {
            name
            description
            args {
                name
                description
                defaultValue
            }
        }
        possibleTypes {
            name
            kind
            description
        }
    }
}
"""
