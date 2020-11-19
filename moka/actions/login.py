"""Module to log in to the Web service.

API
---
.. autofunction:: login_insilico
"""

from ..client.mutations import create_authentication_mutation
from ..client import query_server
from ..utils import Options

def login_insilico(opts: Options) -> None:
    """Log in to the Insilico web service."""
    mutation = create_authentication_mutation(opts.token)
    reply = query_server(opts.url, mutation)
