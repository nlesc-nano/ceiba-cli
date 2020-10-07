"""Module to create mutations perform by the server."""

from typing import Dict


__all__ = ["create_job_mutation"]


def create_job_mutation(info: Dict[str, str]) -> str:
    """Create string with mutation to add a new job to the server."""
    return f"""
    mutation {{
  createJob(input: {{
    _id: {info['job_id']}
    property: {{
      _id: {info['smile_id']}
      smile: "{info['smile']}"
      collection_name: "{info['collection_name']}"
    }}
    status: {info['status']}
    settings: "{info['settings']}"
  }}) {{
    _id
    status
    property {{
      _id
      smile
      collection_name
    }}
  }}
}}
"""


def create_job_status_mutation(info: Dict[str, str]) -> str:
    """Create string with mutation to add a new job to the server."""
    return f"""
    mutation {{
  updateJobStatus(input: {{
    _id: {info['job_id']}
    status: {info['status']}
    collection_name: "{info['collection_name']}"
    schedule_time: {info['schedule_time']}
    completion_time: {info['completion_time']}
}}) {{
    _id
    status
  }}
}}
"""
