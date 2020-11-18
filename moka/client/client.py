"""Client to query the server.

API
---
.. autofunction:: query_server

"""
import json
from enum import Enum
from typing import Any, Dict, Optional

import requests


__all__ = ["query_server"]


class Method(Enum):
    """HTTP Method enumeration."""
    GET = 1
    POST = 2


def query_server(url: str, query: str) -> Dict[str, Any]:
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
    reply = requests.post(url, json={'query': query})

    status = reply.status_code
    if status != 200:
        raise RuntimeError(f"The query doesn't succeed. Error {status}")
    data = json.loads(reply.text)
    if data.get("errors", None) is not None:
        raise RuntimeError(f"There was an error querying the server:\n{data['errors']}")
    return data['data']


def check_github_username(
        token: str, github_api: str = 'https://api.github.com/user') -> Optional[str]:
    """Check that the token correspond to a valid GitHub username."""
    header = {'Authorization': f'token {token}'}
    response = requests.get(github_api, headers=header)

    if response.status_code != "200":
        return None

    data = json.loads(response.text)
    return data['login']
