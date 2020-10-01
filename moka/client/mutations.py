"""Module to create mutations perform by the server."""

from typing import Dict

from ..utils import Options

__all__ = ["create_job_mutation"]


def create_job_mutation(info: Dict[str, str]) -> str:
    """Create string with mutation to add a new job to the server."""
    return f"""
    mutation {{
  createJob(input: {{
    id: {info['job_id']}
    property: {{
      id: {info['smile_id']}
      smile: "{info['smile']}"
      collection_name: "{info['collection_name']}"
    }}
    status: {info['status']}
    settings: "{info['settings']}"
  }}) {{
    id
    status
  }}
}}
"""

def create_job_status_mutation(info: Dict[str, str]) -> str:
    """Create string with mutation to add a new job to the server."""
    return f"""
    mutation {{
  createJob(input: {{
    id: {info['job_id']}
    status: {info['status']}
    schedule_time: {info['schedule_time']}
    completion_time: {info['completion_time']}
) {{
    id
    status
  }}
}}
"""
