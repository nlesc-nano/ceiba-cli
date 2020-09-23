"""Module to compute molecular properties using a given workflow.

API
---

"""
import json
from typing import Any, Dict

import pandas as pd
import requests

from .utils import Options


def create_jobs_query(status: str, kind="job") -> str:
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
        {kind} (status: {status} {{
            id
            property {{
              id
              theory_level
              smile
              geometry
              values
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


def query_server(url: str, query: str) -> Dict[str, Any]:
    """Query the server using graphql.

    Parameters
    ----------
    url
        server URL
    query
        graphql query

    Returns
    -------
    JSON dictionary with the data

    """
    reply = requests.post(url, json={'query': query})
    status = reply.status_code
    if status != 200:
        raise RuntimeError(f"The query doesn't succeed. Error {status}")
    return json.loads(reply.text)


def query_properties(opts: Options) -> pd.Dataframe:
    """Query the user requested properties."""
    pass
