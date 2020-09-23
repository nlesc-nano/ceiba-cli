"""Client to query the server.

API
---
.. autofunction:: query_server

"""
import json
from typing import Any, Dict

import pandas as pd
import requests

from ..utils import Options

__all__ = ["query_server"]


def query_server(url: str, query: str) -> Dict[str, Any]:
    """Query the server using graphql.

    Parameters
    ----------
    url
        server URL
    query
        graphql query

    Returns
    -------
    JSON dictionary with the data

    """
    reply = requests.post(url, json={'query': query})
    status = reply.status_code
    if status != 200:
        raise RuntimeError(f"The query doesn't succeed. Error {status}")
    return json.loads(reply.text)


def query_properties(opts: Options) -> pd.DataFrame:
    """Query the user requested properties."""
    query = f"""query{{
    properties (collection_name: "{opts.collection_name}") {{
        id
        smile
        geometry
        data
    }}
}}
"""
    properties = query_server(opts.url, query)
    df = pd.DataFrame(properties['data']['properties'])
    df['data'].fillna("{}", inplace=True)
    df['data'] = df['data'].apply(lambda x: json.loads(x))
    df.to_csv(opts.output_file)
    return df
