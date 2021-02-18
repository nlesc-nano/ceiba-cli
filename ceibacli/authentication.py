"""Functionality to send authentication credentials to the server.

API
---
.. autofunction:: fetch_cookie

"""
import sys
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
    path_cookie = Path.home() / ".ceiba_web_service"
    if not path_cookie.exists():
        print("You need to login to modify properties in the server!")
        sys.exit()
    with open(path_cookie, 'r') as handler:
        cookie = handler.read()

    return cookie.replace('\"', '\\"')
