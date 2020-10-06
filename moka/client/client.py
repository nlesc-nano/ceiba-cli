"""Client to query the server.

API
---
.. autofunction:: query_server

"""
import json
from typing import Any, Dict

import requests


__all__ = ["query_server"]


def query_server(url: str, query: str) -> Dict[str, Any]:
    """Query the server using graphql.

    Parameters
    ----------
    url
        server URL
    query
        `Graphql <https://graphql.org/>` query

    Returns
    -------
    JSON dictionary with the data

    """
    reply = requests.post(url, json={'query': query})
    status = reply.status_code
    if status != 200:
        raise RuntimeError(f"The query doesn't succeed. Error {status}")
    data = json.loads(reply.text)
    if data.get("errors", None) is not None:
        raise RuntimeError(f"There was an error querying the server:\n{data['errors']}")
    return data["data"]
