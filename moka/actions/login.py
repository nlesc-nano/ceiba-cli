"""Module to log in to the Web service.

API
---
.. autofunction:: login_insilico
"""

import logging
from pathlib import Path

from ..client import query_server
from ..client.mutations import create_authentication_mutation
from ..utils import Options

logger = logging.getLogger(__name__)


def login_insilico(opts: Options) -> None:
    """Log in to the Insilico web service."""
    mutation = create_authentication_mutation(opts.token)
    reply = query_server(opts.web, mutation)["authenticateUser"]
    text = reply['text']
    if reply['status'] == "FAILED":
        raise RuntimeError(f"login error:\n{text}")
    else:
        logger.info("User has been successfully log in!")
        create_cookie(text)


def create_cookie(cookie: str) -> None:
    """Create a temporal cookie with the server token."""
    with open(Path.home() / ".insilicoserver", 'w') as handler:
        handler.write(cookie)
