"""Module to query properties from the server.

API
---
.. autofunction:: query_properties

"""
import json

import pandas as pd

from ..client import query_server
from ..utils import Options


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
