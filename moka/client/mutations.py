"""Module to create mutations perform by the server."""

from typing import Dict

__all__ = ["create_job_mutation", "create_job_status_mutation", "create_job_update_mutation"]


def create_job_mutation(job_info: Dict[str, str], prop_info: Dict[str, str]) -> str:
    """Create string with mutation to add a new job to the server."""
    inp = f"""
    mutation {{
  createJob(input: {{
    _id: {job_info['job_id']}
    property: {{
      _id: {prop_info['smile_id']}
      smile: "{prop_info['smile']}"
      collection_name: "{prop_info['collection_name']}"

    }}
    status: {job_info['status']}
    settings: "{job_info['settings']}"
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
    return format_null(inp)


def create_job_update_mutation(job_info: Dict[str, str], prop_info: Dict[str, str]) -> str:
    """Create string with mutation to add a new job to the server."""
    inp = f"""
    mutation {{
  updateJob(input: {{
    _id: {job_info['job_id']}
    property: {{
      _id: {prop_info['smile_id']}
      smile: "{prop_info['smile']}"
      collection_name: "{prop_info['collection_name']}"
      data: "{prop_info['data']}"
      geometry: "{prop_info['geometry']}"
      input: "{prop_info['input']}"

    }}
    status: {job_info['status']}
    user: "{job_info['user']}"
    platform: "{job_info['platform']}"
    report_time: {job_info['report_time']}

  }}) {{
    _id
    status
  }}
}}
"""
    return format_null(inp)


def create_job_status_mutation(info: Dict[str, str]) -> str:
    """Create string with mutation to add a new job to the server."""
    inp = f"""
    mutation {{
  updateJobStatus(input: {{
    _id: {info['job_id']}
    status: {info['status']}
    collection_name: "{info['collection_name']}"
    schedule_time: {info['schedule_time']}
    report_time: {info['report_time']}
}}) {{
    _id
    status
  }}
}}
"""
    return format_null(inp)


def format_null(string: str) -> str:
    """Remove the quotes from the null values."""
    return string.replace("\"null\"", "null")
