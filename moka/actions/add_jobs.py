"""Module to add new jobs to the server.

API
---
.. autofunction:: add_jobs
"""

from ..utils import Options
from ..client import query_server


def create_mutation() -> None:
    """Add new jobs to the server."""
    job_id = 0
    return f"""
    mutation {{
  createJob(input: {{
    id: {job_id}
    property: {{
      id: 0
      smile: "CC(=O)O"
      collection_name: "functional/basisset"
    }}
    status: AVAILABLE
  }}) {{
    id
    status
  }}
}}
"""


def add_jobs(opts: Options) -> None:
    """Add new jobs to the server."""
    mutation = create_mutation()
    new_job = query_server(opts.url, mutation)
    print(new_job)
