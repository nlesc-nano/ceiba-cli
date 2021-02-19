"""Module to add new jobs to the server.

API
---
.. autofunction:: add_jobs
"""

__all__ = ["add_jobs"]

import json
import logging
from collections import defaultdict
from typing import Any, DefaultDict, Dict, List

import numpy as np

from ..authentication import fetch_cookie
from ..client import query_server
from ..client.mutations import create_job_mutation
from ..utils import Options, format_json, generate_identifier

logger = logging.getLogger(__name__)


def retrieve_jobs(opts: Options) -> List[Dict[str, Any]]:
    """Retrieve candidates to compute from the server."""
    with open(opts.jobs, 'r') as handler:
        jobs = json.load(handler)

    if not isinstance(jobs, list):
        raise RuntimeError("Jobs must be a list of JSON objects")

    return jobs


def add_jobs(opts: Options) -> None:
    """Add new jobs to the server."""
    opts.cookie = fetch_cookie()
    # Get the data to create the jobs
    logger.info("Jobs:")
    for job in retrieve_jobs(opts):
        mutation = create_mutations(opts, job)
        reply = query_server(opts.web, mutation)
        logger.info({reply['createJob']['text']})


def create_mutations(opts: Options, job: Dict[str, Any]) -> str:
    """Create a mutations with the new job."""
    job_info = defaultdict(lambda: "null")  # type: DefaultDict[str, Any]
    prop_info = defaultdict(lambda: "null")  # type: DefaultDict[str, Any]
    metadata = format_json(job)
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
