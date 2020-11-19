"""Client to query the server.

API
---
.. autofunction:: check_github_username
.. autofunction:: query_server

"""
import json
from typing import Any, Dict, Optional

import requests


__all__ = ["check_github_username", "query_server"]


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


def check_github_username(
        token: str, github_api: str = 'https://api.github.com/graphql') -> Optional[str]:
    """Check that the token correspond to a valid GitHub username.

    Using  `GitHub GraphQL API v4 <https://developer.github.com/v4/>`_

    Parameters
    ----------
    token
        GitHub token that gives read only authorization
    github_api
        URL of GitHub's API

    Return
    ------
    GitHub's username or None

    """
    headers = {'Authorization': f'bearer {token}'}
    query = "query { viewer { login }}"
    try:
        data = query_server(github_api, query, headers)
        return data['viewer']['login'].lower()
    except RuntimeError:
        return None
