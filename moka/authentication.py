"""Functionality to send authentication credentials to the server.

API
---
.. autofunction:: fetch_cookie

"""
from pathlib import Path


def fetch_cookie():
    """Return the cookie to authenticate to the web service.

    Returns
    -------
    Authentication cookie

    Raises
    ------
    Runtime error if there is not cookie

    """
    path_cookie = Path.home() / ".insilicoserver"
    if not path_cookie:
        raise RuntimeError("You need to login to modify properties in the server!")
    with open(path_cookie, 'r') as handler:
        cookie = handler.read()

    return cookie.replace('\"', '\\"')
