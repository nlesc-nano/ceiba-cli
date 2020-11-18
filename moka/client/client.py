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
    """Check that the token correspond to a valid GitHub username.

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
    header = {'Authorization': f'token {token}'}
    response = requests.get(github_api, headers=header)
    if response.status_code != "200":
        return None

    data = json.loads(response.text)
    return data['login'].lower()
