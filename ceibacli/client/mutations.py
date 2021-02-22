"""Module to create mutations perform by the server."""
from typing import Any, DefaultDict, Dict

from ..utils import Options

__all__ = ["create_job_mutation", "create_job_status_mutation", "create_job_update_mutation",
           "create_property_mutation"]


def create_property_mutation(cookie: str, prop_info: Dict[str, str]) -> str:
    """Create a string with the mutation to update a property."""
    inp = f"""mutation {{
    updateProperty(cookie: "{cookie}",
      input: {{
      _id: {prop_info['id']}
      collection_name: "{prop_info['collection_name']}"
      metadata: "{prop_info['metadata']}"
      data: "{prop_info['data']}"
      input: "{prop_info['input']}"
    }}) {{
    status
    text
  }}
}}
"""
    return format_null(inp)


def create_job_mutation(cookie: str, job_info: Dict[str, str], prop_info: Dict[str, str]) -> str:
    """Create string with mutation to add a new job to the server."""
    inp = f"""
    mutation {{
  createJob(cookie: "{cookie}",
    input: {{
    _id: {job_info['job_id']}
    property: {{
      _id: {prop_info['id']}
      metadata: "{prop_info['metadata']}"
      collection_name: "{prop_info['collection_name']}"
    }}
    status: {job_info['status']}
    settings: "{job_info['settings']}"
  }}) {{
    status
    text
  }}
}}
"""
    return format_null(inp)


def create_job_update_mutation(
        job_info: DefaultDict[str, str], prop_info: DefaultDict[str, str],
        opts: Options) -> str:
    """Create string with mutation to add a new job to the server."""
    inp = f"""
    mutation {{
  updateJob(cookie: "{opts.cookie}",
     input: {{
    _id: {job_info['job_id']}
    property: {{
      _id: {prop_info['id']}
      collection_name: "{prop_info['collection_name']}"
      metadata: {prop_info['metadata']}
      data: "{prop_info['data']}"
      input: "{prop_info['input']}"
      large_objects: "{prop_info['large_objects']}"

    }}
    status: {job_info['status']}
    user: "{job_info['user']}"
    platform: "{job_info['platform']}"
    report_time: {job_info['report_time']}

  }}
    duplication_policy: {opts.duplication_policy}
  ) {{
    text
    status
  }}
}}
"""
    return format_null(inp)


def create_job_status_mutation(cookie: str, info: Dict[str, Any]) -> str:
    """Create string with mutation to add a new job to the server."""
    inp = f"""
    mutation {{
  updateJobStatus(cookie: "{cookie}",
    input: {{
    _id: {info['job_id']}
    status: {info['status']}
    collection_name: "{info['collection_name']}"
    user: "{info['user']}"
    schedule_time: {info['schedule_time']}
    report_time: {info['report_time']}
}}) {{
    text
    status
  }}
}}
"""
    return format_null(inp)


def create_authentication_mutation(token: str) -> str:
    """Create a string representing a mutation to authenticate an user."""
    return f"""
    mutation {{
  authenticateUser(token: "{token}")
  {{
    text
    status
  }}
}}
"""


def format_null(string: str) -> str:
    """Remove the quotes from the null values."""
    return string.replace("\"null\"", "null")
