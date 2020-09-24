"""Module to add new jobs to the server.

API
---
.. autofunction:: add_jobs
"""

__all__ = ["add_jobs"]

import json
import uuid

import numpy as np
import pandas as pd

from typing import Any, Dict

from ..client import query_server
from ..client.mutations import create_job_mutation
from ..client.queries import create_properties_query
from ..utils import Options, json_properties_to_dataframe


def fetch_candidates(opts: Options) -> pd.DataFrame:
    """Retrieve candidates to compute from the server."""
    query = create_properties_query(opts.target_collection)
    reply = query_server(opts.url, query)
    return json_properties_to_dataframe(reply["data"]["properties"])


def create_mutations(row: pd.Series, opts: Options) -> str:
    """Create a list of mutations with the new jobs."""
    info = {"job_id": np.random.randint(0, 2147483647),
            "smile": row.smile, "smile_id": row.id,
            "collection_name": opts.new_collection,
            "status": "AVAILABLE",
            "settings": format_settings(opts.settings)
            }
    return create_job_mutation(info)


def add_jobs(opts: Options) -> None:
    """Add new jobs to the server."""
    # Get the data to create the jobs
    df_candidates = fetch_candidates(opts)
    # Create the mutation to add the jobs in the server
    rows = df_candidates[["id", "smile"]].iterrows()
    mutations = (create_mutations(row, opts)for _, row in rows)
    for query in mutations:
        new_job = query_server(opts.url, query)
        print(new_job['data'])


def format_settings(settings: Dict[str, Any]) -> str:
    """Format the settings as string."""
    string = json.dumps(settings.to_dict())
    # Escape quotes
    return string.replace('\"', '\\"')
