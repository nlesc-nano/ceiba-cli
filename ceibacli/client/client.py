+"""Client to query the server.

API
---
.. autofunction:: query_server

"""
import json
from typing import Any, Dict, Optional

import requests


__all__ = ["query_server"]


def query_server(url: str, query: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Query the ``url`` API using ``query``.

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
    reply = requests.post(url, json={'query': query}, headers=headers)

    status = reply.status_code
    if status != 200:
        raise RuntimeError(f"The query doesn't succeed. Error {status}")
    data = json.loads(reply.text)
    if data.get("errors", None) is not None:
        raise RuntimeError(f"There was an error querying the server:\n{data['errors']}")
    return data['data']
