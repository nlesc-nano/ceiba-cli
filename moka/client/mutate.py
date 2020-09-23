"""Client to mutate data in the server.

API
---
.. autofunction:: mutate_server

"""

from typing import Any, Dict

from ..utils import Options


def mutate_server(opts: Options, mutation: str, new: Dict[str, Any]) -> None:
    """Mutate the server using the speficied `mutation`.
    
    Parameters
    ----------
    opts
        Options to connect to the API
    mutation
        `Graphql <https://graphql.org/>` mutation
    new
        Dict defining the new object that is going to be update in the server.
    """
    pass
