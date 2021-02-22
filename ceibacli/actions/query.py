"""Module to query properties from the server.

API
---
.. autofunction:: query_properties

"""

import pandas as pd

from ..client import query_server
from ..client.queries import create_properties_query, create_collections_query
from ..utils import Options, json_properties_to_dataframe


def query_properties(opts: Options) -> pd.DataFrame:
    """Retrieve either the properties of a collection or the available collections."""
    if opts.collection_name is not None:
        return query_collection_properties(opts)
    else:
        return query_available_collections(opts)


def query_available_collections(opts: Options) -> pd.DataFrame:
    """Search for the available collections."""
    # Graphql query to get the collections
    query = create_collections_query()
    # Call the server
    reply = query_server(opts.web, query)
    collections = json_properties_to_dataframe(reply["collections"])
    print("Available collections:\n", collections)
    return collections


def query_collection_properties(opts: Options) -> pd.DataFrame:
    """Query the user requested properties."""
    # Graphql query to get the properties
    query = create_properties_query(opts.collection_name)
    # Call the server
    reply = query_server(opts.web, query)
    # Transform the JSON reply into a DataFrame
    properties = reply["properties"]
    df = json_properties_to_dataframe(properties)
    output_file = f"{opts.collection_name}.csv"
    df.to_csv(output_file)
    print(f"Requested properties has been save to: {output_file}")
    return df
