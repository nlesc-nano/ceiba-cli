"""Module to query properties from the server.

API
---
.. autofunction:: query_properties

"""

import pandas as pd

from ..client import query_server
from ..client.queries import create_properties_query
from ..utils import Options, json_properties_to_dataframe


def query_properties(opts: Options) -> pd.DataFrame:
    """Query the user requested properties."""
    # Graphql query to get the properties
    query = create_properties_query(opts.collection_name)
    # Call the server
    properties = query_server(opts.url, query)
    # Transform the JSON reply into a DataFrame
    df = json_properties_to_dataframe(properties)
    df.to_csv(opts.output_file)
    return df
