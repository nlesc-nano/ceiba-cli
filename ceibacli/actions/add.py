"""Module to add new jobs to the server.

API
---
.. autofunction:: add_job
"""

__all__ = ["add_job"]

import logging
from collections import defaultdict
from typing import Any, DefaultDict

import numpy as np
import pandas as pd

from ..authentication import fetch_cookie
from ..client import query_server
from ..client.mutations import create_job_mutation
from ..client.queries import create_properties_query
from ..utils import (Options, format_settings, generate_identifier,
                     json_properties_to_dataframe)

logger = logging.getLogger(__name__)


def fetch_candidates(opts: Options) -> pd.DataFrame:
    """Retrieve candidates to compute from the server."""
    query = create_properties_query(opts.target_collection)
    reply = query_server(opts.web, query)
    return json_properties_to_dataframe(reply["properties"])


def add_job(opts: Options) -> None:
    """Add new jobs to the server."""
    opts.cookie = fetch_cookie()
    # Get the data to create the jobs
    mutation = create_mutations(opts)
    reply = query_server(opts.web, mutation)
    logger.info("New Jobs: ", reply['createJob']['text'])


def create_mutations(opts: Options) -> str:
    """Create a mutations with the new job."""
    job_info = defaultdict(lambda: "null")  # type: DefaultDict[str, Any]
    prop_info = defaultdict(lambda: "null")  # type: DefaultDict[str, Any]
    metadata = format_settings(opts.settings)
    job_info.update({
        "job_id": np.random.randint(0, 2147483647),
        "status": "AVAILABLE",
        "settings": metadata})

    prop_info.update({
        "id": generate_identifier(metadata),
        "metadata": metadata,
        "collection_name": opts.collection_name,
    })

    return create_job_mutation(opts.cookie, job_info, prop_info)
